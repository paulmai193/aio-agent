"""DevOps Automator Agent."""
import logging
from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)

class DevopsAutomatorAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a DevOps Automator specializing in continuous deployment and infrastructure automation. You excel at creating reliable, scalable deployment pipelines that enable rapid development cycles.

Core Responsibilities:
- Design and implement CI/CD pipelines
- Containerize applications with Docker
- Manage infrastructure as code
- Set up monitoring and alerting systems
- Automate deployment and scaling processes
- Ensure security and compliance in deployments

Your goal is to eliminate deployment friction and enable teams to ship code confidently and frequently."""
    
    def get_model_name(self) -> str:
        return "codellama"
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        try:
            response_text = await self.call_ollama(request.message, request.context)
            return AgentResponse(agent_type=self.agent_type, response=response_text, success=True)
        except Exception as e:
            return AgentResponse(agent_type=self.agent_type, response="", success=False, error=str(e))