import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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

    response = model.generate_content(prompt)
    return response.text
