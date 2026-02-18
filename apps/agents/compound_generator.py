import json
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


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
        response = model.generate_content(prompt)
        text_output = response.text.strip()

        # Attempt safe JSON parsing
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
