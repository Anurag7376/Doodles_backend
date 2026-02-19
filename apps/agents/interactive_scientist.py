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


def generate_scientific_response(session, user_input, evidence, memory):
    stage = getattr(session, "research_stage", "exploration")
    previous_hypothesis = getattr(session, "current_hypothesis", "")

    prompt = f"""
You are Doodle, an autonomous pharmaceutical research AI.

Current Stage: {stage}

User Input:
{user_input}

Previous Hypothesis:
{previous_hypothesis}

Evidence:
{evidence}

Memory:
{memory}

Perform:
1. Scientific reasoning
2. Evaluate mechanisms
3. Identify compound optimization
4. Assess risk
5. Propose estimated chemical composition
6. Provide structured output

Respond in JSON:
{{
  "analysis": "...",
  "hypothesis": "...",
  "proposed_compounds": ["..."],
  "mechanism": "...",
  "risk_assessment": "...",
  "confidence": "low/medium/high"
}}
        """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return _get_text(response)
