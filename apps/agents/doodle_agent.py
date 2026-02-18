from .intent_extractor import extract_intent
from .evidence_engine import gather_evidence
from .compound_generator import generate_compound_strategy
from .risk_assessor import assess_risk
from .synthesizer import generate_final_report

def run_doodle_agent(query):
    intent = extract_intent(query)
    evidence = gather_evidence("Alzheimer", "Minocycline")
    compound_plan = generate_compound_strategy(intent, evidence)
    risks = assess_risk(evidence)

    report = generate_final_report(
        query, intent, evidence, compound_plan, risks
    )

    return {
        "report": report,
        "compound_strategy": compound_plan,
        "risks": risks
    }
