

from Bio import Entrez
from tqdm import tqdm
import json
import os
from dotenv import load_dotenv

load_dotenv()


Entrez.email = os.getenv("Email")  

def search_pubmed(query: str, max_results: int = 50):
    """
    Cherche des articles dans PubMed à partir d'une requête.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_details(pubmed_ids):
    """
    Récupère les détails (titre, résumé) des articles à partir des IDs PubMed.
    """
    ids_str = ",".join(pubmed_ids)
    handle = Entrez.efetch(db="pubmed", id=ids_str, rettype="abstract", retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records["PubmedArticle"]

def save_articles(records, output_file="data/pubmed_articles.json"):
    """
    Enregistre les abstracts dans un fichier JSON.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    data = []

    for article in tqdm(records, desc="Sauvegarde des articles"):
        try:
            title = article["MedlineCitation"]["Article"]["ArticleTitle"]
            abstract = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
            pmid = article["MedlineCitation"]["PMID"]
            data.append({
                "pmid": str(pmid),
                "title": title,
                "abstract": abstract
            })
        except Exception:
            continue  

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(data)} articles enregistrés dans {output_file}")

def download_pubmed(query="cardiology", max_results=50):
    """
    Pipeline complet : recherche, téléchargement et sauvegarde.
    """
    print(f"🔍 Recherche d'articles PubMed pour : {query}")
    ids = search_pubmed(query, max_results=max_results)
    print(f"✅ {len(ids)} articles trouvés.")
    records = fetch_details(ids)
    save_articles(records)

# Test rapide
if __name__ == "__main__":
    download_pubmed(query="paralysie faciale", max_results=30)
