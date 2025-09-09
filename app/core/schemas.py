"""
Pydantic models cho request/response schemas.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Request gửi đến agent."""
    agent_type: str = Field(..., min_length=1, description="Agent type must not be empty")
    message: str = Field(..., min_length=1, description="Message must not be empty")
    context: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    """Response từ agent."""
    agent_type: str
    response: str
    metadata: Optional[Dict[str, Any]] = None
    success: bool = True
    error: Optional[str] = None


class OllamaRequest(BaseModel):
    """Request gửi đến Ollama."""
    model: str
    system: Optional[str] = None
    prompt: str
    stream: bool = False
    format: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "system": self.system,
            "prompt": self.prompt,
            "stream": self.stream,
            "format": self.format,
            "options": self.options
        }

class OllamaResponse(BaseModel):
    """Response từ Ollama."""
    model: str
    response: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    agents_loaded: int
    ollama_connected: bool