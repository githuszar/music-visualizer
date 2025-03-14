import os
import requests
import pandas as pd
import streamlit as st

# Verifica se a biblioteca Spotipy está instalada, instala se necessário
try:
    from spotipy.oauth2 import SpotifyOAuth
    import spotipy
except ModuleNotFoundError:
    os.system('pip install spotipy')
    from spotipy.oauth2 import SpotifyOAuth
    import spotipy

# Configuração inicial utilizando Streamlit Secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "https://musicvisualizer.streamlit.app/callback"
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

if "access_token" not in st.session_state:
    if auth_code:
        token_info = sp_oauth.get_access_token(auth_code)
        st.session_state["access_token"] = token_info['access_token']
        st.rerun()
    else:
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[🔑 Conectar ao Spotify]({auth_url})", unsafe_allow_html=True)
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
