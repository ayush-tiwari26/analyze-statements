from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class DummyParser:
    """
    Tiny stand-in for the real Parser hierarchy.

    It expects to receive dicts shaped exactly like whatever your
    VanillaExtractor calls `self.parser.get_content()`.
    """
    def __init__(self, data):
        self._data = data

    def get_content(self):
        return self._data
