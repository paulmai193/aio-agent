"""
Entry point cho Agent Orchestrator Application.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from core.agent_manager import AgentManager
from router.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý lifecycle của ứng dụng."""
    # Startup
    logging.info("Khởi tạo Agent Manager...")
    agent_manager = AgentManager()
    await agent_manager.initialize()
    app.state.agent_manager = agent_manager
    
    yield
    
    # Shutdown
    logging.info("Đóng Agent Manager...")
    await agent_manager.cleanup()


def create_app() -> FastAPI:
    """Tạo và cấu hình FastAPI application."""
    app = FastAPI(
        title="Agent Orchestrator",
        description="Điều phối các agent với Ollama integration",
        version="1.0.0",
        lifespan=lifespan
    )
    
    app.include_router(router, prefix="/api/v1")
    
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )