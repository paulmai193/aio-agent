# Agent Orchestrator

Python application điều phối các agent từ [Contains Studio Agents](https://github.com/contains-studio/agents) với tích hợp Ollama API.

## 🚀 Quick Start

### Development
```bash
# Linux/Mac
git clone <repo-url>
cd AI
docker-compose -f docker-compose.dev.yml up -d
./setup-models-dev.sh

# Windows
git clone <repo-url>
cd AI
docker-compose -f docker-compose.dev.yml up -d
setup-models-dev.bat
```

### Production
```bash
# Linux/Mac
git clone <repo-url>
cd AI
docker-compose -f docker-compose.prod.yml up -d
./setup-models-prod.sh

# Windows
git clone <repo-url>
cd AI
docker-compose -f docker-compose.prod.yml up -d
setup-models-prod.bat
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



## 🔧 Build & Development

### Environment Profiles

#### Development Environment
- **Models**: Lightweight (7b versions)
- **Features**: Hot reload, debug logging, volume mounts
- **Resources**: Lower memory usage

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Setup lightweight models
./setup-models-dev.sh      # Linux/Mac
setup-models-dev.bat        # Windows

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down
```

#### Production Environment
- **Models**: Full-size (13b versions)
- **Features**: Security hardening, health checks, 4 workers
- **Resources**: Optimized for performance

```bash
# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# Setup production models
./setup-models-prod.sh      # Linux/Mac
setup-models-prod.bat       # Windows

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

#### Local Development (Python)
```bash
cd app
pip install -r requirements.txt
cp .env.dev .env  # or .env.prod
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

## 📊 Models Configuration

### Development Models (Lightweight)
- **Engineering agents**: `codellama:7b`
- **Content agents**: `llama2:7b`
- **Task Orchestrator**: `deepseek-r1:1.5b`

### Production Models (Full Performance)
- **Engineering agents**: `codellama:13b`
- **Content agents**: `llama2:13b`
- **Task Orchestrator**: `deepseek-r1:7b`

### Model Assignment
- **Engineering**: aiengineer, backendarchitect, frontenddeveloper, rapidprototyper, devopsautomator, testwriterfixer
- **Content**: uidesigner, contentcreator, growthhacker, trendresearcher, projectshipper
- **Orchestration**: taskorchestrator

## 🐳 Docker Management

### Development Commands
```bash
# Build and start
docker-compose -f docker-compose.dev.yml up --build -d

# Rebuild specific service
docker-compose -f docker-compose.dev.yml build agent-orchestrator

# View logs
docker-compose -f docker-compose.dev.yml logs -f agent-orchestrator

# Reset development data
docker-compose -f docker-compose.dev.yml down -v
```

### Production Commands
```bash
# Deploy production
docker-compose -f docker-compose.prod.yml up --build -d

# Scale workers
docker-compose -f docker-compose.prod.yml up --scale agent-orchestrator=3 -d

# Health check
docker-compose -f docker-compose.prod.yml exec agent-orchestrator curl http://localhost:8000/api/v1/health

# Production logs
docker-compose -f docker-compose.prod.yml logs --tail=100 -f
```

### Model Management
```bash
# List installed models
docker-compose exec ollama ollama list

# Remove unused models
docker-compose exec ollama ollama rm <model-name>

# Pull specific model
docker-compose exec ollama ollama pull llama2:13b
```

## 🧪 Testing & Monitoring

### Integration Testing
```bash
# Test all agents
python test_agents_integration.py

# Test specific environment
ENV=dev python test_agents_integration.py
ENV=prod python test_agents_integration.py
```

### Health Monitoring
```bash
# Application health
curl http://localhost:8000/api/v1/health

# Ollama health
curl http://localhost:11434/api/tags

# Container health
docker-compose ps
docker-compose top
```

### Performance Testing
```bash
# Load test orchestrator
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a simple web app"}'

# Benchmark specific agent
time curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "aiengineer", "message": "Hello"}'
```

## 📄 License

MIT License