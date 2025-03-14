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
    os.system('pip install spotipy')
    from spotipy.oauth2 import SpotifyOAuth
    import spotipy

# Configuração inicial utilizando Streamlit Secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "https://musicvisualizer.streamlit.app/callback"
