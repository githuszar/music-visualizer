import os
import requests
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gerador_imagens import generate_image  # Importando a ferramenta de geração de imagens

# Configuração inicial utilizando Streamlit Secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "https://musicvisualizer.streamlit.app/"
SCOPE = "user-library-read user-top-read"

# Criando objeto de autenticação
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

# Criar interface no Streamlit
st.title("🎵 Music Visualizer")

# Captura o código de autenticação diretamente na mesma página
query_params = st.query_params
auth_code = query_params.get("code")

# Função de logout
def logout():
    st.session_state.pop("access_token", None)
    st.query_params = {}
    st.rerun()

if "access_token" not in st.session_state:
    if auth_code:
        token_info = sp_oauth.get_access_token(auth_code, as_dict=False)
        if token_info and "access_token" in token_info:
            st.session_state["access_token"] = token_info['access_token']
            st.query_params.clear()
            st.rerun()
    else:
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f'<a href="{auth_url}" target="_blank">🔑 Conectar ao Spotify</a>', unsafe_allow_html=True)
else:
    st.success("✅ Autenticado com sucesso!")
    access_token = st.session_state["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    user_profile = sp.current_user()
    st.write(f"Bem-vindo, {user_profile['display_name']}!")

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
    img_path = generate_image()
    st.image(img_path, caption="Sua imagem musical única", use_column_width=True)
