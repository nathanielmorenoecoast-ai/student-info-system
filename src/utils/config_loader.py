"""Configuration management: load settings from an external JSON file."""
import json
import os

# Used if config.json is missing or incomplete (keeps the app resilient).
DEFAULTS = {
    "data_file": "data/students.json",
    "export_file": "data/students_export.csv",
    "log_file": "logs/app.log",
    "log_level": "INFO",
    "app_name": "Student Information System",
}


def load_config(path="config/config.json"):
    """Return configuration merged over defaults.

    Environment variable SIS_DATA_FILE overrides the data file path, which
    is handy for cloud deployments where paths differ per environment.
    """
    config = dict(DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        print(f"Config file '{path}' not found. Using defaults.")
    except json.JSONDecodeError as exc:
        print(f"Config file is invalid JSON ({exc}). Using defaults.")

    config["data_file"] = os.environ.get("SIS_DATA_FILE", config["data_file"])
    return config
