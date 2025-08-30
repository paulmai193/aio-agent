"""
Code agent để xử lý các yêu cầu liên quan đến code.
"""
import logging

from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse


logger = logging.getLogger(__name__)


class CodeAgent(BaseAgent):
    """Agent xử lý các yêu cầu về code."""
    
    def get_system_prompt(self) -> str:
        """System prompt cho code agent."""
        return """Bạn là một chuyên gia lập trình với kinh nghiệm sâu về nhiều ngôn ngữ.
Hãy giúp người dùng với các vấn đề về code, debug, review code, và đưa ra giải pháp tối ưu.
Luôn giải thích rõ ràng và cung cấp ví dụ cụ thể khi cần thiết.
Sử dụng tiếng Việt để giải thích trừ khi code yêu cầu comment bằng tiếng Anh."""
    
    def get_model_name(self) -> str:
        """Model sử dụng cho code."""
        return "codellama"
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        """Xử lý code request."""
        try:
            logger.info(f"Xử lý code request: {request.message[:50]}...")
            
            # Thêm context về ngôn ngữ lập trình nếu có
            enhanced_prompt = request.message
            if request.context and "language" in request.context:
                enhanced_prompt = f"[{request.context['language']}] {enhanced_prompt}"
            
            response_text = await self.call_ollama(enhanced_prompt, request.context)
            
            return AgentResponse(
                agent_type=self.agent_type,
                response=response_text,
                metadata={
                    "model": self.get_model_name(),
                    "language": request.context.get("language") if request.context else None
                },
                success=True
            )
        
        except Exception as e:
            logger.error(f"Lỗi xử lý code: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                response="",
                success=False,
                error=str(e)
            )