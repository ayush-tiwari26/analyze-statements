from abc import ABC, abstractmethod
from typing import List, Dict
from src.parsers.Parser import Parser


class Extractor(ABC):
    @abstractmethod
    def extract(self) -> Dict[str, Dict]:
        pass

    @abstractmethod
    def extract_single(self, content: str) -> Dict:
        pass
