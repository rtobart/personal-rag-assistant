from abc import ABC, abstractmethod
from typing import List


class aiModel(ABC):

    @abstractmethod
    def run_prompt(self, text: str) -> str:
        pass
