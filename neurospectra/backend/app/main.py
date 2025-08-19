from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional

from .schemas import (
    EEGPredictionResponse,
    AVPredictionResponse,
    GameAssessmentRequest,
    GamePredictionResponse,
    CombinedPredictRequest,
    CombinedPredictionResponse,
    FeedbackRequest,
    FeedbackResponse,
)
from .utils.eeg_features import extract_eeg_features_from_csv_bytes
from .utils.audio_features import extract_audio_features
from .utils.video_features import extract_video_features
from .utils.game_features import extract_game_features
from .utils.feedback import generate_feedback
from .models.model_manager import (
    eeg_model_predict,
    av_model_predict,
    game_model_predict,
    combined_model_predict,
)


app = FastAPI(title="NeuroSpectra API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/eeg/predict", response_model=EEGPredictionResponse)
async def eeg_predict(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        return JSONResponse(status_code=400, content={"detail": "Please upload a CSV file"})

    csv_bytes = await file.read()
    features = extract_eeg_features_from_csv_bytes(csv_bytes)
    score = eeg_model_predict(features)
    return EEGPredictionResponse(probability=score, features=features)


@app.post("/api/av/predict", response_model=AVPredictionResponse)
async def av_predict(
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
):
    if audio is None and video is None:
        return JSONResponse(status_code=400, content={"detail": "Upload at least audio or video"})

    audio_features = None
    if audio is not None:
        audio_bytes = await audio.read()
        audio_features = extract_audio_features(audio_bytes)

    video_features = None
    if video is not None:
        video_bytes = await video.read()
        video_features = extract_video_features(video_bytes)

    merged_features = {}
    if audio_features:
        merged_features.update({f"audio_{k}": v for k, v in audio_features.items()})
    if video_features:
        merged_features.update({f"video_{k}": v for k, v in video_features.items()})

    score = av_model_predict(merged_features)
    return AVPredictionResponse(probability=score, features=merged_features)


@app.post("/api/game/submit", response_model=GamePredictionResponse)
async def game_submit(payload: GameAssessmentRequest):
    features = extract_game_features(payload)
    score = game_model_predict(features)
    return GamePredictionResponse(probability=score, features=features)


@app.post("/api/combined/predict", response_model=CombinedPredictionResponse)
async def combined_predict(payload: CombinedPredictRequest):
    score = combined_model_predict(payload.eeg_score, payload.av_score, payload.game_score)
    return CombinedPredictionResponse(probability=score)


@app.post("/api/feedback", response_model=FeedbackResponse)
async def feedback(payload: FeedbackRequest):
    text = generate_feedback(payload)
    return FeedbackResponse(feedback=text)

