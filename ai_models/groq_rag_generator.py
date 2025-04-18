

import os
from dotenv import load_dotenv
from text_generator import GroqTextGenerator
from rag_retriever import RAGRetriever
from pumbed_downloader import download_pubmed

load_dotenv()

class GroqRAGPipeline:
    def __init__(self):
        self.generator = GroqTextGenerator()
        self.retriever = RAGRetriever()

    def generate_answer(self, question: str, top_k: int = 3, max_tokens: int = 300, max_docs: int = 30) -> str:
        
        print(f"\n🔎 Recherche d'articles récents sur : {question}")
        download_pubmed(query=question, max_results=max_docs)

        self.retriever.index_articles(max_docs=max_docs)

        
        documents = self.retriever.query(question, top_k=top_k)
        context = "\n\n".join([doc[:500] for doc, _ in documents])

       
        prompt = f"""
Voici des extraits d'articles scientifiques extraits de PubMed :
---
{context}
---
En te basant uniquement sur ces extraits, réponds de manière claire et précise à la question suivante :
{question}
"""

       
        return self.generator.generate(prompt, max_tokens=max_tokens)

# Test rapide
if __name__ == "__main__":
    pipeline = GroqRAGPipeline()
    question = "what is Crohn disease treatment ?"
    answer = pipeline.generate_answer(question)
    print("\n🧠 Réponse générée par Groq :\n")
    print(answer)


#La classe GroqRAGPipeline implémente un pipeline de type RAG (Retrieval-Augmented Generation), qui combine la recherche d'informations pertinentes et la génération de texte.
#  Lorsqu'une question est posée, le système commence par télécharger des articles scientifiques liés à cette question depuis PubMed grâce à la fonction download_pubmed. Ces documents 
# sont ensuite indexés sous forme vectorielle par le composant RAGRetriever, afin de permettre une recherche de similarité sémantique. Les documents les plus pertinents par rapport à la 
# question sont extraits, puis leurs extraits sont concaténés pour créer un contexte textuel. Ce contexte est utilisé pour construire un prompt clair qui est transmis au générateur de 
# texte (GroqTextGenerator). Le modèle est explicitement invité à répondre uniquement à partir de ces extraits, ce qui garantit une réponse basée sur des sources fiables, récentes, 
# et sans hallucination. Le résultat final est donc une réponse précise, guidée par les données scientifiques extraites, et non par la mémoire interne du modèle