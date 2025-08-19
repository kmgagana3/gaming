from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Dict
import numpy as np


MODELS_DIR = Path(__file__).resolve().parent / "artifacts"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def _bounded(value: float) -> float:
    return float(max(0.0, min(1.0, value)))


def _load_weights(name: str) -> Dict[str, float]:
    path = MODELS_DIR / f"{name}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    # default small weights for demo; could be learned on first run
    weights = {"bias": 0.1}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(weights, f)
    return weights


def eeg_model_predict(features: Dict[str, float]) -> float:
    weights = _load_weights("eeg_weights")
    bias = weights.get("bias", 0.1)
    # Simple normalized sum over present features
    xs = np.array(list(features.values()), dtype=float)
    if xs.size == 0:
        return 0.5
    score = bias + float(xs.mean()) * 0.5
    return _bounded(score)


def av_model_predict(features: Dict[str, float]) -> float:
    weights = _load_weights("av_weights")
    bias = weights.get("bias", 0.1)
    xs = np.array(list(features.values()), dtype=float)
    if xs.size == 0:
        return 0.5
    score = bias + float(xs.std()) * 0.6
    return _bounded(score)


def game_model_predict(features: Dict[str, float]) -> float:
    weights = _load_weights("game_weights")
    bias = weights.get("bias", 0.1)
    # Reaction time mean and error rate play larger roles
    rt_mean = features.get("rt_mean", 0.0)
    error_rate = features.get("emotion_error_rate", 0.0)
    gaze_var = features.get("gaze_var", 0.0)
    score = bias + 0.5 * error_rate + 0.3 * rt_mean + 0.2 * gaze_var
    return _bounded(score)


def combined_model_predict(eeg_score: float, av_score: float, game_score: float) -> float:
    # Weighted fusion; tune as desired
    weights = np.array([0.4, 0.3, 0.3])
    scores = np.array([eeg_score, av_score, game_score])
    score = float((weights * scores).sum())
    return _bounded(score)

