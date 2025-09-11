"""Unit tests for TiktokStrategistAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.tiktok_strategist_agent import TiktokStrategistAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def tiktok_agent(mock_ollama_client):
    """TiktokStrategistAgent instance."""
    return TiktokStrategistAgent(mock_ollama_client)


def test_uses_correct_model(tiktok_agent):
    """Test that agent uses the correct model based on its intended function."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_TIKTOKSTRATEGIST = "llama3.2:3b"
        model = tiktok_agent.get_model_name()
        assert model == "llama3.2:3b"


def test_system_prompt_matches_instruction_exactly(tiktok_agent):
    """Test that agent's system_prompt matches the instruction exactly."""
    prompt = tiktok_agent.get_system_prompt()
    
    # Verify key components from the instruction are present exactly
    assert "You are a TikTok marketing virtuoso who understands the platform's culture, algorithm, and viral mechanics at an expert level." in prompt
    assert "You've helped apps go from zero to millions of downloads through strategic TikTok campaigns" in prompt
    assert "You embody the principle that on TikTok, authenticity beats production value every time." in prompt
    assert "Viral Content Strategy" in prompt
    assert "Algorithm Optimization" in prompt
    assert "Content Format Development" in prompt
    assert "Influencer Collaboration Strategy" in prompt
    assert "User-Generated Content Campaigns" in prompt
    assert "Performance Analytics & Optimization" in prompt
    assert "Content Pillars for Apps" in prompt
    assert "TikTok-Specific Best Practices" in prompt
    assert "Viral Mechanics to Leverage" in prompt
    assert "Platform Culture Rules" in prompt
    assert "Campaign Timeline (6-day sprint)" in prompt
    assert "Decision Framework" in prompt
    assert "Red Flags to Avoid" in prompt
    assert "Success Metrics" in prompt
    assert "Your goal is to make apps culturally relevant and irresistibly shareable on TikTok." in prompt
    assert "You are the studio's secret weapon for turning apps into TikTok phenomena that drive real downloads and engaged users." in prompt


def test_conforms_to_base_agent_schema(tiktok_agent):
    """Test that agent conforms to the BaseAgent schema."""
    # Test standard schema structure
    schema = tiktok_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "solution" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "technologies" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 4


@pytest.mark.asyncio
async def test_process_success(tiktok_agent):
    """Test successful processing."""
    with patch.object(tiktok_agent, 'call_ollama', return_value='{"solution": "test"}'):
        request = AgentRequest(agent_type="tiktokstrategist", message="Create viral TikTok strategy")
        response = await tiktok_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "tiktokstrategist"


@pytest.mark.asyncio
async def test_process_exception(tiktok_agent):
    """Test processing with exception."""
    with patch.object(tiktok_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="tiktokstrategist", message="Test message")
        response = await tiktok_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_agent_type_mapping(tiktok_agent):
    """Test agent type is correctly mapped."""
    assert tiktok_agent.agent_type == "tiktokstrategist"


@pytest.mark.asyncio
async def test_system_initialize_agent_successfully():
    """Test system initializes agent successfully."""
    from core.agent_manager import AgentManager
    
    agent_manager = AgentManager()
    await agent_manager.initialize()
    
    # Verify agent is loaded in system
    assert "tiktokstrategist" in agent_manager.agents
    assert isinstance(agent_manager.agents["tiktokstrategist"], TiktokStrategistAgent)