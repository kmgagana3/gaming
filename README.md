## NeuroSpectra: AI-Assisted Early ASD Screening

This repository contains a complete, runnable full‑stack project with:

- Backend: FastAPI (Python) providing endpoints for EEG, audio‑visual, game assessment, combined risk prediction, and AI‑generated feedback
- Frontend: React (Vite + TypeScript) providing a clean UI to upload data, run an interactive game, and view results

### Quick Start

Prerequisites:

- Python 3.10+
- Node.js 18+ and npm 9+

1) Backend setup

```bash
cd /workspace/neurospectra/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at `http://127.0.0.1:8000` with docs at `http://127.0.0.1:8000/docs`.

2) Frontend setup (in a separate terminal)

```bash
cd /workspace/neurospectra/frontend
npm install
npm run dev
```

Open the printed local URL (usually `http://127.0.0.1:5173`).

### Project Structure

```
neurospectra/
  backend/
    app/
      main.py
      schemas.py
      models/
        model_manager.py
        eeg_model.py
        av_model.py
        game_model.py
        combined_model.py
      utils/
        eeg_features.py
        audio_features.py
        video_features.py
        game_features.py
        feedback.py
    requirements.txt
    README.md
  frontend/
    index.html
    vite.config.ts
    tsconfig.json
    package.json
    src/
      main.tsx
      App.tsx
      services/api.ts
      components/
        EEGUpload.tsx
        AVUpload.tsx
        GameAssessment.tsx
        Results.tsx
    README.md
  .gitignore
```

### Notes

- Models are trained on small synthetic data at first run if no local artifacts exist. Replace with real pre‑recorded datasets and re‑train in `app/models/*` as needed.
- Audio/Video processing uses lightweight features (MFCCs, face detection via OpenCV Haar cascades, motion energy). For production, integrate stronger models.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
