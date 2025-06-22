import json
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_configs() -> dict:
    # Get the current file's path and go two levels up
    base_dir = Path(__file__).resolve().parents[2]
    config_path = base_dir / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(f"config.json not found at {config_path}")

    with open(config_path, "r") as f:
        return json.load(f)