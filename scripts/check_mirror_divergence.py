"""Fail CI when deploy-tree mirrors diverge from the canonical source (M-05).

CI: python scripts/check_mirror_divergence.py

Compares sha256 hashes of the public entrypoints (bot handlers, payments,
encryption, expiry modules) between the canonical trees at the repo root
(``src/``, ``SetDate/``, ``Support Bot/``) and each deploy mirror
(``alwaysdata/``, ``local/``). Exits non-zero on any divergence or when a
mirrored entrypoint is missing, so production can never silently run
different payment/encryption/expiry behavior than the tested ``src/`` tree.
Read-only: never modifies the mirror trees.
"""

import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Canonical tree -> mirror trees (relative to ROOT).
MIRRORS = ('alwaysdata', 'local')

# Public entrypoints whose behavior must be identical everywhere. Directories
# expand to every ``*.py`` file beneath them.
ENTRYPOINTS = (
    'src/buttons.py',
    'src/register.py',
    'src/payments',
    'src/core/security.py',
    'src/core/data_encryption.py',
    'src/services/premium.py',
    'src/services/premium_expiry.py',
    'src/services/backup_manager.py',
    'src/services/token_manager.py',
    'src/scheduler/helpers.py',
    'src/handlers/export.py',
    'src/callbacks/export.py',
    'src/callbacks/bots.py',
    'src/callbacks/channels.py',
    'SetDate/bot.py',
    'Support Bot/bot.py',
)


def _iter_files(base: str):
    if os.path.isdir(base):
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in sorted(filenames):
                if name.endswith('.py'):
                    yield os.path.join(dirpath, name)
    elif os.path.isfile(base):
        yield base


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures = []
    checked = 0
    for entry in ENTRYPOINTS:
        canonical = os.path.join(ROOT, entry)
        if not os.path.exists(canonical):
            print(f"SKIP (no canonical source): {entry}")
            continue
        for rel in _iter_files(canonical):
            rel_path = os.path.relpath(rel, ROOT)
            try:
                want = _sha256(rel)
            except OSError as e:
                failures.append(f"{rel_path}: cannot hash canonical file: {e}")
                continue
            for mirror in MIRRORS:
                mirror_path = os.path.join(ROOT, mirror, rel_path)
                if not os.path.isfile(mirror_path):
                    # A missing mirror file is a divergence: the deploy tree
                    # would run without this module.
                    failures.append(f"{rel_path}: missing in {mirror}/")
                    continue
                try:
                    got = _sha256(mirror_path)
                except OSError as e:
                    failures.append(f"{rel_path}: cannot hash {mirror}/ copy: {e}")
                    continue
                checked += 1
                if got != want:
                    failures.append(f"{rel_path}: DIVERGED in {mirror}/")
    if failures:
        print(f"Mirror divergence: {len(failures)} problem(s) "
              f"({checked} file(s) compared):")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"OK: {checked} mirrored file(s) match the canonical source.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
