from __future__ import annotations

import io
import tempfile
from typing import Dict

import cv2
import numpy as np


def _write_temp_video(video_bytes: bytes) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tmp.write(video_bytes)
    tmp.flush()
    tmp.close()
    return tmp.name


def extract_video_features(video_bytes: bytes) -> Dict[str, float]:
    path = _write_temp_video(video_bytes)
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return {}

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    prev_gray = None
    motion_sum = 0.0
    face_frames = 0
    total_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            face_frames += 1
        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            motion_sum += float(diff.mean())
        prev_gray = gray

    cap.release()
    if total_frames == 0:
        return {}

    face_ratio = face_frames / total_frames
    motion_avg = motion_sum / max(1, total_frames - 1)
    return {
        "face_ratio": float(face_ratio),
        "motion_avg": float(motion_avg),
    }

