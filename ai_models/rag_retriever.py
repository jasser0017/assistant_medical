# ai_models/rag_retriever.py

import json
import os
import numpy as np
from dotenv import load_dotenv
import faiss
from nomic_embedder import NomicEmbedder

load_dotenv()
DATA_PATH = "data/pubmed_articles.json"

class RAGRetriever:
    def __init__(self):
        self.embedder = NomicEmbedder()
        self.texts = []
        self.metadatas = []
        self.index = None

    def index_articles(self, max_docs: int = None):
        """
        Charge les articles depuis JSON, génère les embeddings, crée un index FAISS.
        """
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            articles = json.load(f)

        if max_docs:
            articles = articles[:max_docs]

        texts, metadatas = [], []

        for article in articles:
            text = article["title"] + "\n\n" + article["abstract"]
            texts.append(text)
            metadatas.append({
                "pmid": article["pmid"],
                "title": article["title"]
            })

        print(f"\n📡 Génération des embeddings via Nomic pour {len(texts)} documents...")
        embeddings = self.embedder.embed(texts)
        embeddings_np = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings_np.shape[1])
        self.index.add(embeddings_np)

        self.texts = texts
        self.metadatas = metadatas

        print("✅ Indexation terminée avec FAISS.")

    def query(self, question: str, top_k: int = 3):
        """
        Recherche les textes les plus proches de la question.
        """
        query_embedding = self.embedder.embed([question])[0]
        query_vec = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            doc = self.texts[idx]
            meta = self.metadatas[idx]
            results.append((doc, meta))
        return results


# ✅ Test
if __name__ == "__main__":
    rag = RAGRetriever()
    rag.index_articles(max_docs=50)

    question = "Quels est  ?"
    results = rag.query(question)

    for i, (doc, meta) in enumerate(results, 1):
        print(f"\n🔎 Résultat {i} — PMID: {meta['pmid']}")
        print(f"Titre : {meta['title']}")
        print(doc[:300], "...")
