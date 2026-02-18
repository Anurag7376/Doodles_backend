def assess_risk(evidence):
    risk_flags = []

    for paper in evidence["pubmed"]:
        if "toxicity" in paper["abstract"].lower():
            risk_flags.append("Neurotoxicity mentioned in literature")

    return risk_flags
