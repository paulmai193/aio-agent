"""
Base class cho tất cả các agent.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from core.ollama_client import OllamaClient
from core.schemas import AgentRequest, AgentResponse, OllamaRequest


class BaseAgent(ABC):
    """Base class cho agent."""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.agent_type = self.__class__.__name__.lower().replace('agent', '')
    
    @abstractmethod
    async def process(self, request: AgentRequest) -> AgentResponse:
        """Xử lý request từ user."""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Lấy system prompt cho agent."""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Lấy tên model Ollama sử dụng."""
        pass
    
    async def call_ollama(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gọi Ollama với prompt."""
        system_prompt = self.get_system_prompt()
        full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        ollama_request = OllamaRequest(
            model=self.get_model_name(),
            prompt=full_prompt
        )
        
        response = await self.ollama_client.generate(ollama_request)
        return response.response
    
    def can_handle(self, request: AgentRequest) -> bool:
        """Kiểm tra agent có thể xử lý request không."""
        return request.agent_type == self.agent_type