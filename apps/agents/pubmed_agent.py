from Bio import Entrez
from django.conf import settings
import time

Entrez.email = getattr(settings, "PUBMED_EMAIL", "research@doodle.ai")


def search_pubmed(query, max_results=5):
    try:
        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=max_results,
            sort="relevance"
        )
        record = Entrez.read(handle)
        ids = record.get("IdList", [])

        if not ids:
            return []

        fetch_handle = Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="abstract",
            retmode="xml"
        )
        fetch_records = Entrez.read(fetch_handle)

        articles = []

        for article in fetch_records["PubmedArticle"]:
            article_data = article["MedlineCitation"]["Article"]

            title = article_data.get("ArticleTitle", "")
            abstract = ""

            if "Abstract" in article_data:
                abstract_parts = article_data["Abstract"]["AbstractText"]
                abstract = " ".join(str(part) for part in abstract_parts)

            pmid = article["MedlineCitation"]["PMID"]

            articles.append({
                "title": str(title),
                "abstract": abstract,
                "pmid": str(pmid),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })

            time.sleep(0.3)

        return articles

    except Exception as e:
        return [{
            "error": f"PubMed fetch failed: {str(e)}"
        }]
