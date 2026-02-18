import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_intent(query):
    prompt = f"""
    Extract structured information:

    - Target disease
    - Base compound (if any)
    - Desired improvement (efficacy, toxicity, solubility, etc.)
    - Development stage (research, clinical, market-ready)

    Query: {query}

    Return JSON.
    """
    response = model.generate_content(prompt)
    return response.text
