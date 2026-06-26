import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_store import assert_phase1_static, content_inventory, validate_content


def main():
    assert_phase1_static()
    errors = validate_content()
    inv = content_inventory()
    print(f"Content inventory: {inv['guides']} guides, {inv['components']} components, "
          f"{inv['projects']} projects, {inv['pages']} pages")
    if errors:
        print("\nValidation errors:")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("Content validation passed.")


if __name__ == "__main__":
    main()
