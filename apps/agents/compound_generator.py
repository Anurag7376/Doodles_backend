import json
from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _get_text(response):
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


def generate_compound_strategy(intent_data, evidence, research_stage=None):
    """
    Generates compound optimization strategy based on:
    - Disease
    - Target compound
    - Mechanism
    - Evidence
    - Current research stage
    """

    disease = intent_data.get("disease", "Unknown")
    compound = intent_data.get("compound", "Unknown")
    mechanism = intent_data.get("mechanism", "Not specified")

    prompt = f"""
You are Doodle, an autonomous pharmaceutical compound optimization AI.

Disease: {disease}
Base Compound: {compound}
Mechanism of Action: {mechanism}
Research Stage: {research_stage}

Evidence Summary:
{evidence}

Task:
1. Propose structural modifications.
2. Suggest pharmacokinetic improvements.
3. Suggest safety improvements.
4. Suggest synergistic combination strategies.
5. Suggest formulation strategy.

Respond ONLY in JSON format:

{{
    "suggested_modifications": ["..."],
    "pharmacokinetic_optimization": "...",
    "safety_optimization": "...",
    "combination_strategy": "...",
    "formulation_strategy": "...",
    "rationale": "..."
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        text_output = _get_text(response).strip()
        return json.loads(text_output)

    except Exception as e:
        return {
            "suggested_modifications": [],
            "pharmacokinetic_optimization": "Error generating optimization",
            "safety_optimization": "Error generating optimization",
            "combination_strategy": "Error generating optimization",
            "formulation_strategy": "Error generating optimization",
            "rationale": str(e)
        }
