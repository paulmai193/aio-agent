"""Unit tests for LanguageDetectorAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.language_detector_agent import LanguageDetectorAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def language_agent(mock_ollama_client):
    """LanguageDetectorAgent instance."""
    return LanguageDetectorAgent(mock_ollama_client)


@pytest.mark.asyncio
async def test_process_vietnamese_text(language_agent):
    """Test processing Vietnamese text."""
    with patch.object(language_agent, 'call_ollama', return_value="vi"):
        request = AgentRequest(agent_type="languagedetector", message="Xin chào, tôi cần giúp đỡ")
        response = await language_agent.process(request)
        
        assert response.success is True
        assert response.response == "vi"
        assert response.agent_type == "languagedetector"


@pytest.mark.asyncio
async def test_process_english_text(language_agent):
    """Test processing English text."""
    with patch.object(language_agent, 'call_ollama', return_value="en"):
        request = AgentRequest(agent_type="languagedetector", message="Hello, I need help")
        response = await language_agent.process(request)
        
        assert response.success is True
        assert response.response == "en"


@pytest.mark.asyncio
async def test_process_chinese_text(language_agent):
    """Test processing Chinese text."""
    with patch.object(language_agent, 'call_ollama', return_value="zh"):
        request = AgentRequest(agent_type="languagedetector", message="你好，我需要帮助")
        response = await language_agent.process(request)
        
        assert response.success is True
        assert response.response == "zh"


@pytest.mark.asyncio
async def test_process_exception(language_agent):
    """Test processing with exception."""
    with patch.object(language_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="languagedetector", message="Test message")
        response = await language_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_get_system_prompt(language_agent):
    """Test system prompt generation."""
    prompt = language_agent.get_system_prompt()
    assert "language detection expert" in prompt.lower()
    assert "vi" in prompt
    assert "en" in prompt
    assert "only the 2-letter language code" in prompt.lower()


def test_get_model_name(language_agent):
    """Test model name retrieval."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_LANGUAGEDETECTOR = "test-model"
        model = language_agent.get_model_name()
        assert model == "test-model"


@pytest.mark.asyncio
async def test_process_with_whitespace(language_agent):
    """Test processing with extra whitespace."""
    with patch.object(language_agent, 'call_ollama', return_value="  vi  \n"):
        request = AgentRequest(agent_type="languagedetector", message="Xin chào")
        response = await language_agent.process(request)
        
        assert response.success is True
        assert response.response == "vi"  # Should be stripped


@pytest.mark.asyncio
async def test_process_empty_response(language_agent):
    """Test processing with empty response."""
    with patch.object(language_agent, 'call_ollama', return_value=""):
        request = AgentRequest(agent_type="languagedetector", message="Test")
        response = await language_agent.process(request)
        
        assert response.success is True
        assert response.response == ""