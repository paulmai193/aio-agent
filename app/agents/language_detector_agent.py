"""
Language Detector Agent - Chuyên gia phát hiện ngôn ngữ văn bản.
"""
import logging
import json
from typing import Dict, Any, Optional

from agents.base import BaseAgent
from core.schemas import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)


class LanguageDetectorAgent(BaseAgent):
    """Agent chuyên phát hiện ngôn ngữ của văn bản."""
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        """Xử lý request phát hiện ngôn ngữ."""
        try:
            logger.debug(f"Language detection for: {request.message[:50]}...")
            
            # Gọi LLM để phát hiện ngôn ngữ
            response = await self.call_ollama(request.message, request.context)
            
            # Parse JSON response and extract language
            response_json = json.loads(response)
            language_code = response_json.get("language", "en")
            
            return AgentResponse(
                agent_type=self.agent_type,
                response=language_code,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                response="en",
                success=False,
                error=str(e)
            )
    
    def get_system_prompt(self) -> str:
        """Lấy system prompt cho language detection."""
        return """You are a language detection expert. Your only task is to identify the language of the given text.

Analyze the input text and respond with ONLY the language code in this exact format:
- "vi" for Vietnamese
- "en" for English  
- "zh" for Chinese
- "ja" for Japanese
- "ko" for Korean
- "fr" for French
- "de" for German
- "es" for Spanish
- "it" for Italian
- "pt" for Portuguese
- "ru" for Russian
- "ar" for Arabic
- "hi" for Hindi
- "th" for Thai
- "id" for Indonesian
- "ms" for Malay

Rules:
1. Respond with ONLY the 2-letter language code
2. No explanations, no additional text
3. If uncertain, default to "en"
4. Focus on the primary language of the text

Examples:
Input: "Xin chào, tôi cần giúp đỡ"
Output: vi

Input: "Hello, I need help"
Output: en

Input: "你好，我需要帮助"
Output: zh"""
    
    def get_model_name(self) -> str:
        """Lấy tên model Ollama sử dụng."""
        from config import settings
        return settings.MODEL_LANGUAGEDETECTOR
    
    def get_standard_schema(self) -> Dict[str, Any]:
        """Override schema cho language detection."""
        return {
            "type": "object",
            "properties": {
                "language": {"type": "string"}
            },
            "required": ["language"]
        }