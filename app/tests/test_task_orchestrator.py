"""Unit tests for TaskOrchestrator."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
import json
from core.task_orchestrator import TaskOrchestrator
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def orchestrator(mock_ollama_client):
    """TaskOrchestrator instance."""
    return TaskOrchestrator(mock_ollama_client)


@pytest.mark.asyncio
async def test_process_success(orchestrator):
    """Test successful task processing."""
    mock_tasks = [
        {"task_description": "Test task", "agent_type": "aiengineer", "priority": 1, "dependencies": []}
    ]
    
    with patch.object(orchestrator, 'analyze_and_split_request', return_value=mock_tasks):
        request = AgentRequest(agent_type="taskorchestrator", message="Test request")
        response = await orchestrator.process(request)
        
        assert response.success is True
        assert response.agent_type == "taskorchestrator"
        tasks = json.loads(response.response)
        assert len(tasks) == 1
        assert tasks[0]["agent_type"] == "aiengineer"


@pytest.mark.asyncio
async def test_process_exception(orchestrator):
    """Test processing with exception."""
    with patch.object(orchestrator, 'analyze_and_split_request', side_effect=Exception("Test error")):
        request = AgentRequest(agent_type="taskorchestrator", message="Test request")
        response = await orchestrator.process(request)
        
        assert response.success is False
        assert "Test error" in response.error


def test_get_system_prompt(orchestrator):
    """Test system prompt generation."""
    prompt = orchestrator.get_system_prompt()
    assert "task orchestrator" in prompt.lower()
    assert "aiengineer" in prompt
    assert "json array" in prompt.lower()


def test_get_model_name(orchestrator):
    """Test model name retrieval."""
    with patch('core.task_orchestrator.settings') as mock_settings:
        mock_settings.MODEL_TASKORCHESTRATOR = "test-model"
        model = orchestrator.get_model_name()
        assert model == "test-model"


@pytest.mark.asyncio
async def test_analyze_and_split_request_valid_json(orchestrator):
    """Test request analysis with valid JSON response."""
    valid_json = '[{"task_description": "Test task", "agent_type": "aiengineer", "priority": 1, "dependencies": []}]'
    
    with patch.object(orchestrator, 'call_ollama', return_value=valid_json):
        result = await orchestrator.analyze_and_split_request("Test request")
        
        assert len(result) == 1
        assert result[0]["agent_type"] == "aiengineer"
        assert result[0]["priority"] == 1


@pytest.mark.asyncio
async def test_analyze_and_split_request_json_in_markdown(orchestrator):
    """Test request analysis with JSON in markdown blocks."""
    markdown_response = '```json\n[{"task_description": "Test", "agent_type": "aiengineer", "priority": 1, "dependencies": []}]\n```'
    
    with patch.object(orchestrator, 'call_ollama', return_value=markdown_response):
        result = await orchestrator.analyze_and_split_request("Test request")
        
        assert len(result) == 1
        assert result[0]["agent_type"] == "aiengineer"


@pytest.mark.asyncio
async def test_analyze_and_split_request_invalid_json(orchestrator):
    """Test request analysis with invalid JSON."""
    invalid_json = "This is not JSON"
    
    with patch.object(orchestrator, 'call_ollama', return_value=invalid_json):
        result = await orchestrator.analyze_and_split_request("Test request")
        
        # Should fallback to single aiengineer task
        assert len(result) == 1
        assert result[0]["agent_type"] == "aiengineer"
        assert result[0]["task_description"] == "Test request"


@pytest.mark.asyncio
async def test_analyze_and_split_request_ollama_exception(orchestrator):
    """Test request analysis when Ollama throws exception."""
    with patch.object(orchestrator, 'call_ollama', side_effect=Exception("Ollama error")):
        result = await orchestrator.analyze_and_split_request("Test request")
        
        # Should fallback to single aiengineer task
        assert len(result) == 1
        assert result[0]["agent_type"] == "aiengineer"


def test_validate_dependencies_valid(orchestrator):
    """Test dependency validation with valid dependencies."""
    tasks = [
        {"task_description": "Task 1", "agent_type": "aiengineer", "dependencies": []},
        {"task_description": "Task 2", "agent_type": "uidesigner", "dependencies": [0]}
    ]
    
    result = orchestrator._validate_dependencies(tasks)
    
    assert len(result) == 2
    assert result[1]["dependencies"] == [0]


def test_validate_dependencies_invalid(orchestrator):
    """Test dependency validation with invalid dependencies."""
    tasks = [
        {"task_description": "Task 1", "agent_type": "aiengineer", "dependencies": [1, 5, -1]}  # Self-ref, out of range, negative
    ]
    
    result = orchestrator._validate_dependencies(tasks)
    
    assert len(result) == 1
    assert result[0]["dependencies"] == []  # Invalid deps removed


def test_validate_dependencies_missing_fields(orchestrator):
    """Test dependency validation with missing fields."""
    tasks = [
        {"task_description": "Task 1"}  # Missing agent_type and priority
    ]
    
    result = orchestrator._validate_dependencies(tasks)
    
    assert len(result) == 1
    assert result[0]["agent_type"] == "aiengineer"  # Default
    assert result[0]["priority"] == 3  # Default


def test_validate_dependencies_non_integer_deps(orchestrator):
    """Test dependency validation with non-integer dependencies."""
    tasks = [
        {"task_description": "Task 1", "agent_type": "aiengineer", "dependencies": ["invalid", 0.5, None]}
    ]
    
    result = orchestrator._validate_dependencies(tasks)
    
    assert len(result) == 1
    assert result[0]["dependencies"] == []  # Non-integers removed