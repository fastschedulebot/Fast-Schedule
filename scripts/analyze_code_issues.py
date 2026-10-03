"""Static code-issue scanner for the Fast Scheduler codebase.

Detects three kinds of issues with a lightweight AST pass (no dependencies):

- ``undefined-name``       — a ``Name`` used (Load) that is not defined in the
                             current scope chain, imported, or a builtin.
- ``import-error``         — an absolute import whose top-level module cannot be
                             resolved (checked via ``importlib.util.find_spec``;
                             ``src.*`` imports are verified against the repo root).
- ``callback-user-resolution`` — the edit.py bug class: a callback-query handler
                             (a function that reads ``<param>.callback_query``)
                             that resolves the acting user via the
                             ``_user_*_from_update(update)`` helpers. On a
                             callback update ``update.message`` is None and
                             ``update.effective_message`` is the button message
                             the BOT sent, so those helpers return the BOT's own
                             id. Callback handlers must use
                             ``str(update.callback_query.from_user.id)``.

Two patterns are caught by the callback-user-resolution check:
  A. the handler calls a helper directly;
  B. the handler passes ``update`` into an in-module helper that itself calls a
     helper (the old ``_lookup(update, job_id)`` shape).

A ``# noqa`` comment on the flagged line suppresses the finding.

Run via ``python scripts/analyze_code_issues.py`` (exit 1 on any findings) or
use ``analyze_paths`` from tests.
"""

from __future__ import annotations

import ast
import builtins
import importlib.util
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


@dataclass
class Issue:
    path: str
    line: int
    kind: str
    name: str | None = None
    message: str = ""

    def format(self) -> str:
        location = f"{self.path}:{self.line}" if self.path else str(self.line)
        if self.kind == "undefined-name":
            return f"{location}: undefined name '{self.name}'"
        if self.kind == "import-error":
            return f"{location}: import error: {self.message}"
        return f"{location}: {self.kind}: {self.message}"


# Helpers that derive a user from ``update`` via ``update.message`` /
# ``update.effective_message``. On a CALLBACK update ``effective_message`` is the
# button message the BOT sent, so these resolve the BOT's own id — the edit.py
# bug class. Callback handlers must resolve ``str(update.callback_query.from_user.id)``.
CALLBACK_USER_HELPERS = {
    "_user_id_from_update",
    "_user_from_update",
    "_user_first_name",
    "_user_last_name",
    "_user_username",
}


