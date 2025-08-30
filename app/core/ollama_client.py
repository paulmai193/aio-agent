"""
Client để tích hợp với Ollama API.
"""
import logging
from typing import Dict, Any, Optional

import aiohttp
from aiohttp import ClientTimeout

from config import settings
from core.schemas import OllamaRequest, OllamaResponse


logger = logging.getLogger(__name__)


class OllamaClient:
    """Client để giao tiếp với Ollama API."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = ClientTimeout(total=settings.OLLAMA_TIMEOUT)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Lấy hoặc tạo session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self._session
    
    async def generate(self, request: OllamaRequest) -> OllamaResponse:
        """Gửi request generate đến Ollama."""
        session = await self._get_session()
        url = f"{self.base_url}/api/generate"
        
        try:
            async with session.post(url, json=request.dict()) as response:
                response.raise_for_status()
                data = await response.json()
                return OllamaResponse(**data)
        except aiohttp.ClientError as e:
            logger.error(f"Lỗi khi gọi Ollama API: {e}")
            raise
    
    async def list_models(self) -> Dict[str, Any]:
        """Lấy danh sách models từ Ollama."""
        session = await self._get_session()
        url = f"{self.base_url}/api/tags"
        
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Lỗi khi lấy danh sách models: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Kiểm tra kết nối đến Ollama."""
        try:
            await self.list_models()
            return True
        except Exception as e:
            logger.warning(f"Ollama không khả dụng: {e}")
            return False
    
    async def close(self):
        """Đóng session."""
        if self._session and not self._session.closed:
            await self._session.close()