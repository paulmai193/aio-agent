"""Unit tests for TrendResearcherAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.trend_researcher_agent import TrendResearcherAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def trend_agent(mock_ollama_client):
    """TrendResearcherAgent instance."""
    return TrendResearcherAgent(mock_ollama_client)


def test_uses_correct_model(trend_agent):
    """Test that agent uses the correct model based on its intended function."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_TRENDRESEARCHER = "llama3.2:3b"
        model = trend_agent.get_model_name()
        assert model == "llama3.2:3b"


def test_system_prompt_matches_instruction_exactly(trend_agent):
    """Test that agent's system_prompt matches the instruction exactly."""
    prompt = trend_agent.get_system_prompt()
    
    # Verify key components from the instruction are present exactly
    assert "You are a cutting-edge market trend analyst specializing in identifying viral opportunities and emerging user behaviors" in prompt
    assert "Your superpower is spotting trends before they peak and translating cultural moments into product opportunities that can be built within 6-day sprints." in prompt
    assert "Viral Trend Detection" in prompt
    assert "App Store Intelligence" in prompt
    assert "User Behavior Analysis" in prompt
    assert "Opportunity Synthesis" in prompt
    assert "Competitive Landscape Mapping" in prompt
    assert "Cultural Context Integration" in prompt
    assert "Research Methodologies" in prompt
    assert "Key Metrics to Track" in prompt
    assert "Decision Framework" in prompt
    assert "Trend Evaluation Criteria" in prompt
    assert "Red Flags to Avoid" in prompt
    assert "Reporting Format" in prompt
    assert "Your goal is to be the studio's early warning system for opportunities" in prompt
    assert "You are the bridge between what's trending and what's buildable." in prompt


def test_conforms_to_base_agent_schema(trend_agent):
    """Test that agent conforms to the BaseAgent schema."""
    # Test standard schema structure
    schema = trend_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "solution" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "technologies" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 4


@pytest.mark.asyncio
async def test_process_success(trend_agent):
    """Test successful processing."""
    with patch.object(trend_agent, 'call_ollama', return_value='{"solution": "test"}'):
        request = AgentRequest(agent_type="trendresearcher", message="Research TikTok trends")
        response = await trend_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "trendresearcher"


@pytest.mark.asyncio
async def test_process_exception(trend_agent):
    """Test processing with exception."""
    with patch.object(trend_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="trendresearcher", message="Test message")
        response = await trend_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_agent_type_mapping(trend_agent):
    """Test agent type is correctly mapped."""
    assert trend_agent.agent_type == "trendresearcher"


@pytest.mark.asyncio
async def test_system_initialize_agent_successfully():
    """Test system initializes agent successfully."""
    from core.agent_manager import AgentManager
    
    agent_manager = AgentManager()
    await agent_manager.initialize()
    
    # Verify agent is loaded in system
    assert "trendresearcher" in agent_manager.agents
    assert isinstance(agent_manager.agents["trendresearcher"], TrendResearcherAgent)