"""
filepath: backend/llm/llama_cpp.py
Implementation of the BaseLLM interface using llama-cpp-python.
"""

import logging
from typing import Any, AsyncIterable, Dict, Optional

from llama_cpp import Llama

from .base import BaseLLM, LLMInput, LLMOutput

logger = logging.getLogger(__name__)


class LlamaCPPLLM(BaseLLM):
    """LLM provider using llama.cpp"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model_path = config.get("model_path")
        if not self.model_path:
            raise ValueError("model_path must be specified in LLM config")

        self.model_params = config.get("model_params", {})
        self.generate_params = config.get("generate_params", {})

        # Default Vulkan/GPU settings if not specified
        self.model_params.setdefault(
            "n_gpu_layers", -1
        )  # Use GPU for all layers by default
        self.model_params.setdefault("verbose", False)  # Adjust verbosity as needed

        try:
            self.model = Llama(model_path=self.model_path, **self.model_params)
            logger.info(f"Initialized Llama model from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to initialize Llama model: {e}")
            raise

    async def generate(self, input_data: LLMInput) -> LLMOutput:
        """Generate text using the loaded llama.cpp model"""
        if not self.model:
            raise RuntimeError("Llama model is not initialized")

        prompt = self._format_prompt(input_data.prompt, input_data.system_prompt)

        params = {**self.generate_params, **(input_data.parameters or {})}
        params.setdefault("max_tokens", 512)  # Default max tokens

        try:
            completion = self.model.create_completion(
                prompt=prompt, stream=False, **params
            )

            text = completion["choices"][0]["text"]
            usage = completion.get("usage", {})
            finish_reason = completion["choices"][0].get("finish_reason")

            return LLMOutput(
                text=text.strip(), token_usage=usage, finish_reason=finish_reason
            )
        except Exception as e:
            logger.error(f"Error during Llama generation: {e}")
            # Reraise or return an error LLMOutput
            raise

    async def stream(self, input_data: LLMInput) -> AsyncIterable[LLMOutput]:
        """Stream generated text using the loaded llama.cpp model"""
        if not self.model:
            raise RuntimeError("Llama model is not initialized")

        prompt = self._format_prompt(input_data.prompt, input_data.system_prompt)
        params = {**self.generate_params, **(input_data.parameters or {})}
        params.setdefault("max_tokens", 512)

        try:
            stream = self.model.create_completion(prompt=prompt, stream=True, **params)

            collected_text = ""
            for chunk in stream:
                delta = chunk["choices"][0]["text"]
                collected_text += delta
                yield LLMOutput(text=delta)  # Yield delta chunk

            # Optionally yield a final message with full text and usage (if needed)
            # logger.info("Stream finished")

        except Exception as e:
            logger.error(f"Error during Llama streaming: {e}")
            raise

    def _format_prompt(
        self, user_prompt: str, system_prompt: Optional[str] = None
    ) -> str:
        """Formats the prompt based on whether a system prompt is provided."""
        if system_prompt:
            # Basic system prompt format, adjust based on model requirements
            return f"<|system|>{system_prompt}<|end|><|user|>{user_prompt}<|end|><|assistant|>"
        else:
            return user_prompt
