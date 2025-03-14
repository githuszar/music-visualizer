import os
import requests
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gerador_imagens import generate_perlin_image  # Função de geração de imagem

# Configuração da API do Spotify
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "https://your-music-image.lovable.app/callback"
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
if "access_token" not in st.session_state:
    auth_url = sp_oauth.get_authorize_url()
    st.markdown(f"[Clique aqui para conectar ao Spotify]({auth_url})")
else:
    token_info = st.session_state["access_token"]
    sp = spotipy.Spotify(auth=token_info)
    
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
    image_path = f"visualization/{music_index}.png"
    generate_perlin_image(music_index)
    st.image(image_path, caption="Sua representação musical", use_column_width=True)
    
    # Botão para compartilhar a imagem
    st.markdown("[Compartilhe no Twitter](https://twitter.com/intent/tweet?text=Veja%20minha%20imagem%20musical!)")
    
    # Logout
    if st.button("Sair"):
        del st.session_state["access_token"]
        st.experimental_rerun()
