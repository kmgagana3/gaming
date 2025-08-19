## NeuroSpectra Backend (FastAPI)

Run locally:

```bash
cd /workspace/neurospectra/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open docs at `http://127.0.0.1:8000/docs`.

