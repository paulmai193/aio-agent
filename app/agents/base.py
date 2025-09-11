"""
Base class cho tất cả các agent.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from core.ollama_client import OllamaClient
from core.schemas import AgentRequest, AgentResponse, OllamaRequest

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class cho agent."""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        # Use explicit agent_type mapping for reliability
        class_name = self.__class__.__name__
        agent_type_map = {
            'AiEngineerAgent': 'aiengineer',
            'BackendArchitectAgent': 'backendarchitect', 
            'FrontendDeveloperAgent': 'frontenddeveloper',
            'RapidPrototyperAgent': 'rapidprototyper',
            'DevopsAutomatorAgent': 'devopsautomator',
            'TestWriterFixerAgent': 'testwriterfixer',
            'UiDesignerAgent': 'uidesigner',
            'ContentCreatorAgent': 'contentcreator',
            'GrowthHackerAgent': 'growthhacker',
            'TrendResearcherAgent': 'trendresearcher',
            'ProjectShipperAgent': 'projectshipper',
            'LanguageDetectorAgent': 'languagedetector',
            'BrandGuardianAgent': 'brandguardian',
            'UxResearcherAgent': 'uxresearcher',
            'VisualStorytellerAgent': 'visualstoryteller',
            'WhimsyInjectorAgent': 'whimsyinjector',
            'InstagramCuratorAgent': 'instagramcurator',
            'TiktokStrategistAgent': 'tiktokstrategist',
            'FeedbackSynthesizerAgent': 'feedbacksynthesizer',
            'TrendResearcherAgent': 'trendresearcher'
        }
        self.agent_type = agent_type_map.get(class_name, class_name.lower().replace('agent', ''))
    
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
    
    def get_standard_schema(self) -> Dict[str, Any]:
        """Lấy chuẩn JSON schema cho tất cả agent."""
        return {
            "type": "object",
            "properties": {
                "solution": {"type": "string", "description": "Detailed solution and approach"},
                "implementation": {"type": "array", "items": {"type": "string"}, "description": "Implementation steps or code examples"},
                "technologies": {"type": "array", "items": {"type": "string"}, "description": "Required technologies"},
                "considerations": {"type": "array", "items": {"type": "string"}, "description": "Important considerations"}
            },
            "required": ["solution", "implementation", "technologies", "considerations"]
        }
    
    async def call_ollama(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Gọi Ollama với prompt."""
        logger.debug(f"Agent {self.agent_type} calling Ollama with model: {self.get_model_name()}")
        
        system_prompt = self.get_system_prompt()
        format_schema = self.get_standard_schema()
        
        ollama_request = OllamaRequest(
            model=self.get_model_name(),
            system=system_prompt,
            prompt=prompt,
            format=format_schema
        )
        logger.debug(f"Ollama request: {ollama_request}")
        response = await self.ollama_client.generate(ollama_request)
        logger.debug(f"Agent {self.agent_type} received response from Ollama: {response}")
        return response.response
    
    def can_handle(self, request: AgentRequest) -> bool:
        """Kiểm tra agent có thể xử lý request không."""
        return request.agent_type == self.agent_type