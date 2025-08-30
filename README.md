# Agent Orchestrator

Python application điều phối các agent từ [Contains Studio Agents](https://github.com/contains-studio/agents) với tích hợp Ollama API.

## 🚀 Quick Start

```bash
git clone <repo-url>
cd AI
docker-compose up -d
./setup-models.sh  # hoặc setup-models.bat trên Windows
```

Truy cập: http://localhost:8000

## 🎯 Tính năng

- **11 chuyên gia AI agents** từ Contains Studio repository
- **Kiến trúc modular** dễ mở rộng
- **Tích hợp Ollama** qua REST API
- **FastAPI endpoints** với documentation tự động
- **Docker support** với docker-compose
- **System prompts chuyên nghiệp** từ repository gốc

## 📋 Available Agents

### Engineering (6 agents)
- `aiengineer` - AI/ML implementation, LLM integration
- `backendarchitect` - Scalable APIs, databases, microservices  
- `frontenddeveloper` - React/Vue, responsive design, performance
- `rapidprototyper` - MVP development, fast iteration
- `devopsautomator` - CI/CD, Docker, infrastructure automation
- `testwriterfixer` - Unit tests, integration tests, quality assurance

### Marketing & Growth (2 agents)
- `contentcreator` - Cross-platform content, SEO, video scripts
- `growthhacker` - Viral mechanics, user acquisition, experiments

### Design (1 agent)
- `uidesigner` - Modern interfaces, design systems, rapid implementation

### Product & Research (1 agent)
- `trendresearcher` - Viral opportunities, market analysis, consumer behavior

### Project Management (1 agent)
- `projectshipper` - Launch coordination, risk mitigation, delivery



## 🔧 Development Setup

```bash
cd app
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## 📡 API Usage

### Smart Processing (Recommended)
```bash
# Let AI choose agents automatically
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Build a social media app with AI features and deploy it"}'
```

### Manual Agent Selection
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat with specific agent
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "aiengineer", "message": "Integrate AI chatbot into web app"}'

# List available agents
curl http://localhost:8000/api/v1/agents
```

## 🏗️ Architecture

```
app/
├── main.py              # FastAPI entry point
├── config.py            # Environment configuration
├── router/api.py        # API endpoints
├── core/
│   ├── agent_manager.py # Agent orchestration
│   ├── ollama_client.py # Ollama integration
│   └── schemas.py       # Pydantic models
└── agents/              # 13 specialized agents
    ├── base.py          # Base agent class
    └── *_agent.py       # Individual agents
```

## 🔄 Adding New Agents

1. Create `new_agent.py` inheriting from `BaseAgent`
2. Copy system prompt from corresponding markdown file
3. Choose appropriate model (`codellama` for engineering, `llama2` for others)
4. Register in `AgentManager.initialize()`

## 📊 Models Used

- **Engineering agents**: `codellama` - Optimized for code
- **Other agents**: `llama2` - Optimized for general text

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Reset data
docker-compose down -v
```

## 🧪 Testing

```bash
python test_agents_integration.py
```

## 📄 License

MIT License