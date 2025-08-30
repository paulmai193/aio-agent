# Agent Orchestrator

Ứng dụng Python điều phối các agent với tích hợp Ollama API.

## Tính năng

- Kiến trúc modular, dễ mở rộng
- Tích hợp Ollama qua REST API
- FastAPI endpoints
- Hỗ trợ nhiều loại agent (chat, code, ...)
- Docker support

## Cài đặt

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

## Docker

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