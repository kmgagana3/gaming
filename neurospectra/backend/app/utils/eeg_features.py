from __future__ import annotations

import io
from typing import Dict, List

import numpy as np


def bandpower(signal: np.ndarray, fs: float, low: float, high: float) -> float:
    if signal.size == 0:
        return 0.0
    freqs = np.fft.rfftfreq(signal.size, d=1.0 / fs)
    spectrum = np.abs(np.fft.rfft(signal)) ** 2
    mask = (freqs >= low) & (freqs <= high)
    power = float(spectrum[mask].sum())
    total = float(spectrum.sum()) + 1e-9
    return power / total


def _read_csv_numeric_matrix(csv_bytes: bytes) -> np.ndarray:
    buf = io.BytesIO(csv_bytes)
    try:
        data = np.genfromtxt(buf, delimiter=",", names=True, dtype=float, encoding=None)
        if isinstance(data, np.ndarray) and data.dtype.names:
            cols: List[np.ndarray] = [np.asarray(data[name], dtype=float) for name in data.dtype.names]
            values = np.vstack(cols).T
        else:
            values = np.atleast_2d(np.asarray(data, dtype=float))
    except Exception:
        buf.seek(0)
        data = np.genfromtxt(buf, delimiter=",", dtype=float)
        values = np.atleast_2d(np.asarray(data, dtype=float))
    # Drop rows with NaNs
    values = values[~np.isnan(values).any(axis=1)]
    return values


def _excess_kurtosis(x: np.ndarray) -> float:
    x = x.astype(float)
    if x.size == 0:
        return 0.0
    mean = float(x.mean())
    std = float(x.std())
    if std == 0.0:
        return 0.0
    m4 = float(np.mean((x - mean) ** 4))
    return m4 / (std ** 4) - 3.0


def extract_eeg_features_from_csv_bytes(csv_bytes: bytes, fs: float = 256.0) -> Dict[str, float]:
    values = _read_csv_numeric_matrix(csv_bytes)
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
    features["global_kurt"] = _excess_kurtosis(values.flatten())
    return features

