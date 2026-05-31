import os
import json
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from custom_objects import FeatureGateLayer, CustomSparseCategoricalLoss

from response_generator import (
    get_ai_insight,
    get_ai_score_explanation,
    get_recovery_suggestion,
)


ARTIFACT_DIR = "artifacts"

MODEL_PATH = os.path.join(ARTIFACT_DIR, "recovery_strategy_model.keras")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "recovery_scaler.pkl")
FEATURE_COLS_PATH = os.path.join(ARTIFACT_DIR, "feature_cols.json")
ID_TO_CLASS_PATH = os.path.join(ARTIFACT_DIR, "id_to_class.json")


model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={
        "FeatureGateLayer": FeatureGateLayer,
        "CustomSparseCategoricalLoss": CustomSparseCategoricalLoss,
    },
    compile=False,
)

scaler = joblib.load(SCALER_PATH)

with open(FEATURE_COLS_PATH, "r") as f:
    feature_cols = json.load(f)

with open(ID_TO_CLASS_PATH, "r") as f:
    id_to_class_raw = json.load(f)

ID_TO_CLASS = {int(k): v for k, v in id_to_class_raw.items()}


def encode_battery_status(status):
    status = str(status).lower().strip()

    if status == "low":
        return 0
    elif status == "medium":
        return 1
    elif status == "high":
        return 2

    return 1


def find_free_slots(events, min_gap_minutes=15):
    if not events or len(events) < 2:
        return []

    event_df = pd.DataFrame(events)

    if "startTime" not in event_df.columns or "endTime" not in event_df.columns:
        return []

    event_df["startTime"] = pd.to_datetime(event_df["startTime"], errors="coerce")
    event_df["endTime"] = pd.to_datetime(event_df["endTime"], errors="coerce")
    event_df = event_df.dropna(subset=["startTime", "endTime"])
    event_df = event_df.sort_values("startTime").reset_index(drop=True)

    free_slots = []

    for i in range(len(event_df) - 1):
        current_end = event_df.loc[i, "endTime"]
        next_start = event_df.loc[i + 1, "startTime"]

        gap_minutes = int((next_start - current_end).total_seconds() / 60)

        if gap_minutes >= min_gap_minutes:
            free_slots.append({
                "startTime": current_end.isoformat(),
                "endTime": next_start.isoformat(),
                "durationMinutes": gap_minutes,
                "afterEvent": event_df.loc[i, "title"],
                "beforeEvent": event_df.loc[i + 1, "title"],
            })

    return free_slots


def calculate_duration_minutes(start_time, end_time):
    try:
        start = pd.to_datetime(start_time, errors="coerce")
        end = pd.to_datetime(end_time, errors="coerce")

        if pd.isna(start) or pd.isna(end):
            return 0

        duration = int((end - start).total_seconds() / 60)
        return max(duration, 0)
    except Exception:
        return 0


def select_movable_events(events, max_events=3):
    if not events:
        return []

    movable_events = []

    flexible_keywords = [
        "rapat",
        "meeting",
        "diskusi",
        "nugas",
        "tugas",
        "review",
        "belajar",
        "organisasi",
        "capstone",
        "revisi",
        "project",
        "kelompok",
    ]

    fixed_keywords = [
        "kelas",
        "kuliah",
        "ujian",
        "exam",
        "bimbingan",
        "sidang",
        "presentasi",
        "seminar",
    ]

    for event in events:
        title = str(event.get("title", "")).lower()
        event_type = str(event.get("eventType", "")).lower()

        is_movable = event.get("isMovable", False)

        duration = event.get("durationMinutes", None)

        if duration is None:
            duration = calculate_duration_minutes(
                event.get("startTime", ""),
                event.get("endTime", ""),
            )

        try:
            duration = int(duration)
        except Exception:
            duration = 0

        is_flexible_by_title = any(keyword in title for keyword in flexible_keywords)
        is_fixed_by_title = any(keyword in title for keyword in fixed_keywords)

        is_flexible_by_type = event_type in [
            "meeting",
            "task",
            "assignment",
            "discussion",
            "organization",
            "personal",
        ]

        if is_movable:
            event["durationMinutes"] = duration
            movable_events.append(event)

        elif not is_fixed_by_title and (
            duration >= 60 or is_flexible_by_title or is_flexible_by_type
        ):
            event["durationMinutes"] = duration
            movable_events.append(event)

    return movable_events[:max_events]

def extract_features(ai_payload):
    events = ai_payload.get("events", [])

    free_slots = find_free_slots(events, min_gap_minutes=15)
    movable_events = select_movable_events(events, max_events=3)

    has_recovery_slot = 1 if len(free_slots) > 0 else 0

    max_free_slot_minutes = max(
        [slot["durationMinutes"] for slot in free_slots],
        default=0,
    )

    movable_events_count = len(movable_events)

    features = {
        "battery_score": float(ai_payload.get("batteryScore", 50)),
        "battery_status_encoded": encode_battery_status(
            ai_payload.get("batteryStatus", "medium")
        ),
        "total_events": int(ai_payload.get("totalEvents", 0)),
        "total_duration_minutes": float(ai_payload.get("totalDurationMinutes", 0)),
        "social_intensity_score": float(ai_payload.get("socialIntensityScore", 0)),
        "has_recovery_slot": has_recovery_slot,
        "max_free_slot_minutes": float(max_free_slot_minutes),
        "movable_events_count": int(movable_events_count),
    }

    return features, free_slots, movable_events


def rule_based_safety_override(ai_payload, recovery_strategy):
    total_events = int(ai_payload.get("totalEvents", 0))
    total_duration = float(ai_payload.get("totalDurationMinutes", 0))
    battery_score = float(ai_payload.get("batteryScore", 50))
    battery_status = str(ai_payload.get("batteryStatus", "medium")).lower().strip()

    
    if battery_status == "low" or battery_score < 50:
        return "RESCHEDULE_ACTIVITY"

    
    if battery_status == "medium" or 50 <= battery_score < 80:
        return "TAKE_BREAK"

   
    if battery_status == "high" or battery_score >= 80:
        return "LIGHT_RECOVERY"

 
    if total_events == 0 and total_duration == 0:
        return "LIGHT_RECOVERY"

    return recovery_strategy


def predict_social_battery_response(ai_payload):
    features, free_slots, movable_events = extract_features(ai_payload)

    input_df = pd.DataFrame([features])
    input_df = input_df[feature_cols]

    input_scaled = scaler.transform(input_df)

    pred_prob = model.predict(input_scaled, verbose=0)[0]

    pred_idx = int(np.argmax(pred_prob))
    recovery_strategy = ID_TO_CLASS[pred_idx]

    recovery_strategy = rule_based_safety_override(
        ai_payload,
        recovery_strategy,
    )

    ai_insight = get_ai_insight(ai_payload)
    ai_score_explanation = get_ai_score_explanation(ai_payload)

    recovery_suggestion = get_recovery_suggestion(
        ai_payload=ai_payload,
        recovery_strategy=recovery_strategy,
        free_slots=free_slots,
        movable_events=movable_events,
    )

    return {
        "aiInsight": ai_insight,
        "aiScoreExplanation": ai_score_explanation,
        "recoverySuggestion": recovery_suggestion if isinstance(recovery_suggestion, str) else None,
        "aiModelName": "mlp-recovery-strategy-v3",
    }