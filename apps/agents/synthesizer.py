import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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

    response = model.generate_content(prompt)
    return response.text
