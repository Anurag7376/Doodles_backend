import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_scientific_response(session, user_input, evidence, memory):

    prompt = f"""
You are Doodle, an autonomous pharmaceutical research AI.

Current Stage: {session.research_stage}

User Input:
{user_input}

Previous Hypothesis:
{session.current_hypothesis}

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

    response = model.generate_content(prompt)
    return response.text
