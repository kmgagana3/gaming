from __future__ import annotations

from typing import Dict
import numpy as np

from ..schemas import GameAssessmentRequest


def extract_game_features(payload: GameAssessmentRequest) -> Dict[str, float]:
    reaction = np.array(payload.reactionTimesMs, dtype=float)
    rt_mean = float(reaction.mean()) if reaction.size else 0.0
    rt_std = float(reaction.std()) if reaction.size else 0.0
    error_rate = 1.0 - (payload.correctEmotionSelections / max(1, payload.totalEmotionTrials))
    gaze = np.array(payload.gazeHoldMs, dtype=float)
    gaze_mean = float(gaze.mean()) if gaze.size else 0.0
    gaze_var = float(gaze.var()) if gaze.size else 0.0
    return {
        "rt_mean": rt_mean / 1000.0,  # seconds
        "rt_std": rt_std / 1000.0,
        "emotion_error_rate": float(error_rate),
        "gaze_mean": gaze_mean / 1000.0,
        "gaze_var": gaze_var / (1000.0 ** 2),
        "age": float(payload.ageYears) if payload.ageYears is not None else 0.0,
    }

