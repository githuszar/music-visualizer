import os
import requests
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import numpy as np
from urllib.parse import urlparse, parse_qs
import time
import json

try:
    from perlin_noise import PerlinNoise
except ImportError:
    os.system("pip install perlin-noise")
    from perlin_noise import PerlinNoise

# Criando diretório para salvar os dados do usuário
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_user_data(user_id, data):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_user_data(user_id):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None

# Função de geração de imagem
def generate_perlin_image(seed, size=500):
    noise = PerlinNoise(octaves=3, seed=seed)
    img_array = np.array([[int((noise([x/size, y/size]) + 1) * 127.5) for x in range(size)] for y in range(size)])
    img = Image.fromarray(img_array.astype('uint8'), mode='L')
    os.makedirs("visualization", exist_ok=True)
    img_path = f"visualization/{seed}.png"
    img.save(img_path)
    return img_path

# Carregar credenciais do Spotify do arquivo secrets.toml
CLIENT_ID = st.secrets.get("CLIENT_ID", "")
CLIENT_SECRET = st.secrets.get("CLIENT_SECRET", "")
REDIRECT_URI = st.secrets.get("REDIRECT_URI", "")
SCOPE = "user-top-read"

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    st.error("Erro: Credenciais do Spotify não configuradas corretamente. Verifique o arquivo secrets.toml.")
    st.stop()

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

st.title("🎵 Music Visualizer")

query_params = st.query_params
if "code" in query_params and "access_token" not in st.session_state:
    auth_code = query_params["code"][0]
    token_info = sp_oauth.get_cached_token() if sp_oauth.get_cached_token() else sp_oauth.get_access_token(auth_code)
    if token_info:
        st.session_state["access_token"] = token_info["access_token"]
        st.session_state["token_info"] = token_info
        user_info = spotipy.Spotify(auth=token_info["access_token"]).me()
        st.session_state["user_id"] = user_info["id"]
        st.success("Autenticação realizada com sucesso! Você será redirecionado automaticamente.")
        st.query_params.clear()
        st.toast("Redirecionando...", icon="🔄")
        time.sleep(2)
        st.rerun()
    else:
        st.error("Erro ao obter o token de autenticação. Tente novamente.")
        st.stop()

if "access_token" not in st.session_state:
    auth_url = sp_oauth.get_authorize_url()
    st.markdown(f"[Clique aqui para conectar ao Spotify]({auth_url})")
    st.stop()

sp = spotipy.Spotify(auth=st.session_state["access_token"])

user_id = st.session_state.get("user_id", "unknown_user")
user_data = load_user_data(user_id) or {}

st.subheader("Seus artistas mais ouvidos")
try:
    top_artists = sp.current_user_top_artists(limit=10)
except spotipy.SpotifyException as e:
    st.error(f"Erro ao obter dados do Spotify: {e}")
    st.stop()
artist_names = [artist["name"] for artist in top_artists["items"]] if "items" in top_artists and top_artists["items"] else []
user_data["top_artists"] = artist_names
st.write(", ".join(artist_names) if artist_names else "Nenhum artista encontrado.")

st.subheader("Seus gêneros favoritos")
genres = set()
if "items" in top_artists and top_artists["items"]:
    for artist in top_artists["items"]:
    genres.update(artist.get("genres", []))
user_data["top_genres"] = list(genres)
st.write(", ".join(genres) if genres else "Nenhum gênero encontrado.")

music_index = len(artist_names) * 10
st.subheader("Seu índice musical único:")
st.write(music_index)
user_data["music_index"] = music_index

if music_index > 0:
    if music_index > 0:
    image_path = generate_perlin_image(music_index)
else:
    image_path = None
    user_data["image_path"] = image_path
    st.image(image_path, caption="Sua representação musical", use_container_width=True)
else:
    st.write("Nenhuma imagem gerada. Índice musical inválido.")

save_user_data(user_id, user_data)

st.markdown("[Compartilhe no Twitter](https://twitter.com/intent/tweet?text=Veja%20minha%20imagem%20musical!)")

if st.button("Sair"):
    del st.session_state["access_token"]
    st.query_params.clear()
    st.rerun()
