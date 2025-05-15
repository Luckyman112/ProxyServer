# ProxyServer

Простое локальное Flask-приложение, которое по GET-запросу на `/get` возвращает JSON.

---

## Как запустить
## 1. Склонировать репозиторий  
git clone https://github.com/Luckyman112/ProxyServer.git

cd ProxyServer

## 2. Создать и активировать виртуальное окружение
python -m venv venv
#### Windows (PowerShell):
venv\Scripts\Activate.ps1
#### macOS/Linux:
source venv/bin/activate

## 3. Установить зависимости
В корне проекта есть requirements.txt.
pip install -r requirements.txt
  
  Содержимое requirements.txt:
  
  Flask
  
  requests
  
  gunicorn

## 4. Запустить сервер
python app.py
Сервер будет доступен по адресу http://127.0.0.1:5000

# Использование
#### GET /
Отображает простую HTML-подсказку.
#### GET /get
Возвращает JSON:

{
  
  "status": "ok",
  
  "message": "Works on my machine.",
  
  "params": { /* переданные GET-параметры */ }

}

### Пример:
curl "http://127.0.0.1:5000/get?foo=bar"

# Продакшн-запуск (опционально)
#### На Linux/WSL с Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
