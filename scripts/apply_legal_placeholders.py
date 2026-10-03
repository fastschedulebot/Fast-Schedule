"""Read legal_values.json and replace all [[PLACEHOLDER]] markers in legal docs."""
import json
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "legal_values.json")

FILES = [
    "docs/terms.md",
    "docs/privacy.md",
    "docs/refundpolicy.md",
    "website/legal/terms.html",
    "website/legal/privacy.html",
    "website/legal/refundpolicy.html",
]

PLACEHOLDER_MAP = {
    "date": "DATE",
    "operator_legal_name": "OPERATOR LEGAL NAME",
    "website": "WEBSITE",
    "support_telegram": "SUPPORT TELEGRAM HANDLE or LINK",
    "privacy_contact_email": "PRIVACY CONTACT EMAIL",
    "legal_contact_email": "LEGAL CONTACT EMAIL",
    "contact_email": "CONTACT EMAIL",
    "operator_address": "OPERATOR REGISTERED ADDRESS",
    "company_registration_number": "COMPANY REGISTRATION NUMBER",
    "governing_jurisdiction": "GOVERNING JURISDICTION",
    "jurisdiction_venue": "JURISDICTION VENUE",
    "response_window": "RESPONSE_WINDOW, e.g. 5 business days",
    "refund_processing_window": "e.g. 5\u201310 business days",
    "discretionary_refund_window": "e.g. 7 business days",
}


def main():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: {CONFIG_PATH} not found. Create it first.")
        return 1

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    replacements = {}
    for cfg_key, placeholder_name in PLACEHOLDER_MAP.items():
        value = config.get(cfg_key)
        if value is None:
            print(f"Warning: '{cfg_key}' not found in config, skipping [[{placeholder_name}]]")
            continue
        placeholder = f"[[{placeholder_name}]]"
        if placeholder not in replacements:
            replacements[placeholder] = value
        else:
            old = replacements[placeholder]
            if old != value:
                print(f"Warning: conflicting values for {placeholder}: '{old}' vs '{value}', using '{value}'")
                replacements[placeholder] = value

    total_changes = 0
    for rel_path in FILES:
        abs_path = os.path.join(PROJECT_ROOT, rel_path)
        if not os.path.exists(abs_path):
            print(f"Skipping (not found): {rel_path}")
            continue

        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        changed = content
        for placeholder, value in replacements.items():
            changed = changed.replace(placeholder, str(value))

        count = (len(changed) != len(content))
        if count:
            total_changes += 1
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(changed)
            print(f"Updated: {rel_path}")
        else:
            print(f"No changes: {rel_path}")

    print(f"\nDone. {total_changes} file(s) updated.")
    return 0


if __name__ == "__main__":
    exit(main())
