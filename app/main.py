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
    logging.info("Starting Agent Orchestrator application...")
    agent_manager = None
    try:
        logging.info("Khởi tạo Agent Manager...")
        agent_manager = AgentManager()
        await agent_manager.initialize()
        app.state.agent_manager = agent_manager
        logging.info("Application startup completed")
    except Exception as e:
        logging.error(f"Failed to initialize Agent Manager: {e}")
        raise
    
    yield
    
    # Shutdown
    logging.info("Shutting down Agent Orchestrator application...")
    if agent_manager:
        try:
            logging.info("Đóng Agent Manager...")
            await agent_manager.cleanup()
            logging.info("Application shutdown completed")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")


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
    logging.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )