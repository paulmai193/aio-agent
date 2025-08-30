"""
Utility functions và helpers chung.
"""
import logging
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO"):
    """Cấu hình logging cho ứng dụng."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Lấy giá trị từ dict một cách an toàn."""
    try:
        return data.get(key, default)
    except (AttributeError, TypeError):
        return default


def validate_agent_type(agent_type: str, available_types: list) -> bool:
    """Kiểm tra agent type có hợp lệ không."""
    return agent_type in available_types


def format_error_response(error: Exception, agent_type: str = "unknown") -> Dict[str, Any]:
    """Format error response."""
    return {
        "agent_type": agent_type,
        "response": "",
        "success": False,
        "error": str(error),
        "error_type": type(error).__name__
    }