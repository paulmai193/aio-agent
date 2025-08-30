# Available Agents

Danh sách tất cả agents có sẵn trong hệ thống (system prompts được lấy từ https://github.com/contains-studio/agents):

## Engineering Agents

- **aiengineer** - AiEngineerAgent: Expert AI engineer - LLM integration, ML pipelines, computer vision, general programming
- **backendarchitect** - BackendArchitectAgent: Master backend architect - scalable APIs, databases, microservices
- **frontenddeveloper** - FrontendDeveloperAgent: Elite frontend specialist - React/Vue, responsive design, performance
- **rapidprototyper** - RapidPrototyperAgent: Rapid prototyping specialist - MVP development, fast iteration
- **devopsautomator** - DevopsAutomatorAgent: DevOps automator - CI/CD, Docker, infrastructure automation
- **testwriterfixer** - TestWriterFixerAgent: Test specialist - unit tests, integration tests, quality assurance

## Marketing & Growth Agents

- **contentcreator** - ContentCreatorAgent: Content creator - cross-platform content, SEO, video scripts
- **growthhacker** - GrowthHackerAgent: Growth hacker - viral mechanics, user acquisition, data-driven experiments

## Design Agents

- **uidesigner** - UiDesignerAgent: Visionary UI designer - modern interfaces, design systems, rapid implementation

## Product & Research Agents

- **trendresearcher** - TrendResearcherAgent: Trend researcher - viral opportunities, market analysis, consumer behavior

## Project Management Agents

- **projectshipper** - ProjectShipperAgent: Project shipper - launch coordination, risk mitigation, delivery management

## Cách sử dụng

### API Request
```json
{
  "agent_type": "aiengineer",
  "message": "Tích hợp AI chatbot vào ứng dụng web",
  "context": {
    "language": "python",
    "framework": "fastapi"
  }
}
```

### Response
```json
{
  "agent_type": "aiengineer",
  "response": "Để tích hợp AI chatbot...",
  "metadata": {
    "model": "codellama"
  },
  "success": true
}
```

## Mở rộng Agents

Để thêm agent mới:

1. Tạo file `new_agent.py` trong `agents/`
2. Kế thừa từ `BaseAgent`
3. Implement các method bắt buộc
4. Thêm vào `__init__.py`
5. Đăng ký trong `AgentManager.initialize()`

## Models sử dụng

- **Engineering agents**: `codellama` - Tối ưu cho code
- **Other agents**: `llama2` - Tối ưu cho text chung
- **Task Orchestrator**: `deepseek-r1:1.5b` - Tối ưu cho reasoning và task analysis (compact version)

## System Prompts

Tất cả system prompts được lấy trực tiếp từ các file markdown trong repository https://github.com/contains-studio/agents, đảm bảo tính chính xác và đầy đủ của chuyên môn cho từng agent.

Các agents đã được tích hợp với system prompts đầy đủ từ repository gốc, bao gồm:
- Detailed responsibilities và expertise areas
- Best practices và frameworks
- Integration với 6-day sprint model
- Performance metrics và success criteria

## Mở rộng Agents

Để thêm agent mới từ repository:

1. Tạo file `new_agent.py` trong `agents/` kế thừa từ `BaseAgent`
2. Sao chép system prompt từ file markdown tương ứng
3. Chọn model phù hợp (`codellama` cho engineering, `llama2` cho khác)
4. Thêm vào `__init__.py` và `AgentManager.initialize()`

Tất cả 13 agents chính đã được tích hợp với system prompts đầy đủ từ repository gốc.