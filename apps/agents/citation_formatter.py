def format_citations(pubmed_articles):
    citations = []

    for article in pubmed_articles:
        if "error" in article:
            continue

        citations.append(
            f"{article['title']} ({article['year']}) - {article['journal']} | PMID:{article['pmid']}"
        )

    return citations
