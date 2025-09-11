"""Unit tests for UxResearcherAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.ux_researcher_agent import UxResearcherAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def ux_agent(mock_ollama_client):
    """UxResearcherAgent instance."""
    return UxResearcherAgent(mock_ollama_client)


@pytest.mark.asyncio
async def test_process_success(ux_agent):
    """Test successful UX research processing."""
    with patch.object(ux_agent, 'call_ollama', return_value='{"research_approach": "test"}'):
        request = AgentRequest(agent_type="uxresearcher", message="Analyze user onboarding flow")
        response = await ux_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "uxresearcher"
        assert "research_approach" in response.response


@pytest.mark.asyncio
async def test_process_exception(ux_agent):
    """Test processing with exception."""
    with patch.object(ux_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="uxresearcher", message="Test message")
        response = await ux_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_get_system_prompt(ux_agent):
    """Test system prompt generation."""
    prompt = ux_agent.get_system_prompt()
    assert "ux researcher" in prompt.lower()
    assert "user behavior" in prompt.lower()
    assert "research methodologies" in prompt.lower()
    assert "usability testing" in prompt.lower()


def test_get_model_name(ux_agent):
    """Test model name retrieval."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_UXRESEARCHER = "test-ux-model"
        model = ux_agent.get_model_name()
        assert model == "test-ux-model"


def test_get_standard_schema(ux_agent):
    """Test UX researcher schema."""
    schema = ux_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "research_approach" in schema["properties"]
    assert "user_insights" in schema["properties"]
    assert "journey_mapping" in schema["properties"]
    assert "testing_methods" in schema["properties"]
    assert "personas" in schema["properties"]
    assert "recommendations" in schema["properties"]
    assert len(schema["required"]) == 6


def test_agent_type_mapping(ux_agent):
    """Test agent type is correctly mapped."""
    assert ux_agent.agent_type == "uxresearcher"