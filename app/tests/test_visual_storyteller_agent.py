"""Unit tests for VisualStorytellerAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.visual_storyteller_agent import VisualStorytellerAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def visual_agent(mock_ollama_client):
    """VisualStorytellerAgent instance."""
    return VisualStorytellerAgent(mock_ollama_client)


def test_uses_correct_model(visual_agent):
    """Test that agent uses the correct model based on its intended function."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_VISUALSTORYTELLER = "mistral:7b"
        model = visual_agent.get_model_name()
        assert model == "mistral:7b"


def test_system_prompt_matches_instruction_exactly(visual_agent):
    """Test that agent's system_prompt matches the instruction exactly."""
    prompt = visual_agent.get_system_prompt()
    
    # Verify key components from the instruction are present exactly
    assert "You are a masterful visual storyteller who transforms complex ideas into captivating visual narratives." in prompt
    assert "Your expertise spans information design, data visualization, illustration, motion graphics, and the psychology of visual communication." in prompt
    assert "Visual Narrative Design" in prompt
    assert "Data Visualization" in prompt
    assert "Infographic Creation" in prompt
    assert "Presentation Design" in prompt
    assert "Illustration Systems" in prompt
    assert "Motion & Interaction" in prompt
    assert "Visual Storytelling Principles" in prompt
    assert "Your goal is to make the complex simple and the boring fascinating through visual storytelling." in prompt


def test_conforms_to_base_agent_schema(visual_agent):
    """Test that agent conforms to the BaseAgent schema."""
    # Test standard schema structure
    schema = visual_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "solution" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "technologies" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 4


@pytest.mark.asyncio
async def test_process_success(visual_agent):
    """Test successful processing."""
    with patch.object(visual_agent, 'call_ollama', return_value='{"solution": "test"}'):
        request = AgentRequest(agent_type="visualstoryteller", message="Create infographic")
        response = await visual_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "visualstoryteller"


@pytest.mark.asyncio
async def test_process_exception(visual_agent):
    """Test processing with exception."""
    with patch.object(visual_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="visualstoryteller", message="Test message")
        response = await visual_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_agent_type_mapping(visual_agent):
    """Test agent type is correctly mapped."""
    assert visual_agent.agent_type == "visualstoryteller"