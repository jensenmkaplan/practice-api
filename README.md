## practice-api
For creating custom APIs

### Prerequisites
- Python 3.11+ on macOS (`python3 --version`)

### Quickstart
```bash
cd practice-api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Try it
- Open your browser to `http://127.0.0.1:8000` for the welcome message
- Health check: `http://127.0.0.1:8000/health`
- Interactive docs: `http://127.0.0.1:8000/docs`

Example request:
```bash
curl -X POST "http://127.0.0.1:8000/echo" \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

### Project structure
```
practice-api/
  app/
    __init__.py
    main.py
  requirements.txt
  README.md
```

### Next steps
- Add new endpoints in `app/main.py`
- Split routes into modules (e.g., `app/routers/`) as the API grows
- Add tests with `pytest`

### Deploy to Render
1. Push this repo to GitHub.
2. Sign in to Render and create a new Web Service from your repo.
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`
3. After deploy, your base URL will be something like `https://practice-api.onrender.com`.

### Test from n8n (HTTP Request node)
- Method: `GET`
- URL: `https://practice-api.onrender.com/health`
- Expect: `{"status":"ok"}` and HTTP 200

For POST `/echo` in n8n:
- Method: `POST`
- URL: `https://practice-api.onrender.com/echo`
- Send: JSON body `{"message":"hello"}`
- Headers: `Content-Type: application/json`
