from apps.chat.models import ChatSession, ResearchMemory
from apps.chat.state_machine import get_next_stage
from .intent_extractor import extract_intent
from .evidence_engine import gather_evidence
from .interactive_scientist import generate_scientific_response
import json


def get_or_fetch_evidence(session, disease, compound):
    existing = ResearchMemory.objects.filter(
        session=session,
        key="evidence"
    ).first()

    if existing:
        return existing.value

    evidence = gather_evidence(disease, compound)

    ResearchMemory.objects.create(
        session=session,
        key="evidence",
        value=evidence
    )

    return evidence


def run_interactive_research(session: ChatSession, user_input: str):

    # 1️⃣ Extract structured intent
    intent_raw = extract_intent(user_input)

    try:
        intent = json.loads(intent_raw)
        disease = intent.get("target_disease")
        compound = intent.get("base_compound")
    except Exception:
        disease = None
        compound = None

    # 2️⃣ Fallback to session memory if not provided
    if not disease:
        disease = session.research_topic

    if not compound:
        memory = ResearchMemory.objects.filter(
            session=session,
            key="base_compound"
        ).first()
        compound = memory.value if memory else None

    # 3️⃣ Store topic if first time
    if not session.research_topic and disease:
        session.research_topic = disease

    # 4️⃣ Fetch or reuse evidence
    evidence = get_or_fetch_evidence(session, disease, compound)

    # 5️⃣ Generate interactive scientific response
    response = generate_scientific_response(
        session,
        user_input,
        evidence
    )

    # 6️⃣ Update session state (single save)
    session.research_stage = get_next_stage(session.research_stage)
    session.current_hypothesis = response
    session.save()

    return response
