import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cms_loader import PROJECTS_DIR, load_yaml, save_yaml
from rebuild_parents import load_hardware_from_archive


def archive_hardware(parent: dict) -> dict:
    return load_hardware_from_archive(parent)


def main():
    updated = 0
    for path in sorted(PROJECTS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue
        hw = archive_hardware(data)
        wiring = [{"component": comp, "pin": pin} for comp, pin in hw.get("wiring", [])]
        data["hardware"] = {
            "sensor_pin": hw.get("sensor_pin", "GPIO34"),
            "output_pin": hw.get("output_pin", "GPIO26"),
            "sensor_name": hw.get("sensor_name") or data.get("sensor", "Sensor"),
            "output_name": hw.get("output_name") or data.get("output", "Output"),
            "wiring": wiring,
        }
        data.pop("levels", None)
        save_yaml(path, data)
        updated += 1
        print(f"Updated {path.name} ({len(wiring)} wiring rows)")
    print(f"Exported hardware for {updated} project YAML files.")


if __name__ == "__main__":
    main()
