import threading
from app.services.collect_answers import save_answers_jsonl
from app.services.collect_answers import extract_answers_from_context
from app.services.severity_predictor import SeverityPredictor
from app.services.care_tip_handlers import run_rag_async
from app.config import globals

DESIRED_KEYS = [
    "pain_type",
    "radiates",
    "duration",
    "self_score",
    "activity_score",
    "mood_score",
    "sleep_score"
]

def handle_submit(body):
    answers = extract_answers_from_context(body, "pain_assessment")
    user_input_dict = {k: answers[k] for k in DESIRED_KEYS if k in answers}

    # Ensure numeric fields are int, not str
    for key in ["self_score", "activity_score", "mood_score", "sleep_score"]:
        if key in user_input_dict:
            user_input_dict[key] = int(user_input_dict[key])

    # Predict severity using only allowed fields
    # Initialize Severity Predictor
    predictor = SeverityPredictor()
    severity_score = predictor.predict(user_input_dict)
    user_input_dict["predicted_severity_score"] = severity_score

    # Save to JSONL
    save_answers_jsonl(user_input_dict)

    # Run RAG asynchronously
    if globals.RAG_AVAILABLE:
        session_id = body.get("session", "").split("/")[-1]
        care_tip_uuid = body.get("care_tip_uuid", "")
        threading.Thread(
            target=run_rag_async,
            args=(session_id, care_tip_uuid, severity_score),
            daemon=True
        ).start()

    # Respond to Dialogflow
    return [
        f"Thank you! Your assessment has been submitted. Your severity level is {severity_score}/5.\n\n"
    ]