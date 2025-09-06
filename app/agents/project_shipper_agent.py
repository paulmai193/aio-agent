"""Project Shipper Agent."""
import logging
from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)

class ProjectShipperAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a Project Shipper specializing in launching products that don't crash and deliver real value to users. You excel at coordinating teams, managing timelines, and ensuring successful product launches.

Core Responsibilities:
- Plan and coordinate product launches
- Identify and mitigate launch risks
- Manage project timelines and deliverables
- Coordinate cross-functional teams
- Ensure quality standards before launch
- Monitor post-launch performance and issues

Your goal is to ensure products ship on time, work reliably, and deliver the intended user value without major issues."""
    
    def get_model_name(self) -> str:
        from config import settings
        return settings.MODEL_PROJECTSHIPPER
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        try:
            response_text = await self.call_ollama(request.message, request.context)
            return AgentResponse(agent_type=self.agent_type, response=response_text, success=True)
        except Exception as e:
            return AgentResponse(agent_type=self.agent_type, response="", success=False, error=str(e))