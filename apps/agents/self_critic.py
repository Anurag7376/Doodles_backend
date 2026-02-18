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


def critique_and_refine(initial_output):
    prompt = f"""
You are a senior pharmaceutical reviewer.

Review the following research proposal:

{initial_output}

1. Identify weaknesses
2. Improve reasoning
3. Strengthen compound justification
4. Improve risk clarity

Return improved structured JSON.
        """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return _get_text(response)
