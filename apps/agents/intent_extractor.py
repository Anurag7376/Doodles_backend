import json
import re
import logging
from typing import Dict

import google.generativeai as genai
from django.conf import settings


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _clean_response_text(text: str) -> str:
    """
    Removes markdown code fences and trims whitespace.
    """
    if not text:
        return ""

    # Remove ```json and ``` wrappers
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)
    return text.strip()


def _extract_json_block(text: str) -> str:
    """
    Extracts the first JSON object found in text.
    Handles cases where model adds explanations before/after JSON.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else ""


def _default_fallback() -> Dict:
    """
    Safe fallback structure to prevent orchestrator crashes.
    """
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
    """
    Extract structured scientific intent from user query.

    Always returns a dictionary.
    Never raises exceptions.
    """

    if not query:
        return _default_fallback()

    prompt = f"""
    Extract structured scientific intent from the query below.

    Required JSON keys:
    - disease
    - compound
    - improvement
    - stage

    Rules:
    - Return ONLY valid JSON.
    - No markdown.
    - No explanations.
    - No text outside JSON.

    Query:
    {query}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = getattr(response, "text", "") or ""

        cleaned = _clean_response_text(raw_text)
        json_block = _extract_json_block(cleaned)

        if not json_block:
            logger.warning("No JSON block found in model output.")
            return _default_fallback()

        parsed = json.loads(json_block)

        # Ensure required keys exist
        return {
            "disease": parsed.get("disease", "unknown"),
            "compound": parsed.get("compound", "unknown"),
            "improvement": parsed.get("improvement", "unspecified"),
            "stage": parsed.get("stage", "research"),
        }

    except Exception as e:
        logger.error(f"Intent extraction failed: {str(e)}")
        return _default_fallback()
