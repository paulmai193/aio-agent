"""Unit tests for BrandGuardianAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.brand_guardian_agent import BrandGuardianAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def brand_agent(mock_ollama_client):
    """BrandGuardianAgent instance."""
    return BrandGuardianAgent(mock_ollama_client)


@pytest.mark.asyncio
async def test_process_success(brand_agent):
    """Test successful brand guardian processing."""
    with patch.object(brand_agent, 'call_ollama', return_value='{"brand_strategy": "test"}'):
        request = AgentRequest(agent_type="brandguardian", message="Create brand guidelines")
        response = await brand_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "brandguardian"
        assert "brand_strategy" in response.response


@pytest.mark.asyncio
async def test_process_exception(brand_agent):
    """Test processing with exception."""
    with patch.object(brand_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="brandguardian", message="Test message")
        response = await brand_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_get_system_prompt(brand_agent):
    """Test system prompt generation."""
    prompt = brand_agent.get_system_prompt()
    assert "brand guardian" in prompt.lower()
    assert "visual identity" in prompt.lower()
    assert "brand strategy" in prompt.lower()


def test_get_model_name(brand_agent):
    """Test model name retrieval."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_BRANDGUARDIAN = "test-brand-model"
        model = brand_agent.get_model_name()
        assert model == "test-brand-model"


def test_get_standard_schema(brand_agent):
    """Test brand guardian schema."""
    schema = brand_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "brand_strategy" in schema["properties"]
    assert "visual_identity" in schema["properties"]
    assert "design_system" in schema["properties"]
    assert "asset_management" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 6


def test_agent_type_mapping(brand_agent):
    """Test agent type is correctly mapped."""
    assert brand_agent.agent_type == "brandguardian"