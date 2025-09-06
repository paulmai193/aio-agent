"""Unit tests for API endpoints."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from router.api import router, get_agent_manager
from core.schemas import AgentResponse, HealthResponse


@pytest.fixture
def mock_agent_manager():
    """Mock AgentManager."""
    manager = MagicMock()
    manager.process_request = AsyncMock()
    manager.list_agents = MagicMock(return_value=["aiengineer", "uidesigner"])
    manager.health_check = AsyncMock(return_value={
        "agents_loaded": 2,
        "agent_types": ["aiengineer", "uidesigner"],
        "ollama_connected": True
    })
    return manager


@pytest.fixture
def test_app(mock_agent_manager):
    """Test FastAPI app."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    
    # Override dependency
    app.dependency_overrides[get_agent_manager] = lambda: mock_agent_manager
    
    return app


@pytest.fixture
def client(test_app):
    """Test client."""
    return TestClient(test_app)


def test_chat_endpoint_success(client, mock_agent_manager):
    """Test successful chat endpoint."""
    mock_agent_manager.process_request.return_value = AgentResponse(
        agent_type="aiengineer",
        response="Test response",
        success=True
    )
    
    response = client.post("/api/v1/chat", json={
        "agent_type": "aiengineer",
        "message": "Test message"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["agent_type"] == "aiengineer"
    assert data["response"] == "Test response"
    assert data["success"] is True


def test_chat_endpoint_agent_failure(client, mock_agent_manager):
    """Test chat endpoint with agent failure."""
    mock_agent_manager.process_request.return_value = AgentResponse(
        agent_type="aiengineer",
        response="",
        success=False,
        error="Agent error"
    )
    
    response = client.post("/api/v1/chat", json={
        "agent_type": "aiengineer",
        "message": "Test message"
    })
    
    assert response.status_code == 400
    assert "Agent error" in response.json()["detail"]


def test_chat_endpoint_exception(client, mock_agent_manager):
    """Test chat endpoint with exception."""
    mock_agent_manager.process_request.side_effect = Exception("Unexpected error")
    
    response = client.post("/api/v1/chat", json={
        "agent_type": "aiengineer",
        "message": "Test message"
    })
    
    assert response.status_code == 500
    assert "Unexpected error" in response.json()["detail"]


def test_chat_endpoint_invalid_request(client):
    """Test chat endpoint with invalid request."""
    response = client.post("/api/v1/chat", json={
        "agent_type": "",  # Empty agent_type should fail validation
        "message": "Test message"
    })
    
    assert response.status_code == 422  # Validation error


def test_list_agents_endpoint(client, mock_agent_manager):
    """Test list agents endpoint."""
    response = client.get("/api/v1/agents")
    
    assert response.status_code == 200
    data = response.json()
    assert data == ["aiengineer", "uidesigner"]
    mock_agent_manager.list_agents.assert_called_once()


def test_health_check_endpoint_healthy(client, mock_agent_manager):
    """Test health check endpoint when healthy."""
    response = client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["agents_loaded"] == 2
    assert data["ollama_connected"] is True


def test_health_check_endpoint_degraded(client, mock_agent_manager):
    """Test health check endpoint when degraded."""
    mock_agent_manager.health_check.return_value = {
        "agents_loaded": 2,
        "agent_types": ["aiengineer", "uidesigner"],
        "ollama_connected": False
    }
    
    response = client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["agents_loaded"] == 2
    assert data["ollama_connected"] is False


def test_health_check_endpoint_exception(client, mock_agent_manager):
    """Test health check endpoint with exception."""
    mock_agent_manager.health_check.side_effect = Exception("Health check error")
    
    response = client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["agents_loaded"] == 0
    assert data["ollama_connected"] is False


def test_process_user_request_success(client, mock_agent_manager):
    """Test process user request endpoint success."""
    # Mock TaskOrchestrator
    mock_tasks = [
        {"task_description": "Test task", "agent_type": "aiengineer", "priority": 1, "dependencies": []}
    ]
    
    mock_response = AgentResponse(
        agent_type="aiengineer",
        response="Task completed",
        success=True
    )
    
    mock_agent_manager.process_request.return_value = mock_response
    
    with patch('router.api.TaskOrchestrator') as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator.analyze_and_split_request = AsyncMock(return_value=mock_tasks)
        mock_orchestrator_class.return_value = mock_orchestrator
        
        response = client.post("/api/v1/process", json={
            "message": "Build a web app"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["tasks"]) == 1
    assert len(data["results"]) == 1


def test_process_user_request_task_failure(client, mock_agent_manager):
    """Test process user request with task failure."""
    mock_tasks = [
        {"task_description": "Test task", "agent_type": "aiengineer", "priority": 1, "dependencies": []}
    ]
    
    mock_response = AgentResponse(
        agent_type="aiengineer",
        response="",
        success=False,
        error="Task failed"
    )
    
    mock_agent_manager.process_request.return_value = mock_response
    
    with patch('router.api.TaskOrchestrator') as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator.analyze_and_split_request = AsyncMock(return_value=mock_tasks)
        mock_orchestrator_class.return_value = mock_orchestrator
        
        response = client.post("/api/v1/process", json={
            "message": "Build a web app"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Some tasks failed" in data["error"]


def test_process_user_request_exception(client, mock_agent_manager):
    """Test process user request with exception."""
    with patch('router.api.TaskOrchestrator', side_effect=Exception("Orchestrator error")):
        response = client.post("/api/v1/process", json={
            "message": "Build a web app"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Orchestrator error" in data["error"]


def test_process_user_request_invalid_input(client):
    """Test process user request with invalid input."""
    response = client.post("/api/v1/process", json={
        "message": ""  # Empty message should fail validation
    })
    
    assert response.status_code == 422  # Validation error