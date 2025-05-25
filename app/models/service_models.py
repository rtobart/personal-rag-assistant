from abc import ABC, abstractmethod

from app.models.agent_models import InputModel


class AnswerService(ABC):

    @abstractmethod
    def ainvoke(self, input_data: InputModel) -> str:
        pass
