"""
Chat agent để xử lý các cuộc hội thoại chung.
"""
import logging

from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse


logger = logging.getLogger(__name__)


class ChatAgent(BaseAgent):
    """Agent xử lý chat thông thường."""
    
    def get_system_prompt(self) -> str:
        """System prompt cho chat agent."""
        return """Bạn là một trợ lý AI thông minh và hữu ích. 
Hãy trả lời câu hỏi của người dùng một cách chính xác, hữu ích và thân thiện.
Sử dụng tiếng Việt để trả lời trừ khi được yêu cầu khác."""
    
    def get_model_name(self) -> str:
        """Model sử dụng cho chat."""
        return "llama2"
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        """Xử lý chat request."""
        try:
            logger.info(f"Xử lý chat request: {request.message[:50]}...")
            
            response_text = await self.call_ollama(request.message, request.context)
            
            return AgentResponse(
                agent_type=self.agent_type,
                response=response_text,
                metadata={"model": self.get_model_name()},
                success=True
            )
        
        except Exception as e:
            logger.error(f"Lỗi xử lý chat: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                response="",
                success=False,
                error=str(e)
            )