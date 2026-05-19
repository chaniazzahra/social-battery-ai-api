from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import joblib
import json
from tensorflow.keras.models import load_model


app = FastAPI(title="Social Battery AI Service")


MODEL_PATH = "artifacts/recovery_strategy_model.keras"
SCALER_PATH = "artifacts/recovery_scaler.pkl"
FEATURE_COLS_PATH = "artifacts/feature_cols.json"
LABEL_CLASSES_PATH = "artifacts/label_classes.json"


recovery_model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

with open(FEATURE_COLS_PATH, "r") as f:
    feature_cols = json.load(f)

with open(LABEL_CLASSES_PATH, "r") as f:
    label_classes = json.load(f)


class CalendarEvent(BaseModel):
    title: str
    startTime: str
    endTime: str
    attendeeCount: Optional[int] = 1
    location: Optional[str] = None
    eventType: Optional[str] = None


class SocialBatteryAIPayload(BaseModel):
    totalEvents: int
    totalDurationMinutes: int
    socialIntensityScore: float
    batteryScore: float
    batteryStatus: str
    events: List[CalendarEvent] = []


def parse_datetime(value):
    return pd.to_datetime(value)


def calculate_event_duration_minutes(event):
    start = parse_datetime(event["startTime"])
    end = parse_datetime(event["endTime"])
    duration = (end - start).total_seconds() / 60
    return max(0, int(duration))


def encode_battery_status(status):
    status = str(status).lower()

    if status == "low":
        return 0
    elif status == "medium":
        return 1
    elif status == "high":
        return 2

    return 1


def normalize_battery_status(status):
    status = str(status).lower()

    if status == "low":
        return "LOW"
    elif status == "medium":
        return "MEDIUM"
    elif status == "high":
        return "HIGH"

    return "MEDIUM"


def find_free_slots_from_be_events(events, min_gap_minutes=15):
    if events is None or len(events) == 0:
        return []

    sorted_events = sorted(events, key=lambda x: parse_datetime(x["startTime"]))
    free_slots = []

    for i in range(len(sorted_events) - 1):
        current_end = parse_datetime(sorted_events[i]["endTime"])
        next_start = parse_datetime(sorted_events[i + 1]["startTime"])

        gap_minutes = int((next_start - current_end).total_seconds() / 60)

        if gap_minutes >= min_gap_minutes:
            free_slots.append({
                "startTime": current_end,
                "endTime": next_start,
                "durationMinutes": gap_minutes,
                "afterEvent": sorted_events[i]["title"],
                "beforeEvent": sorted_events[i + 1]["title"]
            })

    return free_slots


def select_movable_events_from_be(events, max_events=3):
    if events is None or len(events) == 0:
        return []

    non_movable_keywords = [
        "daily", "standup", "sprint", "planning", "meeting",
        "client", "exam", "ujian", "kelas", "lecture",
        "interview", "deadline", "sidang", "presentasi"
    ]

    movable_events = []

    for event in events:
        title = str(event.get("title", "")).lower()
        is_non_movable = any(keyword in title for keyword in non_movable_keywords)

        if not is_non_movable:
            movable_events.append(event)

    if len(movable_events) == 0:
        movable_events = events

    movable_events = sorted(
        movable_events,
        key=lambda x: calculate_event_duration_minutes(x),
        reverse=True
    )

    return movable_events[:max_events]


def format_time_from_datetime(dt):
    return pd.to_datetime(dt).strftime("%H:%M")


def join_event_titles(events):
    titles = []

    for event in events:
        start = format_time_from_datetime(event["startTime"])
        end = format_time_from_datetime(event["endTime"])
        titles.append(f"{event['title']} ({start}-{end})")

    if len(titles) == 0:
        return ""

    if len(titles) == 1:
        return titles[0]

    if len(titles) == 2:
        return f"{titles[0]} dan {titles[1]}"

    return f"{titles[0]}, {titles[1]}, dan {titles[2]}"


