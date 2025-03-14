import os
import requests
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

# Verifica se a biblioteca Spotipy está instalada, instala se necessário
try:
    from spotipy.oauth2 import SpotifyOAuth
    import spotipy
except ModuleNotFoundError:
    st.error("Spotipy library is not installed. Please install it using 'pip install spotipy' and restart the application.")

# Configuração inicial utilizando Streamlit Secrets
try:
    CLIENT_ID = st.secrets["CLIENT_ID"]
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
except KeyError as e:
    st.error(f"Missing secret: {e}")
    st.stop()

# Criando objeto de autenticação
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read user-read-email",
    show_dialog=True  # Garante que a autenticação exiba o popup corretamente
)

# Criar interface no Streamlit
st.title("🎵 Music Visualizer")

# Captura o código de autenticação diretamente na mesma página
query_params = st.experimental_get_query_params()
auth_code = query_params.get("code")

@st.cache
def generate_image(music_score):
    width, height = 500, 500
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    np.random.seed(music_score)
    energy, valence, danceability = np.random.randint(0, 256, 3)
    for x in range(width):
        for y in range(height):
            draw.point((x, y), (energy, valence, danceability))
    from io import BytesIO
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# Função de logout
def logout():
    st.session_state.pop("access_token", None)
    st.experimental_set_query_params()  # Limpar parâmetros da URL

if "access_token" not in st.session_state:
    if auth_code:
        token_info = sp_oauth.get_access_token(auth_code)
        if token_info:
            st.session_state["access_token"] = token_info['access_token']
            st.experimental_set_query_params()  # Limpar parâmetros da URL
            st.experimental_rerun()  # Redirecionar corretamente para a página principal
        else:
            st.error("Failed to retrieve token information.")
    else:
        auth_url = sp_oauth.get_authorize_url()
        if st.button("🔑 Conectar ao Spotify"):
            st.write(f'<a href="{auth_url}" target="_blank">Conectar ao Spotify</a>', unsafe_allow_html=True)
else:
    st.success("✅ Autenticado com sucesso!")
    access_token = st.session_state["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    user_profile = sp.current_user()
    st.write(f"Bem-vindo, {user_profile['display_name']}!")

    # Exibir botão de logout
    if st.button("🔴 Logout"):
        logout()

    # Exibir Top Artistas
    top_artists = sp.current_user_top_artists(limit=5)
    st.subheader("Seus Top 5 Artistas no Spotify:")
    for artist in top_artists['items']:
        st.write(f"🎤 {artist['name']}")

    # Exibir Top Músicas
    top_tracks = sp.current_user_top_tracks(limit=5)
    st.subheader("Suas Top 5 Músicas no Spotify:")
    for track in top_tracks['items']:
        st.write(f"🎵 {track['name']} - {track['artists'][0]['name']}")

    # Gerar e exibir imagem baseada na música
    music_score = sum(ord(char) for char in user_profile['id']) % 1000
    img_bytes = generate_image(music_score)
    st.image(img_bytes, caption="Sua imagem musical única", use_column_width=True)
