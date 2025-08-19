from __future__ import annotations

from ..schemas import FeedbackRequest


def generate_feedback(payload: FeedbackRequest) -> str:
    p = payload.probability
    age = payload.ageYears
    age_str = f" for age {age:.1f}y" if age is not None else ""
    if p < 0.33:
        return (
            f"Estimated low ASD risk{age_str}. Consider routine monitoring and supportive learning activities. "
            "If concerns persist, consult a pediatrician."
        )
    if p < 0.66:
        return (
            f"Estimated moderate ASD risk{age_str}. Schedule a screening with a specialist, and explore early ".strip()
            + " interventions such as social skills training and speech-language evaluation."
        )
    return (
        f"Estimated elevated ASD risk{age_str}. Please seek a comprehensive developmental assessment with a qualified "
        "clinician. Early intervention (ABA-based approaches, speech/OT) can improve outcomes."
    )