def extract_features_from_ai_payload(ai_payload):
    events = ai_payload.get("events", [])

    free_slots = find_free_slots_from_be_events(events, min_gap_minutes=15)

    has_recovery_slot = 1 if len(free_slots) > 0 else 0

    max_free_slot_minutes = max(
        [slot["durationMinutes"] for slot in free_slots],
        default=0
    )

    movable_events = select_movable_events_from_be(events, max_events=3)

    return {
        "batteryScore": float(ai_payload["batteryScore"]),
        "batteryStatusEncoded": encode_battery_status(ai_payload["batteryStatus"]),
        "totalEvents": int(ai_payload["totalEvents"]),
        "totalDurationMinutes": float(ai_payload["totalDurationMinutes"]),
        "socialIntensityScore": float(ai_payload["socialIntensityScore"]),
        "hasRecoverySlot": has_recovery_slot,
        "maxFreeSlotMinutes": float(max_free_slot_minutes),
        "movableEventsCount": int(len(movable_events))
    }


def predict_recovery_strategy_from_payload(ai_payload):
    features = extract_features_from_ai_payload(ai_payload)

    input_df = pd.DataFrame([{
        "battery_score": features["batteryScore"],
        "battery_status_encoded": features["batteryStatusEncoded"],
        "total_events": features["totalEvents"],
        "total_duration_minutes": features["totalDurationMinutes"],
        "social_intensity_score": features["socialIntensityScore"],
        "has_recovery_slot": features["hasRecoverySlot"],
        "max_free_slot_minutes": features["maxFreeSlotMinutes"],
        "movable_events_count": features["movableEventsCount"]
    }])

    input_df = input_df[feature_cols]
    input_scaled = scaler.transform(input_df)

    pred_prob = recovery_model.predict(input_scaled, verbose=0)
    pred_idx = int(np.argmax(pred_prob[0]))

    return label_classes[pred_idx]


def generate_ai_insight(ai_payload):
    battery_status = normalize_battery_status(ai_payload["batteryStatus"])

    total_events = int(ai_payload["totalEvents"])
    total_duration = int(ai_payload["totalDurationMinutes"])

    if battery_status == "HIGH":
        return (
            f"🍯🧸 Energi sosialmu terlihat sangat baik hari ini. Walaupun ada {total_events} agenda "
            f"({total_duration} menit) hari ini, kamu terlihat punya cukup energi untuk menjalani semuanya dengan nyaman. "
            f"Semoga harimu menyenangkan, ya! 🤎✨"
        )

    if battery_status == "MEDIUM":
        return (
            f" ☕🎧 Energi sosialmu sedang berada di titik tengah nih. Hari ini kamu memiliki {total_events} kegiatan "
            f"({total_duration} menit) yang mengisi harimu. Wajar kalau mulai terasa sedikit lelah, "
            f"tapi tenang saja, kamu punya kendali penuh untuk menyisipkan jeda dan memulihkan diri. 🤎🪴"
        )

    return (
        f"🕯️📖 Sepertinya energi sosialmu sedang butuh diisi ulang. Dengan {total_events} agenda "
        f"yang memakan waktu {total_duration} menit hari ini, sangat wajar kalau kamu merasa kewalahan. "
        f"Tapi, nggak apa-apa banget lho kalau kamu mau istirahat sebentar. "
        f"Kamu sudah melakukan yang terbaik untuk hari ini, jadi luangkan waktumu untuk recharge energimu terlebih dahulu yaa. 🤎🛋️"
    )


def generate_ai_score_explanation(ai_payload):
    battery_score = float(ai_payload["batteryScore"])
    battery_status = normalize_battery_status(ai_payload["batteryStatus"])

    total_events = int(ai_payload["totalEvents"])
    total_duration = int(ai_payload["totalDurationMinutes"])
    social_intensity = float(ai_payload["socialIntensityScore"])

    return (
        f"Catatan hari ini menunjukkan energi sosialmu berada [pada skor {battery_score:.2f}/100 ({battery_status}). "
        f"Dengan {total_events} kegiatanmu yang berdurasi ({total_duration} menit) dan tingkat interaksi di level {social_intensity:.2f}, "
        f"Catatan ini menjadi rekapan kecil dari rutinitas sosialmu hari ini. "
        f"Bagaimanapun kondisimu saat ini, pastikan kamu tetap nyaman dan mengambil jeda sejenak yaa. 🧸🤎"
    )


