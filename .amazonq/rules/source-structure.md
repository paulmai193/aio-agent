app/
│
├── main.py                # Entry point (khởi tạo FastAPI, route chung)
├── config.py              # Đọc config (YAML/ENV)
├── router/
│   └── api.py             # Định nghĩa các endpoint REST
│
├── core/
│   ├── agent_manager.py   # Quản lý, điều phối agent (khởi tạo, routing)
│   ├── ollama_client.py   # Gọi Ollama API (REST client)
│   ├── schemas.py         # Pydantic models cho request/response
│   └── utils.py           # Helper chung (logging, xử lý lỗi, ...)
│
├── agents/
│   ├── __init__.py
│   ├── base.py            # Base class cho agent (interface)
│   ├── agent_x.py         # Một agent cụ thể
│   ├── agent_y.py         # Agent khác (dễ mở rộng)
│   └── ...                # Thêm agent mới ở đây
│
├── tests/                 # Unit test, integration test
│
├── requirements.txt
├── Dockerfile
└── README.md