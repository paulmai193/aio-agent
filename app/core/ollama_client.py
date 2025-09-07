"""
Client để tích hợp với Ollama API.
"""
import asyncio
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
        self.timeout = ClientTimeout(total=settings.OLLAMA_TIMEOUT, connect=30)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Lấy hoặc tạo session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self._session
    
    async def generate(self, request: OllamaRequest) -> OllamaResponse:
        """Gửi request generate đến Ollama."""
        logger.debug(f"Generating with model: {request.model}, prompt length: {len(request.prompt)}")
        session = await self._get_session()
        url = f"{self.base_url}/api/generate"
        
        try:
            async with session.post(url, json=request.dict(), timeout=self.timeout) as response:
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"Ollama response received, length: {len(data.get('response', ''))}")
                return OllamaResponse(**data)
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error(f"Lỗi khi gọi Ollama API: {e}")
            raise
    
    async def list_models(self) -> Dict[str, Any]:
        """Lấy danh sách models từ Ollama."""
        logger.debug("Fetching models list from Ollama")
        session = await self._get_session()
        url = f"{self.base_url}/api/tags"
        
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"Found {len(data.get('models', []))} models")
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Lỗi khi lấy danh sách models: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Kiểm tra kết nối đến Ollama."""
        logger.debug("Checking Ollama health")
        session = await self._get_session()
        url = f"{self.base_url}/api/version"
        
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                response.raise_for_status()
                logger.debug("Ollama health check passed")
                return True
        except Exception as e:
            logger.warning(f"Ollama không khả dụng: {e}")
            return False
    
    async def close(self):
        """Đóng session."""
        if self._session and not self._session.closed:
            await self._session.close()