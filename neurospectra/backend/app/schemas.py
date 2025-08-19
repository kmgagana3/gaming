from pydantic import BaseModel, Field
from typing import Dict, Optional, List


class EEGPredictionResponse(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)
    features: Dict[str, float]


class AVPredictionResponse(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)
    features: Dict[str, float]


class GameAssessmentRequest(BaseModel):
    # Example payload captured from the frontend mini‑game
    # reactionTimesMs per round, selectedEmotions correctness, gazeHoldMs durations, etc.
    reactionTimesMs: List[float]
    correctEmotionSelections: int
    totalEmotionTrials: int
    gazeHoldMs: List[float]
    ageYears: Optional[float] = None


class GamePredictionResponse(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)
    features: Dict[str, float]


class CombinedPredictRequest(BaseModel):
    eeg_score: float = Field(ge=0.0, le=1.0)
    av_score: float = Field(ge=0.0, le=1.0)
    game_score: float = Field(ge=0.0, le=1.0)


class CombinedPredictionResponse(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)


class FeedbackRequest(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)
    ageYears: Optional[float] = None


class FeedbackResponse(BaseModel):
    feedback: str

