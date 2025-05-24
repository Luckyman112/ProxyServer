# ProxyServer

Лёгкий заглушечный прокси для OpenAI-совместимых запросов и Open-WebUI.  
Логирует все входящие запросы с отметкой времени и отдаёт фиктивный ответ или SSE-поток.

---

## Содержание

- [Требования](#требования)  
- [Установка](#установка)  
- [Запуск](#запуск)  
  - [Локально](#локально)  
  - [Через Docker](#через-docker)  
- [Конфигурация](#конфигурация)  
- [Endpoints](#endpoints)  
- [Логи](#логи)  
- [.gitignore](#gitignore)  
- [Разработка](#разработка)  

---

## Требования

- Python 3.11+  
- pip  
- Docker & Docker Compose (для контейнерной сборки)  

---

## Установка

1. Клонировать репозиторий:  
   ```bash
   git clone <ваш_репозиторий_URL>
   cd ProxyServer

2. (опционально) Создать виртуальное окружение и установить зависимости:
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
pip install -r requirements.txt

## Запуск
### Локально
export TZ=Europe/Riga     # настроить часовой пояс
python app.py
— сервер стартует на http://0.0.0.0:5000.

### Через Docker
docker-compose up --build -d
proxy слушает 5000:5000

open-webui слушает 3000:8080

## Конфигурация
TZ: часовой пояс задаётся в Dockerfile через ENV TZ=Europe/Riga и пакет tzdata.

log.txt: файл логов создаётся автоматически при первом запросе.

## Endpoints
### GET /v1/models
Возвращает JSON:

{
  "object":"list",
  "data":[{"id":"gpt-3.5-turbo","object":"model","created":0,"owned_by":"proxy-server","permission":[]}]
}

### OPTIONS /v1/models
CORS-прелюдия, отвечает 204 No Content.

### POST /v1/chat/completions

  С stream=true отдаёт SSE-поток (text/event-stream) с фиктивными чат-чанками и завершением data: [DONE].

  Без stream (или stream=false) выдаёт единичный JSON-ответ в формате OpenAI.

### OPTIONS /v1/chat/completions
CORS-прелюдия, отвечает 204 No Content.

## Логи
Все входящие payload’ы записываются в log.txt в формате JSON:

{
  "stream": true,
  "model": "gpt-3.5-turbo",
  "messages": [...],
  "timestamp": "2025-05-24T14:29:30"
}

Чтобы смотреть логи на хосте (при volume .:/app):

tail -f log.txt

## .gitignore
__pycache__/
*.py[cod]
log.txt
.venv/
venv/
.dockerignore

## Разработка
Для правок в коде: app.py

Для изменений зависимостей: requirements.txt

После правок пересобрать Docker:
  docker-compose build proxy
  docker-compose up -d

Проверять эндпоинты через curl или Open-WebUI.

Примечание: файл log.txt не хранится в репозитории, он создаётся автоматически при первом запросе. ```