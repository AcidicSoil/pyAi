"""
filepath: backend/llm/base.py
Base class for Large Language Model interactions.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class LLMInput(BaseModel):
    """Input structure for LLM calls"""

    prompt: str
    system_prompt: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None  # e.g., temp, top_p


class LLMOutput(BaseModel):
    """Output structure from LLM calls"""

    text: str
    token_usage: Optional[Dict[str, int]] = (
        None  # e.g., prompt_tokens, completion_tokens
    )
    finish_reason: Optional[str] = None


class BaseLLM(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def generate(self, input_data: LLMInput) -> LLMOutput:
        """Generate text based on the input prompt"""
        # TODO: Implement generation logic (e.g., using llama.cpp server)
        raise NotImplementedError

    @abstractmethod
    async def stream(self, input_data: LLMInput) -> AsyncIterable[LLMOutput]:
        """Stream generated text"""
        # TODO: Implement streaming logic
        raise NotImplementedError
        yield  # Required for async generator


# TODO: Implement LlamaCPPLLM subclass
# from llama_cpp import Llama
#
# class LlamaCPPLLM(BaseLLM):
#     def __init__(self, config: Dict[str, Any]):
#         super().__init__(config)
#         # Initialize llama.cpp model
#         # self.model = Llama(model_path=config.get('model_path'), ...)
#
#     async def generate(self, input_data: LLMInput) -> LLMOutput:
#         # Use self.model.create_completion
#         pass
#
#     async def stream(self, input_data: LLMInput) -> AsyncIterable[LLMOutput]:
#         # Use self.model.create_completion with stream=True
#         pass
