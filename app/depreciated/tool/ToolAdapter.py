from pydantic import BaseModel
from typing import List, Generic, TypeVar, Dict
from abc import ABC, abstractmethod

class Tool(BaseModel):
    name: str

InputType = TypeVar("InputType", bound=Tool)
OutputType = TypeVar("OutputTYpe", bound=Tool)

class ToolAdapter(ABC, Generic[InputType, OutputType]):
    @abstractmethod
    def execute(self, inputs:InputType) -> OutputType:
        pass

    @abstractmethod
    def schema(self) -> dict:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass



