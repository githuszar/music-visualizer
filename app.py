import os
import requests
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

# Configuração inicial
CLIENT_ID = "e983ab76967541819658cb3126d9f3df"
CLIENT_SECRET = "4f4d1a7a3697434db2a0edc2c484f80c"
REDIRECT_URI = "https://musicvisualizer.streamlit.app/callback"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"
SCOPE = "user-top-read"

# Função para gerar a URL de autenticação
def get_auth_url():
    return (f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code"
            f"&redirect_uri={REDIRECT_URI}&scope={SCOPE}")

# Função para obter o token de acesso do Spotify
def get_spotify_access_token(auth_code):
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    return response.json().get("access_token")

# Função para buscar os principais artistas do usuário
def get_top_artists(access_token):
    url = f"{API_BASE_URL}/me/top/artists?limit=5"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("items", [])

# Função para buscar os principais gêneros musicais do usuário
def get_top_tracks_features(access_token):
    url = f"{API_BASE_URL}/me/top/tracks?limit=5"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    tracks = response.json().get("items", [])
    
    if tracks:
        track_ids = ",".join([track["id"] for track in tracks])
        url_features = f"{API_BASE_URL}/audio-features?ids={track_ids}"
        response_features = requests.get(url_features, headers=headers)
        features = response_features.json().get("audio_features", [])
        return features
    return []

# Criar diretório para armazenar imagens
visualization_dir = "visualization"
os.makedirs(visualization_dir, exist_ok=True)

# Função para gerar imagem baseada nas características musicais
def generate_simple_image(user_id, features):
    width, height = 500, 500
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    
    if features:
        energy = features[0]["energy"] * 255
        valence = features[0]["valence"] * 255
        danceability = features[0]["danceability"] * 255
    else:
        energy, valence, danceability = 128, 128, 128  # Valores padrão

    for x in range(width):
        for y in range(height):
            draw.point((x, y), (int(energy), int(valence), int(danceability)))

    img_path = f"{visualization_dir}/{user_id}.png"
    img.save(img_path)
    return img_path

# Criar interface no Streamlit
st.title("🎨 Music Visualizer")

auth_url = get_auth_url()
st.markdown(f"[🔑 Clique aqui para autenticar no Spotify]({auth_url})")

auth_code = st.text_input("📥 Cole aqui o código de autenticação do Spotify")
if st.button("🎵 Gerar Visualização Musical"):
    if auth_code:
        access_token = get_spotify_access_token(auth_code)
        top_artists = get_top_artists(access_token)
        track_features = get_top_tracks_features(access_token)
        
        user_id = "spotify_user"
        img_path = generate_simple_image(user_id, track_features)
        
        st.image(img_path, caption="Imagem baseada no perfil musical do Spotify", use_container_width=True)
        st.success("✅ Visualização gerada com sucesso!")
    else:
        st.warning("⚠️ Por favor, forneça o código de autenticação do Spotify.")
