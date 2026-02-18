from .pubmed_agent import search_pubmed
from .tools.clinical_trials import search_clinical_trials

def gather_evidence(disease, compound):
    query = f"{compound} AND {disease}"
    pubmed = search_pubmed(query)
    trials = search_clinical_trials(query)

    return {
        "pubmed": pubmed,
        "clinical_trials": trials
    }
