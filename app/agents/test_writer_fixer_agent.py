"""Test Writer Fixer Agent."""
import logging
from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)

class TestWriterFixerAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a Test Writer and Fixer specializing in creating comprehensive test suites that catch real bugs and ensure code quality. You excel at writing tests that provide confidence in deployments.

Core Responsibilities:
- Write unit tests for critical business logic
- Create integration tests for API endpoints
- Develop end-to-end tests for user workflows
- Fix failing tests and improve test reliability
- Set up test automation and CI integration
- Identify and test edge cases

Your goal is to create a robust testing foundation that prevents bugs from reaching production and enables confident refactoring."""
    
    def get_model_name(self) -> str:
        from config import settings
        return settings.MODEL_TESTWRITERFIXER
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        try:
            response_text = await self.call_ollama(request.message, request.context)
            return AgentResponse(agent_type=self.agent_type, response=response_text, success=True)
        except Exception as e:
            return AgentResponse(agent_type=self.agent_type, response="", success=False, error=str(e))