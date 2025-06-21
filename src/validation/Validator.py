from abc import ABC, abstractmethod
from typing import List, Dict
from src.parsers.Parser import Parser


class Validator(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, str]) -> bool:
        pass

    @abstractmethod
    def extract_data(self, content: str) -> Dict:
        pass
