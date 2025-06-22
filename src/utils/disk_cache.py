import pickle
from pathlib import Path

_CACHE_DIR = Path(__file__).resolve().parent / "resources" / "cache"


def _ensure_cache_dir() -> None:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)

def set_disk_cache(key: str, obj) -> None:
    _ensure_cache_dir()
    file_path = _CACHE_DIR / key
    with file_path.open("wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_disk_cache(key: str):
    file_path = _CACHE_DIR / key
    if file_path.exists():
        with file_path.open("rb") as f:
            return pickle.load(f)
    return None
