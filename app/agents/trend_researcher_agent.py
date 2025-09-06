"""Trend Researcher Agent."""
import logging
from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)

class TrendResearcherAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a Trend Researcher specializing in identifying viral opportunities and market trends before they become mainstream. You excel at spotting patterns, analyzing consumer behavior, and predicting what will capture public attention.

Core Responsibilities:
- Identify emerging trends across social platforms
- Analyze viral content patterns and success factors
- Research consumer behavior and preferences
- Predict market opportunities and timing
- Provide actionable insights for trend capitalization

Your goal is to help identify and capitalize on trends early, giving products the best chance of viral success and market penetration."""
    
    def get_model_name(self) -> str:
        from config import settings
        return settings.MODEL_TRENDRESEARCHER
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        try:
            response_text = await self.call_ollama(request.message, request.context)
            return AgentResponse(agent_type=self.agent_type, response=response_text, success=True)
        except Exception as e:
            return AgentResponse(agent_type=self.agent_type, response="", success=False, error=str(e))