def generate_recovery_suggestion_from_strategy(ai_payload, recovery_strategy):
    battery_status = normalize_battery_status(ai_payload["batteryStatus"])
    events = ai_payload.get("events", [])

    free_slots = find_free_slots_from_be_events(events, min_gap_minutes=15)

    if recovery_strategy in ["LIGHT_RECOVERY", "TAKE_BREAK"] and len(free_slots) > 0:
        best_slot = max(free_slots, key=lambda x: x["durationMinutes"])
        recovery_duration = min(30, best_slot["durationMinutes"])

        start = format_time_from_datetime(best_slot["startTime"])
        end = format_time_from_datetime(best_slot["endTime"])

        if recovery_strategy == "LIGHT_RECOVERY":
            return (
                f"Energi sosialmu masih terjaga dengan baik! Yuk, beri dirimu hadiah istirahat ringan "
                f"di sela-sela waktu {start}–{end} setelah {best_slot['afterEvent']}. "
                f"Jeda sekitar 15 menit ini sangat berarti agar kamu punya ketenangan penuh "
                f"untuk menghadapi aktivitas  {best_slot['beforeEvent']} nanti. ☕🎧"
            )

        return (
            f"Yuk, ambil napas sejenak. Ada waktu luang sekitar {recovery_duration} menit nih "
            f"di jam {start}–{end}, tepat setelah {best_slot['afterEvent']}. Sebelum lanjut ke "
            f"{best_slot['beforeEvent']}, kamu bisa pakai waktu ini untuk duduk manis, menjauh dari layar, "
            f"atau sekadar menikmati momen tenang tanpa harus berinteraksi. 🕯️📖"
        )

    movable_events = select_movable_events_from_be(events, max_events=3)
    move_text = join_event_titles(movable_events)

    if recovery_strategy == "RESCHEDULE_ACTIVITY" or battery_status == "LOW":
        if move_text:
            return (
                f"Sepertinya hari ini jadwalmu cukup padat dan energimu butuh diisi ulang. 🧸🤎 "
                f"Demi kebaikanmu, bagaimana kalau kita pindahkan {move_text} ke hari lain "
                f"yang lebih luang? Memberi ruang untuk dirimu sendiri beristirahat itu langkah yang hebat, lho. 🛋️✨"
            )

        return (
            "Saat ini energi sosialmu sedang sangat terbatas. 🕯️🤎 "
            "Yuk, kurangi interaksi sosial yang tidak mendesak, "
            "jauhkan diri dari notifikasi sejenak, dan prioritaskan ketenanganmu hari ini. 🛌💤"
        )

    return (
        "Jangan lupa untuk selalu menyelipkan senyum dan jeda kecil di antara aktivitasmu ya, "
        "agar energi baikmu slalu terjaga. 🍯🧸"
    )


def generate_social_battery_insight_from_be_payload(ai_payload):
    recovery_strategy = predict_recovery_strategy_from_payload(ai_payload)

    return {
        "aiInsight": generate_ai_insight(ai_payload),
        "aiScoreExplanation": generate_ai_score_explanation(ai_payload),
        "recoverySuggestion": generate_recovery_suggestion_from_strategy(
            ai_payload,
            recovery_strategy
        ),
        "aiModelName": "mlp-recovery-strategy-v1"
    }


@app.get("/")
def home():
    return {
        "message": "Social Battery AI Service is running",
        "model": "mlp-recovery-strategy-v1"
    }


@app.post("/social-battery/insight")
def social_battery_insight(payload: SocialBatteryAIPayload):
    ai_payload = payload.model_dump()
    return generate_social_battery_insight_from_be_payload(ai_payload)