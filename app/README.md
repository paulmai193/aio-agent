# Agent Orchestrator

Ứng dụng Python điều phối các agent với tích hợp Ollama API.

## Tính năng

- Kiến trúc modular, dễ mở rộng
- Tích hợp Ollama qua REST API
- FastAPI endpoints
- Hỗ trợ nhiều loại agent (chat, code, ...)
- Docker support

## Quick Start

### Với Docker Compose (Khuyến nghị)

```bash
git clone <repo-url>
cd AI
docker-compose up -d
```

Trực tiếp truy cập: http://localhost:8000

### Với Python (Development)

1. Clone repository:
```bash
git clone <repo-url>
cd app
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Cấu hình environment:
```bash
cp .env.example .env
# Chỉnh sửa .env theo môi trường
```

4. Chạy ứng dụng:
```bash
python main.py
```

## Docker Compose (Khuyến nghị)

1. Chạy toàn bộ stack (Agent Orchestrator + Ollama):
```bash
docker-compose up -d
```

2. Xem logs:
```bash
docker-compose logs -f
```

3. Dừng services:
```bash
docker-compose down
```

4. Xóa volumes (reset data):
```bash
docker-compose down -v
```

### Services bao gồm:
- **agent-orchestrator**: FastAPI app (port 8000)
- **ollama**: Ollama server (port 11434)
- **ollama_data**: Persistent volume cho models

## Docker (Manual)

```bash
docker build -t agent-orchestrator .
docker run -p 8000:8000 agent-orchestrator
```

## API Endpoints

- `POST /api/v1/chat` - Gửi request đến agent
- `GET /api/v1/agents` - Danh sách agents
- `GET /api/v1/health` - Health check

## Thêm Agent mới

1. Tạo file trong `agents/` kế thừa từ `BaseAgent`
2. Implement các method bắt buộc
3. Đăng ký trong `AgentManager.initialize()`

## Cấu trúc dự án

```
app/
├── main.py              # Entry point
├── config.py            # Cấu hình
├── router/
│   └── api.py          # API endpoints
├── core/
│   ├── agent_manager.py # Quản lý agent
│   ├── ollama_client.py # Ollama client
│   ├── schemas.py       # Pydantic models
│   └── utils.py         # Utilities
└── agents/
    ├── base.py          # Base agent class
    ├── chat_agent.py    # Chat agent
    └── code_agent.py    # Code agent
```
## Ollama Models Setup

Sau khi chạy docker-compose, cài đặt models:

### Tự động (Khuyến nghị)
```bash
# Linux/Mac
./setup-models.sh

# Windows
setup-models.bat
```

### Thủ công
```bash
# Pull models cần thiết
docker-compose exec ollama ollama pull llama2
docker-compose exec ollama ollama pull codellama

# Kiểm tra models đã cài
docker-compose exec ollama ollama list
```

## Testing

```bash
# Test tất cả agents
python test_agents_integration.py

# Test API endpoints
curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "chat", "message": "Hello"}'
```