from __future__ import annotations

import io
import tempfile
from typing import Dict

import imageio.v3 as iio
import numpy as np


def extract_video_features(video_bytes: bytes) -> Dict[str, float]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    try:
        frames_iter = iio.imiter(tmp_path, plugin="FFMPEG")
    except Exception:
        return {}

    motion_sum = 0.0
    total_frames = 0
    prev_gray: np.ndarray | None = None
    face_ratio_proxy = 0.0  # placeholder without OpenCV face detector

    for frame in frames_iter:
        total_frames += 1
        if frame.ndim == 3 and frame.shape[2] == 3:
            gray = np.mean(frame, axis=2).astype(np.float32)
        else:
            gray = frame.astype(np.float32)
        if prev_gray is not None:
            diff = np.abs(gray - prev_gray)
            motion_sum += float(diff.mean())
        prev_gray = gray

    if total_frames == 0:
        return {}
    motion_avg = motion_sum / max(1, total_frames - 1)
    return {"face_ratio": float(face_ratio_proxy), "motion_avg": float(motion_avg)}

