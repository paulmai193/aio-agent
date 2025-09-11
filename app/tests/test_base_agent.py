"""Unit tests for BaseAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock
from agents.base import BaseAgent
from core.schemas import AgentRequest, OllamaRequest, OllamaResponse


class MockTestAgent(BaseAgent):
    """Test implementation of BaseAgent."""
    
    async def process(self, request):
        return f"Processed: {request.message}"
    
    def get_system_prompt(self):
        return "Test system prompt"
    
    def get_model_name(self):
        return "test-model"


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    client.generate = AsyncMock(return_value=OllamaResponse(
        model="test-model",
        response="Test response",
        done=True
    ))
    return client


@pytest.fixture
def test_agent(mock_ollama_client):
    """Test agent instance."""
    return MockTestAgent(mock_ollama_client)


def test_agent_type_mapping():
    """Test agent type mapping for known classes."""
    mock_client = MagicMock()
    
    # Test known agent types
    from agents.ai_engineer_agent import AiEngineerAgent
    from agents.language_detector_agent import LanguageDetectorAgent
    from agents.brand_guardian_agent import BrandGuardianAgent
    
    ai_agent = AiEngineerAgent(mock_client)
    assert ai_agent.agent_type == "aiengineer"
    
    lang_agent = LanguageDetectorAgent(mock_client)
    assert lang_agent.agent_type == "languagedetector"
    
    brand_agent = BrandGuardianAgent(mock_client)
    assert brand_agent.agent_type == "brandguardian"


def test_agent_type_fallback():
    """Test agent type fallback for unknown classes."""
    mock_client = MagicMock()
    
    class UnknownAgent(BaseAgent):
        async def process(self, request):
            pass
        def get_system_prompt(self):
            return "test"
        def get_model_name(self):
            return "test"
    
    agent = UnknownAgent(mock_client)
    assert agent.agent_type == "unknown"


@pytest.mark.asyncio
async def test_call_ollama_success(test_agent, mock_ollama_client):
    """Test successful Ollama call."""
    result = await test_agent.call_ollama("Test prompt")
    
    assert result == "Test response"
    mock_ollama_client.generate.assert_called_once()
    
    # Check the request structure
    call_args = mock_ollama_client.generate.call_args[0][0]
    assert isinstance(call_args, OllamaRequest)
    assert call_args.model == "test-model"
    assert "Test system prompt" in call_args.prompt
    assert "Test prompt" in call_args.prompt


@pytest.mark.asyncio
async def test_call_ollama_with_context(test_agent, mock_ollama_client):
    """Test Ollama call with context."""
    context = {"key": "value"}
    result = await test_agent.call_ollama("Test prompt", context)
    
    assert result == "Test response"
    mock_ollama_client.generate.assert_called_once()


@pytest.mark.asyncio
async def test_call_ollama_exception(test_agent, mock_ollama_client):
    """Test Ollama call with exception."""
    mock_ollama_client.generate.side_effect = Exception("Ollama error")
    
    with pytest.raises(Exception) as exc_info:
        await test_agent.call_ollama("Test prompt")
    
    assert "Ollama error" in str(exc_info.value)


def test_can_handle_matching_type(test_agent):
    """Test can_handle with matching agent type."""
    request = AgentRequest(agent_type="testagent", message="Test")
    # Set agent_type manually for test
    test_agent.agent_type = "testagent"
    
    result = test_agent.can_handle(request)
    assert result is True


def test_can_handle_non_matching_type(test_agent):
    """Test can_handle with non-matching agent type."""
    request = AgentRequest(agent_type="different", message="Test")
    test_agent.agent_type = "testagent"
    
    result = test_agent.can_handle(request)
    assert result is False


def test_abstract_methods():
    """Test that BaseAgent is properly abstract."""
    mock_client = MagicMock()
    
    # Should not be able to instantiate BaseAgent directly
    with pytest.raises(TypeError):
        BaseAgent(mock_client)


def test_system_prompt_integration(test_agent):
    """Test system prompt integration in call_ollama."""
    system_prompt = test_agent.get_system_prompt()
    assert system_prompt == "Test system prompt"


def test_model_name_integration(test_agent):
    """Test model name integration in call_ollama."""
    model_name = test_agent.get_model_name()
    assert model_name == "test-model"


@pytest.mark.asyncio
async def test_full_prompt_construction(test_agent, mock_ollama_client):
    """Test full prompt construction with system prompt."""
    await test_agent.call_ollama("User message")
    
    call_args = mock_ollama_client.generate.call_args[0][0]
    full_prompt = call_args.prompt
    
    assert "Test system prompt" in full_prompt
    assert "User: User message" in full_prompt