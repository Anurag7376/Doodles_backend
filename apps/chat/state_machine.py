RESEARCH_STAGES = [
    "exploration",
    "hypothesis_generation",
    "optimization",
    "risk_refinement",
    "commercial_analysis"
]


def get_next_stage(current_stage: str) -> str:
    try:
        index = RESEARCH_STAGES.index(current_stage)
        if index + 1 < len(RESEARCH_STAGES):
            return RESEARCH_STAGES[index + 1]
        return current_stage
    except ValueError:
        return "exploration"
