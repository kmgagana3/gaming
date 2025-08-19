from __future__ import annotations

import io
import wave
import numpy as np
from typing import Dict


def _read_wav_bytes_pcm16(wav_bytes: bytes) -> tuple[np.ndarray, int]:
    with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
        num_channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        num_frames = wf.getnframes()
        raw = wf.readframes(num_frames)
        if num_channels == 0 or sample_rate == 0 or len(raw) == 0:
            return np.array([], dtype=float), 0
        audio = np.frombuffer(raw, dtype=np.int16)
        if num_channels > 1:
            audio = audio.reshape(-1, num_channels).mean(axis=1)
        audio = audio.astype(np.float32) / 32768.0
        return audio, sample_rate


def extract_audio_features(wav_bytes: bytes) -> Dict[str, float]:
    try:
        data, sr = _read_wav_bytes_pcm16(wav_bytes)
    except wave.Error:
        return {}
    if sr == 0 or data.size == 0:
        return {}

    rms = float(np.sqrt(np.mean(np.square(data))))
    zero_crossings = np.where(np.diff(np.signbit(data)))[0]
    zcr = float(len(zero_crossings) / max(1, data.size))
    spectrum = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(data.size, 1.0 / sr)
    dom_idx = int(np.argmax(spectrum))
    dom_freq = float(freqs[dom_idx]) if dom_idx < freqs.size else 0.0

    return {"rms": rms, "zcr": zcr, "dom_freq": dom_freq}

