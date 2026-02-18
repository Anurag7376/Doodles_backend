from .intent_extractor import extract_intent
from .evidence_engine import gather_evidence
from .interactive_scientist import generate_scientific_response
from apps.chat.models import ResearchMemory
from apps.chat.state_machine import get_next_stage


def run_autonomous_research(session, user_input):

    # 1️ Extract intent
    intent = extract_intent(user_input)

    disease = intent.get("disease")
    compound = intent.get("compound")

    # 2️ Gather evidence
    evidence = gather_evidence(disease, compound)

    # 3️ Retrieve memory
    past_memory = ResearchMemory.objects.filter(session=session)

    # 4️ Generate reasoning
    response = generate_scientific_response(
        session=session,
        user_input=user_input,
        evidence=evidence,
        memory=past_memory
    )

    # 5️ Update research stage
    session.research_stage = get_next_stage(session.research_stage)
    session.current_hypothesis = response["hypothesis"]
    session.save()

    return response
