# Report_llm_agent

## Запуск

Добавить файл .env в директорию **configs/.env**

Пример содержания .env:
```
LANGFUSE_PUBLIC_KEY=""
LANGFUSE_SECRET_KEY=""
LANGFUSE_HOST="https://cloud.langfuse.com"
API_KEY=""
TAVILY_API_KEY=""
```

```bash
  docker build -t fastapi-app . 
```

```bash
  docker run -d -p 8000:8000 --name report-llm-agent-v1.0 fastapi-app 
```

## Endpoints

### 1. /llm_agent/user_endpoint

Вход:
- "topic": str (Тема отчета)
- "num_chapters": int (Количество глав в отчете)

Выход:
- .docx файл