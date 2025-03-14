import os
import requests
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import numpy as np
from perlin_noise import PerlinNoise

<<<<<<< HEAD
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
    img.save(img_path)
    return img_path

# Configuração da API do Spotify
CLIENT_ID = "e983ab76967541819658cb3126d9f3df"
CLIENT_SECRET = "4f4d1a7a3697434db2a0edc2c484f80c"
REDIRECT_URI = "https://musicvisualizer.streamlit.app"
SCOPE = "user-top-read"

=======
# Função de geração de imagem
def generate_perlin_image(seed, size=500):
    noise = PerlinNoise(octaves=3, seed=seed)
    img_array = np.array([[int((noise([x/size, y/size]) + 1) * 127.5) for x in range(size)] for y in range(size)])
    img = Image.fromarray(img_array.astype('uint8'), mode='L')
    img_path = f"visualization/{seed}.png"
    os.makedirs("visualization", exist_ok=True)
    img.save(img_path)
    return img_path

# Configuração da API do Spotify
CLIENT_ID = "e983ab76967541819658cb3126d9f3df"
CLIENT_SECRET = "4f4d1a7a3697434db2a0edc2c484f80c"
REDIRECT_URI = "https://musicvisualizer.streamlit.app"
SCOPE = "user-top-read"

>>>>>>> 51b279a (Atualização do Music Visualizer com correções e melhorias)
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
    image_path = generate_perlin_image(music_index)
    st.image(image_path, caption="Sua representação musical", use_column_width=True)
    
    # Botão para compartilhar a imagem
    st.markdown("[Compartilhe no Twitter](https://twitter.com/intent/tweet?text=Veja%20minha%20imagem%20musical!)")
    
    # Logout
    if st.button("Sair"):
        del st.session_state["access_token"]
        st.experimental_rerun()