class StaticIssueScanner:
    def __init__(self, root: Path) -> None:
        self.root = root

    def scan(self, paths: Sequence[Path] | None = None, include_tests: bool = True) -> List[Issue]:
        targets = [self.root] if paths is None else list(paths)
        issues: List[Issue] = []
        for target in targets:
            if target.is_file():
                if self._should_scan_file(target, include_tests):
                    issues.extend(self._scan_file(target))
            else:
                for path in sorted(target.rglob("*.py")):
                    if self._should_scan_file(path, include_tests):
                        issues.extend(self._scan_file(path))
        return issues

    def _should_scan_file(self, path: Path, include_tests: bool) -> bool:
        if not path.is_file():
            return False
        if not path.name.endswith(".py"):
            return False
        if not include_tests and "tests" in path.parts:
            return False
        if any(part in {".venv", "venv", "__pycache__", ".git", "node_modules"} for part in path.parts):
            return False
        return True

    def _scan_file(self, path: Path) -> List[Issue]:
        issues: List[Issue] = []
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            issues.append(Issue(str(path), exc.lineno or 1, "syntax-error", message=str(exc)))
            return issues
        source_lines = source.splitlines()
        issues.extend(self._check_callback_user_resolution(tree, path, source_lines))

        scope_stack: list[dict[str, bool]] = [{}]
        imported_names: set[str] = set()
        builtins_names = set(dir(builtins))

        class Visitor(ast.NodeVisitor):
            def __init__(self, root: Path) -> None:
                self.root = root

            def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name.split(".")[0])
                self.generic_visit(node)

            def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
                module = node.module or ""
                if module:
                    imported_names.update(alias.asname or alias.name for alias in node.names)
                    if self._is_missing_import(module, node.names):
                        issues.append(Issue(str(path), node.lineno, "import-error",
                                            message=f"cannot import {module}"))
                self.generic_visit(node)

            def visit_Name(self, node: ast.Name) -> None:  # noqa: N802
                if isinstance(node.ctx, ast.Load):
                    if (
                        node.id not in imported_names
                        and node.id not in scope_stack[-1]
                        and node.id not in builtins_names
                        and node.id not in {"True", "False", "None", "__name__", "__file__", "__package__"}
                    ):
                        issues.append(Issue(str(path), node.lineno, "undefined-name", name=node.id))
                self.generic_visit(node)

            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
                scope_stack.append({**scope_stack[-1], **{arg.arg: True for arg in node.args.args}})
                self.generic_visit(node)
                scope_stack.pop()

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
                scope_stack.append({**scope_stack[-1], **{arg.arg: True for arg in node.args.args}})
                self.generic_visit(node)
                scope_stack.pop()

            def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
                scope_stack.append({**scope_stack[-1], **{node.name: True}})
                self.generic_visit(node)
                scope_stack.pop()

            def visit_Assign(self, node: ast.Assign) -> None:  # noqa: N802
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        scope_stack[-1][target.id] = True
                self.generic_visit(node)

            def visit_AnnAssign(self, node: ast.AnnAssign) -> None:  # noqa: N802
                if isinstance(node.target, ast.Name):
                    scope_stack[-1][node.target.id] = True
                self.generic_visit(node)

            def visit_For(self, node: ast.For) -> None:  # noqa: N802
                if isinstance(node.target, ast.Name):
                    scope_stack[-1][node.target.id] = True
                self.generic_visit(node)

            def _is_missing_import(self, module: str, names: list[ast.alias]) -> bool:
                if module.startswith("src."):
                    module_path = self.root / (module.replace(".", os.sep) + ".py")
                    if not module_path.exists():
                        return True
                for alias in names:
                    if alias.name == "*":
                        continue
                    if not self._module_exists(module):
                        return True
                return False

            def _module_exists(self, module: str) -> bool:
                if module.startswith("src."):
                    return True
                try:
                    return importlib.util.find_spec(module) is not None
                except (ModuleNotFoundError, ImportError, ValueError):
                    return False

        Visitor(self.root).visit(tree)
        return issues

    @staticmethod
    def _fn_params(node: ast.AST) -> list[str]:
        args = node.args
        names = [a.arg for a in list(args.posonlyargs) + list(args.args)]
        if args.vararg:
            names.append(args.vararg.arg)
        if args.kwarg:
            names.append(args.kwarg.arg)
        names += [a.arg for a in args.kwonlyargs]
        return names

    @staticmethod
    def _helper_calls(fn: ast.AST, params: set[str]) -> list[tuple[ast.Call, str]]:
        """Direct calls of the `_user_*_from_update` helpers with an `update`-like
        argument inside ``fn``."""
        out = []
        for node in ast.walk(fn):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in CALLBACK_USER_HELPERS
                and node.args
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id in params
            ):
                out.append((node, node.func.id))
        return out

    @staticmethod
    def _callback_update_param(fn: ast.AST, params: set[str]) -> str | None:
        """Return the parameter used as ``<param>.callback_query`` (i.e. this is a
        callback-query handler), or None."""
        for node in ast.walk(fn):
            if (
                isinstance(node, ast.Attribute)
                and node.attr == "callback_query"
                and isinstance(node.value, ast.Name)
                and node.value.id in params
            ):
                return node.value.id
        return None

    def _check_callback_user_resolution(
        self, tree: ast.AST, path: Path, source_lines: list[str]
    ) -> List[Issue]:
        """Flag callback-query handlers that resolve the user from ``update``.

        On a callback update ``update.message`` is None and
        ``update.effective_message`` is the button message the BOT sent, so
        ``_user_id_from_update(update)`` returns the BOT's own id — exactly the
        bug that broke the message-list Preview/Edit/Duplicate buttons (and was
        found again live in ``search_page_handler``). Callback handlers must use
        ``str(update.callback_query.from_user.id)``.

        Two patterns are caught:
          A. the handler calls a helper directly;
          B. the handler passes ``update`` into an in-module helper that calls a
             helper (the old ``_lookup(update, job_id)`` shape).

        A ``# noqa`` comment on the flagged line suppresses the finding.
        """
        issues: List[Issue] = []
        funcs = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        def suppressed(line: int) -> bool:
            if 0 < line <= len(source_lines):
                return "noqa" in source_lines[line - 1]
            return False

        for fn in funcs.values():
            params = self._fn_params(fn)
            if not params:
                continue
            update_param = self._callback_update_param(fn, set(params))
            if update_param is None:
                continue

            # Rule A: direct helper call inside the callback handler.
            for call, helper in self._helper_calls(fn, set(params)):
                if suppressed(call.lineno):
                    continue
                issues.append(Issue(
                    str(path), call.lineno, "callback-user-resolution", name=helper,
                    message=(
                        f"{fn.name} resolves the user from `update` in a callback "
                        "handler — `_user_*_from_update(update)` reads "
                        "effective_message.from_user (the BOT). Use "
                        "str(update.callback_query.from_user.id)."
                    ),
                ))

            # Rule B: `update` handed to an in-module helper that resolves the user.
            for node in ast.walk(fn):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in funcs
                    and node.args
                    and isinstance(node.args[0], ast.Name)
                    and node.args[0].id == update_param
                ):
                    g = funcs[node.func.id]
                    g_params = self._fn_params(g)
                    if g_params and self._helper_calls(g, {g_params[0]}):
                        if suppressed(node.lineno):
                            continue
                        issues.append(Issue(
                            str(path), node.lineno, "callback-user-resolution", name=g.name,
                            message=(
                                f"{fn.name} passes `update` to {g.name}, which resolves "
                                "the user via `_user_*_from_update` — on a callback "
                                "update that is the BOT. Use "
                                "str(update.callback_query.from_user.id)."
                            ),
                        ))
        return issues


def analyze_paths(paths: Sequence[Path] | None = None, include_tests: bool = True) -> List[Issue]:
    root = Path(__file__).resolve().parents[1]
    if paths is None:
        paths = [root / "src", root / "scripts", root / "SetDate"]
    return StaticIssueScanner(root).scan(paths, include_tests=include_tests)


def main() -> None:
    issues = analyze_paths(include_tests=False)
    for issue in issues:
        print(issue.format())
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    print("Running static issue scan...")
    main()