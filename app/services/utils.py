import os
import json
import logging

logger = logging.getLogger(__name__)


def to_severity_score(predicted_label: int) -> int:
    return int(predicted_label) + 1

def save_refined_care_tip(session_id: str, uuid: str, response) -> None:
    # Save to file
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(current_dir, "care_tip_cache")
        os.makedirs(cache_dir, exist_ok=True)

        cache_path = os.path.join(cache_dir, f"{session_id}-{uuid}.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved RAG care tip to {cache_path}")
    except Exception as file_err:
        logger.warning(f"Failed to save care tip to file: {file_err}")

def read_refined_care_tip(session_id: str, uuid: str):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(current_dir, "care_tip_cache")
        cache_path = os.path.join(cache_dir, f"{session_id}-{uuid}.json")

        if not os.path.exists(cache_path):
            logger.warning(f"No care tip file found for session: {session_id}")
            return None

        with open(cache_path, "r", encoding="utf-8") as f:
            care_tip = json.load(f)

        logger.info(f"Loaded care tip from {cache_path}")
        return care_tip

    except Exception as file_err:
        logger.warning(f"Failed to read care tip from file: {file_err}")
        return None
