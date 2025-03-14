import os
import requests
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

# Configuração inicial
CLIENT_ID = "e983ab76967541819658cb3126d9f3df"
CLIENT_SECRET = "4f4d1a7a3697434db2a0edc2c484f80c"
REDIRECT_URI = "https://musicvisualizer.streamlit.app"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"
SCOPE = "user-top-read"

# Criar diretório para armazenar imagens
visualization_dir = "visualization"
os.makedirs(visualization_dir, exist_ok=True)

# Função para gerar a URL de autenticação do Spotify
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

# Captura o código de autenticação diretamente da URL
query_params = st.query_params
auth_code = query_params.get("code")

if "access_token" not in st.session_state:
    if auth_code:
        access_token = get_spotify_access_token(auth_code)
        st.session_state["access_token"] = access_token
        st.rerun()
    else:
        st.markdown(f"[🔑 Conectar ao Spotify]({auth_url})", unsafe_allow_html=True)
else:
    st.success("✅ Autenticado com sucesso!")
    access_token = st.session_state["access_token"]
    track_features = get_top_tracks_features(access_token)
    
    user_id = "spotify_user"
    img_path = generate_simple_image(user_id, track_features)
    
    st.image(img_path, caption="Sua imagem musical única", use_container_width=True)
