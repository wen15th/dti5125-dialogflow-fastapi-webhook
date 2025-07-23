import json
import logging

from app.services.utils import read_refined_care_tip, save_refined_care_tip
from app.services.pain_handlers import handle_pain_report
from app.services.collect_answers import extract_answers_from_context

logger = logging.getLogger(__name__)


def handle_care_tip(body):
    session_id = body.get("session", "").split("/")[-1]
    context = extract_answers_from_context(body, "awaiting_care_tip")
    uuid = context.get("care_tip_uuid", "")

    logger.info(f"Reading from saved care-tip file, session_id: {session_id}, uuid: {uuid}")

    care_tips = read_refined_care_tip(session_id, uuid)
    if not care_tips:
        return {
            "fulfillmentText": "Sorry, failed to retrieve care tip. Please try again later.",
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["Sorry, failed to retrieve care tip. Please try again later."]
                    }
                }
            ],
        }

    # Return saved care tips
    return care_tips


def run_rag_async(session_id: str, uuid: str, severity_score: int):
    try:
        logger.info(f"[RAG async] start processing, session_id: {session_id}, uuid: {uuid}, severity_score: {severity_score}")
        result = handle_pain_report({
            "queryResult": {
                "parameters": {
                    "severity_score": severity_score,
                    "symptom": "pain"
                },
            },
            "session": session_id,
        })

        logger.info(f"[RAG async] result: {json.dumps(result, ensure_ascii=False)}")

        # Save care tips
        save_refined_care_tip(session_id, uuid, result)
    except Exception as e:
        logger.error(f"[RAG async] Failed to get care tip: {str(e)}")