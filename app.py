import os
import requests
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import numpy as np
from urllib.parse import urlparse, parse_qs

try:
    from perlin_noise import PerlinNoise
except ImportError:
    os.system("pip install perlin-noise")
    from perlin_noise import PerlinNoise

# Função de geração de imagem
def generate_perlin_image(seed, size=500):
    noise = PerlinNoise(octaves=3, seed=seed)
    img_array = np.array([[int((noise([x/size, y/size]) + 1) * 127.5) for x in range(size)] for y in range(size)])
    img = Image.fromarray(img_array.astype('uint8'), mode='L')
    img_path = f"visualization/{seed}.png"
    os.makedirs("visualization", exist_ok=True)
    img.save(img_path)
    return img_path

# Carregar credenciais do Spotify do arquivo secrets.toml
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]
SCOPE = "user-top-read"

# Objeto de autenticação
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

# Título da aplicação
st.title("🎵 Music Visualizer")

# Verifica autenticação
query_params = st.experimental_get_query_params()
if "code" in query_params:
    auth_code = query_params["code"][0]  # Extrai o código de autenticação
    token_info = sp_oauth.get_access_token(auth_code, as_dict=True)
    st.session_state["access_token"] = token_info["access_token"]
    st.success("Autenticação realizada com sucesso! Retornando à página principal...")
    st.experimental_set_query_params()  # Remove os parâmetros da URL
    st.stop()  # Para evitar múltiplas execuções
    st.rerun()

if "access_token" not in st.session_state:
    auth_url = sp_oauth.get_authorize_url()
    st.markdown(f"[Clique aqui para conectar ao Spotify]({auth_url})")
    st.stop()

# Criando objeto Spotipy autenticado
sp = spotipy.Spotify(auth=st.session_state["access_token"])

# Recuperando os top artistas
st.subheader("Seus artistas mais ouvidos")
top_artists = sp.current_user_top_artists(limit=10)
artist_names = [artist["name"] for artist in top_artists["items"]]
st.write(", ".join(artist_names))

# Recuperando os gêneros musicais
genres = set()
for artist in top_artists["items"]:
    genres.update(artist["genres"])
st.subheader("Seus gêneros favoritos")
st.write(", ".join(genres))

# Geração do índice musical
music_index = len(artist_names) * 10  # Exemplo de cálculo simples
st.subheader("Seu índice musical único:")
st.write(music_index)

# Gerar imagem baseada no índice
image_path = generate_perlin_image(music_index)
st.image(image_path, caption="Sua representação musical", use_column_width=True)

# Botão para compartilhar a imagem
st.markdown("[Compartilhe no Twitter](https://twitter.com/intent/tweet?text=Veja%20minha%20imagem%20musical!)")

# Logout
if st.button("Sair"):
    del st.session_state["access_token"]
    st.experimental_set_query_params()  # Remove query params para evitar erro
    st.rerun()
