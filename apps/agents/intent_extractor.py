import json
import re
import logging
from typing import Dict

from google import genai
from django.conf import settings

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _get_text(response) -> str:
    text = getattr(response, "text", None)
    if text:
        return text
    try:
        return response.output_text
    except Exception:
        pass
    try:
        candidates = getattr(response, "candidates", None) or []
        if candidates:
            parts = getattr(candidates[0].content, "parts", None) or []
            if parts:
                part_text = getattr(parts[0], "text", None)
                if part_text:
                    return part_text
    except Exception:
        pass
    return ""


def _clean_response_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)
    return text.strip()

def _extract_json_block(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else ""

def _default_fallback() -> Dict:
    return {
        "disease": "unknown",
        "compound": "unknown",
        "improvement": "unspecified",
        "stage": "research"
    }

# ---------------------------------------------------------
# Main Intent Extraction Function
# ---------------------------------------------------------

def extract_intent(query: str) -> Dict:
    if not query:
        return _default_fallback()

    prompt = f"""
    Extract structured scientific intent from the query below.
    Required JSON keys: disease, compound, improvement, stage.
    Rules: Return ONLY valid JSON. No markdown. No explanations.
    
    Query: {query}
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        raw_text = _get_text(response) or ""

        cleaned = _clean_response_text(raw_text)
        json_block = _extract_json_block(cleaned)

        if not json_block:
            logger.warning("No JSON block found in model output.")
            return _default_fallback()

        parsed = json.loads(json_block)

        return {
            "disease": parsed.get("disease", "unknown"),
            "compound": parsed.get("compound", "unknown"),
            "improvement": parsed.get("improvement", "unspecified"),
            "stage": parsed.get("stage", "research"),
        }

    except Exception as e:
        logger.error(f"Intent extraction failed: {str(e)}")
        return _default_fallback()
