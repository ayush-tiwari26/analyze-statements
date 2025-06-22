from abc import ABC, abstractmethod
from typing import List, Dict
from src.parsers.Parser import Parser


class Validator(ABC):
    @abstractmethod
    def validate(self) -> Dict[str, bool]:
        pass

    @abstractmethod
    def get_discrepancy(self) -> Dict[str, str]:
        pass
