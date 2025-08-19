from __future__ import annotations

import io
from typing import Dict

import numpy as np
import pandas as pd


def bandpower(signal: np.ndarray, fs: float, low: float, high: float) -> float:
    if signal.size == 0:
        return 0.0
    freqs = np.fft.rfftfreq(signal.size, d=1.0 / fs)
    spectrum = np.abs(np.fft.rfft(signal)) ** 2
    mask = (freqs >= low) & (freqs <= high)
    power = float(spectrum[mask].sum())
    total = float(spectrum.sum()) + 1e-9
    return power / total


def extract_eeg_features_from_csv_bytes(csv_bytes: bytes, fs: float = 256.0) -> Dict[str, float]:
    df = pd.read_csv(io.BytesIO(csv_bytes))
    # Expect multiple EEG channels as columns; compute relative band powers
    values = df.select_dtypes(include=["number"]).to_numpy()
    if values.size == 0:
        return {}
    features: Dict[str, float] = {}
    for channel_index in range(values.shape[1]):
        channel = values[:, channel_index].astype(float)
        features[f"ch{channel_index}_delta"] = bandpower(channel, fs, 0.5, 4)
        features[f"ch{channel_index}_theta"] = bandpower(channel, fs, 4, 8)
        features[f"ch{channel_index}_alpha"] = bandpower(channel, fs, 8, 13)
        features[f"ch{channel_index}_beta"] = bandpower(channel, fs, 13, 30)
        features[f"ch{channel_index}_gamma"] = bandpower(channel, fs, 30, 45)
    # Simple global stats
    features["global_std"] = float(values.std())
    kurt_series = pd.DataFrame(values).kurtosis(skipna=True)
    features["global_kurt"] = float(kurt_series.mean()) if hasattr(kurt_series, "mean") else float(kurt_series)
    return features

