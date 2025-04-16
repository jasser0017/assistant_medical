# ai_models/nomic_embedder.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")

class NomicEmbedder:
    def __init__(self):
        if not NOMIC_API_KEY:
            raise ValueError("❌ Clé API Nomic manquante dans le .env")

        self.api_key = NOMIC_API_KEY
        self.endpoint = "https://api-atlas.nomic.ai/v1/embedding/text"

    def embed(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
    "model": "nomic-embed-text-v1",
    "texts": texts
}


        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Erreur API Nomic: {response.status_code} - {response.text}")

        return response.json()["embeddings"]
