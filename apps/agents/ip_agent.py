def evaluate_ip_risk(patent_data):
    if patent_data["novelty_risk"] == "High":
        return "High infringement risk"
    return "Potentially patentable with structural modification"
