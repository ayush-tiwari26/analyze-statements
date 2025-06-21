from abc import ABC, abstractmethod
from typing import List, Any


class Parser(ABC):
    @abstractmethod
    def get_files(self, input: str) -> List[Any]:
        pass

    @abstractmethod
    def get_content(self, obj: Any) -> str:
        pass