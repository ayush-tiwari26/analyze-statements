from abc import ABC, abstractmethod
from typing import List, Any, Dict


class Parser(ABC):
    @abstractmethod
    def get_files(self) -> List[Any]:
        pass

    @abstractmethod
    def get_content(self) -> Dict[str, str]:
        pass
