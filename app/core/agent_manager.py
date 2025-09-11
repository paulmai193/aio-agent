"""
Quản lý và điều phối các agent.
"""
import logging
from typing import Dict, List, Optional

from agents import (BaseAgent, AiEngineerAgent, UiDesignerAgent, ContentCreatorAgent, 
                    BackendArchitectAgent, FrontendDeveloperAgent, RapidPrototyperAgent, 
                    GrowthHackerAgent, TrendResearcherAgent, DevopsAutomatorAgent, 
                    TestWriterFixerAgent, ProjectShipperAgent, LanguageDetectorAgent, 
                    BrandGuardianAgent, UxResearcherAgent, VisualStorytellerAgent)
from core.ollama_client import OllamaClient
from core.schemas import AgentRequest, AgentResponse


logger = logging.getLogger(__name__)


class AgentManager:
    """Quản lý và điều phối các agent."""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.agents: Dict[str, BaseAgent] = {}
        self.default_agent_type = "aiengineer"
    
    async def initialize(self):
        """Khởi tạo các agent."""
        logger.info("Khởi tạo Agent Manager...")
        
        # Khởi tạo các agent có sẵn
        agents_to_init = [
            ("languagedetector", LanguageDetectorAgent), ("aiengineer", AiEngineerAgent), 
            ("uidesigner", UiDesignerAgent), ("contentcreator", ContentCreatorAgent), 
            ("backendarchitect", BackendArchitectAgent), ("frontenddeveloper", FrontendDeveloperAgent), 
            ("rapidprototyper", RapidPrototyperAgent), ("growthhacker", GrowthHackerAgent), 
            ("trendresearcher", TrendResearcherAgent), ("devopsautomator", DevopsAutomatorAgent), 
            ("testwriterfixer", TestWriterFixerAgent), ("projectshipper", ProjectShipperAgent), 
            ("brandguardian", BrandGuardianAgent), ("uxresearcher", UxResearcherAgent), 
            ("visualstoryteller", VisualStorytellerAgent)
        ]
        
        for agent_name, agent_class in agents_to_init:
            logger.debug(f"Initializing agent: {agent_name}")
            self.agents[agent_name] = agent_class(self.ollama_client)
        
        logger.info(f"Đã khởi tạo {len(self.agents)} agents: {list(self.agents.keys())}")
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Xử lý request và route đến agent phù hợp."""
        agent_type = request.agent_type or self.default_agent_type
        logger.debug(f"Processing request for agent: {agent_type}, message length: {len(request.message)}")
        
        # Tìm agent phù hợp
        agent = self.get_agent(agent_type)
        if not agent:
            logger.error(f"Agent not found: {agent_type}")
            return AgentResponse(
                agent_type=agent_type,
                response="",
                success=False,
                error=f"Không tìm thấy agent: {agent_type}"
            )
        
        logger.info(f"Routing request đến agent: {agent_type}")
        try:
            response = await agent.process(request)
            logger.debug(f"Agent {agent_type} response: success={response.success}, response_length={len(response.response)}")
            return response
        except Exception as e:
            logger.error(f"Agent {agent_type} processing failed: {e}")
            return AgentResponse(
                agent_type=agent_type,
                response="",
                success=False,
                error=f"Agent processing error: {str(e)}"
            )
    
    def get_agent(self, agent_type: str) -> Optional[BaseAgent]:
        """Lấy agent theo type."""
        return self.agents.get(agent_type)
    
    def list_agents(self) -> List[str]:
        """Lấy danh sách các agent có sẵn."""
        return list(self.agents.keys())
    
    def register_agent(self, agent: BaseAgent):
        """Đăng ký agent mới."""
        self.agents[agent.agent_type] = agent
        logger.info(f"Đã đăng ký agent: {agent.agent_type}")
    
    async def health_check(self) -> Dict[str, any]:
        """Kiểm tra trạng thái của manager."""
        logger.debug("Performing health check")
        ollama_status = await self.ollama_client.health_check()
        
        health_data = {
            "agents_loaded": len(self.agents),
            "agent_types": list(self.agents.keys()),
            "ollama_connected": ollama_status
        }
        logger.debug(f"Health check result: {health_data}")
        return health_data
    
    async def cleanup(self):
        """Dọn dẹp resources."""
        logger.info("Dọn dẹp Agent Manager...")
        try:
            await self.ollama_client.close()
        except Exception as e:
            logger.error(f"Error closing ollama client: {e}")