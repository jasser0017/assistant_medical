import requests
import json

# Ton access_token complet, bien copié depuis le localStorage (sans guillemets, sans espaces supplémentaires)
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlM0UTNhblpKUlNpOEk4WHAtZUE2aiJ9.eyJub21pY2VtYWlsIjoiamFzc2VyYWxsZWxhMDA3QGdtYWlsLmNvbSIsImlzcyI6Imh0dHBzOi8vbm9taWNhaS1wcm9kdWN0aW9uLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2ZlYTZhZDgzODE3NzE5MzFkODkwMGYiLCJhdWQiOlsiaHR0cHM6Ly9hcGktYXRsYXMubm9taWMuYWkiLCJodHRwczovL25vbWljYWktcHJvZHVjdGlvbi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzQ0NzQyMTA2LCJleHAiOjE3NDczMzQxMDYsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJWRjQxRHFkRXlTMkFhcTY0cTFJb08xRU96ZHBqcGxudiJ9.Rug2xeKR3HHIYjlrf_l9T3JhDe61hmHydoFwQveAuG0biJIZ62UMmTLgeBgEly2YKvv8QL_7f-zGfBHYXuP_6JRsuTaLaLQo_TurgMuXLMynod4BZWx31CILf5ulxvXN0zynpzyiqetnCpLqoUiBoIzZOmV5R--je0-E1LtAOPBAndi13chpbCKaWNvrgm5ZA1sxSV2Xr935hgUDaFr76LYD-cqFHgZgroJutTTIOiuDkCiNxkx76SQk47eFANmgfJyw0Wl3wDGWbfpAl3LfFCpS1vyi1taLYsammozlAUyMLZNOc3sJEHfwFYghWdt6aQzuZZXwuXFeGuI2FzYeLg"

# Vérification rapide que le token est bien formé
if len(token.split(".")) != 3:
    print("❌ Token mal formé. Assure-toi de copier TOUT le token depuis le localStorage sans rien manquer.")
    exit()
else:
    print("✅ Token bien formé !")

# URL de création de la clé API (USER scope)
url = "https://api-atlas.nomic.ai/v1/user/authorization/keys/VF41DqdEyS2Aaq64q1IoO1EOzdpjplnv/create"

# En-têtes HTTP
headers = {
    "Authorization": f"Bearer {token.strip()}",
    "Content-Type": "application/json"
}

# Corps de la requête
payload = {
    "key_name": "JasserAPIKey",  # Donne un nom à ta clé
    "key_role": "OWNER",  # Rôle de la clé
    "key_scope": "USER",  # Portée : pour ton propre utilisateur
    "key_target_id": "auth0|67fea6ad8381771931d8900f"  # Ton ID utilisateur (sub dans le JWT)
}

# Envoi de la requête
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Résultat
print("Status code :", response.status_code)
print("Réponse API :", response.json())
