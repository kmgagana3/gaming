from __future__ import annotations

import io
from typing import Dict

import numpy as np
import soundfile as sf


def extract_audio_features(wav_bytes: bytes) -> Dict[str, float]:
    data, sr = sf.read(io.BytesIO(wav_bytes))
    if data.ndim > 1:
        data = data.mean(axis=1)
    data = data.astype(float)
    if data.size == 0:
        return {}

    # RMS energy
    rms = float(np.sqrt(np.mean(np.square(data))))
    # Zero crossing rate
    zero_crossings = np.where(np.diff(np.signbit(data)))[0]
    zcr = float(len(zero_crossings) / max(1, data.size))
    # Pitch proxy via dominant frequency
    spectrum = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(data.size, 1.0 / sr)
    dom_idx = int(np.argmax(spectrum))
    dom_freq = float(freqs[dom_idx]) if dom_idx < freqs.size else 0.0

    return {
        "rms": rms,
        "zcr": zcr,
        "dom_freq": dom_freq,
    }

