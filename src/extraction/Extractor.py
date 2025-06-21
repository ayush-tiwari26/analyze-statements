from abc import ABC, abstractmethod
from typing import List, Dict
from src.parsers.Parser import Parser


class Extractor(ABC):
    @abstractmethod
    def parse_data(self) -> List[str]:
        pass

    @abstractmethod
    def extract_data(self, content: str) -> Dict:
        pass
