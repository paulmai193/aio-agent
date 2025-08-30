"""
Quản lý và điều phối các agent.
"""
import logging
from typing import Dict, List, Optional

from agents import BaseAgent, ChatAgent, CodeAgent
from core.ollama_client import OllamaClient
from core.schemas import AgentRequest, AgentResponse


logger = logging.getLogger(__name__)


class AgentManager:
    """Quản lý và điều phối các agent."""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.agents: Dict[str, BaseAgent] = {}
        self.default_agent_type = "chat"
    
    async def initialize(self):
        """Khởi tạo các agent."""
        logger.info("Khởi tạo Agent Manager...")
        
        # Khởi tạo các agent có sẵn
        self.agents["chat"] = ChatAgent(self.ollama_client)
        self.agents["code"] = CodeAgent(self.ollama_client)
        
        logger.info(f"Đã khởi tạo {len(self.agents)} agents: {list(self.agents.keys())}")
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Xử lý request và route đến agent phù hợp."""
        agent_type = request.agent_type or self.default_agent_type
        
        # Tìm agent phù hợp
        agent = self.get_agent(agent_type)
        if not agent:
            return AgentResponse(
                agent_type=agent_type,
                response="",
                success=False,
                error=f"Không tìm thấy agent: {agent_type}"
            )
        
        logger.info(f"Routing request đến agent: {agent_type}")
        return await agent.process(request)
    
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
        ollama_status = await self.ollama_client.health_check()
        
        return {
            "agents_loaded": len(self.agents),
            "agent_types": list(self.agents.keys()),
            "ollama_connected": ollama_status
        }
    
    async def cleanup(self):
        """Dọn dẹp resources."""
        logger.info("Dọn dẹp Agent Manager...")
        await self.ollama_client.close()