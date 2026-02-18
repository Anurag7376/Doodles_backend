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


def generate_final_report(query, intent, evidence, compound_plan, risks):
    prompt = f"""
    Generate a startup-ready pharmaceutical proposal.

    Include:

    1. Problem Summary
    2. Evidence Overview
    3. Compound Optimization Strategy
    4. Risk & Safety Notes
    5. Estimated Development Path
    6. Commercial Feasibility
    7. References (PMID numbers)

    Data:
    Intent: {intent}
    Evidence: {evidence}
    Compound Plan: {compound_plan}
    Risks: {risks}

    Keep it practical and actionable.
        """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return _get_text(response)
