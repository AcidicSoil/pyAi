"""
filepath: backend/agents/base.py
Base agent class that defines the interface for all agents in the system.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from ..integrations import BaseIntegration, IntegrationToolInput, IntegrationToolOutput
from ..llm import BaseLLM, LLMInput
from ..memory import BaseMemory, MemoryRecord
from ..utils import logger


class AgentInput(BaseModel):
    """Input model for agent tasks"""

    prompt: str
    parameters: Optional[Dict[str, Any]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Research the latest developments in LLMs",
                    "parameters": {"max_sources": 5, "min_confidence": 0.8},
                }
            ]
        }
    }

    @validator("parameters")
    def validate_parameters(cls, v):
        # TODO: Add more sophisticated parameter validation based on agent capabilities
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError("Parameters must be a dictionary")
        return v


class AgentOutput(BaseModel):
    """Output model for agent results"""

    answer: str
    sources: List[str] = []
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    execution_time: float = Field(default=0.0, ge=0.0)
    reflection_notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "Based on research...",
                    "sources": ["https://example.com/1"],
                    "confidence": 0.85,
                    "execution_time": 1.2,
                    "reflection_notes": "Task completed successfully with high confidence",
                }
            ]
        }
    }


class BaseAgent:
    """Base agent class that all specialized agents should inherit from"""

    def __init__(
        self,
        name: str,
        description: str = "",
        capabilities: List[str] = [],
        config: Dict[str, Any] = {},
    ):
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.config = config
        self.id = f"{name.lower().replace(' ', '-')}"
        self._task_history: List[AgentOutput] = []

        # Add LLM and Memory instances
        self.llm: Optional[BaseLLM] = None
        self.memory: Optional[BaseMemory] = None

    def set_llm(self, llm_instance: BaseLLM):
        self.llm = llm_instance

    def set_memory(self, memory_instance: BaseMemory):
        self.memory = memory_instance

    async def run(self, input_data: AgentInput) -> AgentOutput:
        """
        Run the agent with the given input

        Parameters:
            input_data: AgentInput - The input data for the agent task

        Returns:
            AgentOutput - The result of the agent's execution
        """
        # TODO: Implement the run method in subclasses
        raise NotImplementedError("Subclasses must implement run()")

    async def stop(self) -> bool:
        """
        Stop a running agent task

        Returns:
            bool - True if successfully stopped, False otherwise
        """
        # TODO: Implement the stop method using task ID tracking (e.g., Prefect flow run ID)
        print(f"Attempting to stop agent {self.id}...")
        return True

    async def reflect(self, result: AgentOutput) -> str:
        """
        Reflect on the agent's output and suggest improvements

        Parameters:
            result: AgentOutput - The output to reflect on

        Returns:
            str - Reflection notes
        """
        reflection_points = []

        # Analyze confidence
        if result.confidence < 0.7:
            reflection_points.append(
                "Low confidence score - consider gathering more sources or refining the search"
            )

        # Check execution time
        if result.execution_time > 5.0:
            reflection_points.append(
                "Task took longer than expected - may need optimization"
            )

        # Evaluate source quality
        if len(result.sources) < 2:
            reflection_points.append(
                "Limited number of sources - consider broadening the search"
            )

        # Check answer quality
        if len(result.answer.split()) < 50:
            reflection_points.append(
                "Answer may be too brief - consider providing more detail"
            )

        # Add to task history
        self._task_history.append(result)

        if not reflection_points:
            return "Task completed successfully with no significant issues"

        return " | ".join(reflection_points)


# Example specialized agent stub
class ResearchAgent(BaseAgent):
    """Agent specialized for web research and summarization"""

    def __init__(
        self,
        name: str = "Research Agent",
        config: Dict[str, Any] = {},
        llm: Optional[BaseLLM] = None,
        memory: Optional[BaseMemory] = None,
    ):
        super().__init__(
            name=name,
            description="Performs web research and summarizes findings",
            capabilities=["web_search", "document_summarization", "citation"],
            config=config,
        )
        if llm:
            self.set_llm(llm)
        if memory:
            self.set_memory(memory)

    async def run(self, input_data: AgentInput) -> AgentOutput:
        """Run research task using memory, tools, and LLM"""

        if not self.llm:
            raise RuntimeError("ResearchAgent requires an LLM instance.")
        if not self.memory:
            raise RuntimeError("ResearchAgent requires a Memory instance.")

        start_time = time.time()
        prompt = input_data.prompt
        max_sources = (
            input_data.parameters.get("max_sources", 3) if input_data.parameters else 3
        )

        # 1. Search Memory
        try:
            memory_results = await self.memory.search(
                query=prompt, top_k=max_sources, filter={"agent_id": self.id}
            )
            logger.info(f"Found {len(memory_results)} relevant records in memory.")
            context = "\n".join([r.content for r in memory_results])
        except Exception as e:
            logger.error(f"Error searching memory: {e}")
            memory_results = []
            context = ""

        # 2. (Placeholder) Use Web Search Tool if memory is insufficient
        sources = [
            r.metadata.get("source", "")
            for r in memory_results
            if r.metadata.get("source")
        ]
        if len(memory_results) < max_sources:
            logger.info("Memory insufficient, performing web search (placeholder)...")
            # TODO: Implement actual web search tool integration
            # Assume web_search_tool is an instance of BaseIntegration providing 'search'
            # web_search_result = await self.run_integration_tool('web_search', {'query': prompt, 'num_results': max_sources - len(memory_results)})
            # if web_search_result.success:
            #     context += "\n" + "\n".join(web_search_result.result['snippets'])
            #     sources.extend(web_search_result.result['urls'])
            # For now, add dummy web results
            dummy_web_context = f"Web search placeholder for '{prompt}'. Found relevant info at example.com."
            context += "\n" + dummy_web_context
            sources.append("https://placeholder.example.com")

        # 3. Synthesize Answer using LLM
        llm_prompt = f"Based on the following context, please answer the question: {prompt}\n\nContext:\n{context}"
        llm_input = LLMInput(prompt=llm_prompt)

        try:
            llm_output = await self.llm.generate(llm_input)
            answer = llm_output.text
            confidence = 0.8  # TODO: Estimate confidence based on LLM output/sources
        except Exception as e:
            logger.error(f"Error generating response with LLM: {e}")
            answer = "Error: Could not generate response."
            confidence = 0.1

        # 4. Format Output and Store in Memory
        execution_time = time.time() - start_time
        final_output = AgentOutput(
            answer=answer,
            sources=list(set(sources)),  # Deduplicate sources
            confidence=confidence,
            execution_time=execution_time,
        )

        # Store the result in memory
        try:
            memory_record = MemoryRecord(
                id=f"task_{int(start_time)}_{self.id}",  # Example ID
                content=f"Prompt: {prompt}\nAnswer: {answer}",
                metadata={"source_urls": sources, "confidence": confidence},
                agent_id=self.id,
            )
            await self.memory.add(memory_record)
            logger.info(f"Stored result for task '{prompt}' in memory.")
        except Exception as e:
            logger.error(f"Error storing result in memory: {e}")

        # Add reflection
        final_output.reflection_notes = await self.reflect(final_output)
        return final_output

    # Helper placeholder for running integration tools (to be implemented properly)
    async def run_integration_tool(
        self, tool_name: str, params: Dict[str, Any]
    ) -> IntegrationToolOutput:
        # TODO: Implement actual logic to find and run integration tools
        logger.warning(
            f"Placeholder: Running integration tool '{tool_name}' with params {params}"
        )
        # Return dummy success for now
        return IntegrationToolOutput(
            result={
                "snippets": ["Dummy snippet 1"],
                "urls": ["https://dummy.example.com"],
            },
            success=True,
        )

    async def reflect(self, result: AgentOutput) -> str:
        """Reflect on research quality"""
        reflection = await super().reflect(result)

        # Add research-specific reflection
        research_points = []

        # Check source diversity
        unique_domains = {source.split("/")[2] for source in result.sources}
        if len(unique_domains) < 2:
            research_points.append(
                "Sources are from limited domains - diversify research"
            )

        # Check for academic sources
        academic_sources = [s for s in result.sources if ".edu" in s or ".ac." in s]
        if not academic_sources:
            research_points.append(
                "No academic sources found - consider including scholarly references"
            )

        if research_points:
            reflection += " | " + " | ".join(research_points)

        return reflection
