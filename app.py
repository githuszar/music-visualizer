import os
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gerador_imagens import generate_image  # Importando a função de geração de imagens

# Configuração inicial utilizando Streamlit Secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "https://musicvisualizer.streamlit.app/"
SCOPE = "user-library-read user-top-read user-read-private"

# Criando objeto de autenticação
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

# Título da aplicação
st.title("🎵 Music Visualizer")

# Função de logout
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Função principal
def main():
    # Verifica se o token de acesso está na sessão
    if "access_token" not in st.session_state:
        # Se não estiver, tenta obter o código de autenticação da URL
        auth_code = st.experimental_get_query_params().get("code")
        if auth_code:
            # Troca o código pelo token de acesso
            token_info = sp_oauth.get_access_token(auth_code[0])
            if token_info and "access_token" in token_info:
                st.session_state["access_token"] = token_info['access_token']
                # Limpa os parâmetros da URL
                st.experimental_set_query_params()
                st.experimental_rerun()
        else:
            # Se não houver código, exibe o link de autenticação
            auth_url = sp_oauth.get_authorize_url()
            st.markdown(f'<a href="{auth_url}" target="_self">🔑 Conectar ao Spotify</a>', unsafe_allow_html=True)
    else:
        # Se o token estiver na sessão, inicializa o cliente Spotipy
        access_token = st.session_state["access_token"]
        sp = spotipy.Spotify(auth=access_token)
        
        # Tenta obter os dados do usuário
        try:
            user_profile = sp.current_user()
            st.success(f"✅ Autenticado como {user_profile['display_name']}!")
            
            # Exibe botão de logout
            if st.button("🔴 Logout"):
                logout()
            
            # Exibe Top Artistas
            top_artists = sp.current_user_top_artists(limit=5)
            st.subheader("Seus Top 5 Artistas no Spotify:")
            for artist in top_artists['items']:
                st.write(f"🎤 {artist['name']}")
            
            # Exibe Top Músicas
            top_tracks = sp.current_user_top_tracks(limit=5)
            st.subheader("Suas Top 5 Músicas no Spotify:")
            for track in top_tracks['items']:
                st.write(f"🎵 {track['name']} - {track['artists'][0]['name']}")
            
            # Gera e exibe imagem baseada na música
            img_path = generate_image()
            st.image(img_path, caption="Sua imagem musical única", use_column_width=True)
        
        except spotipy.exceptions.SpotifyException as e:
            st.error("Ocorreu um erro ao acessar os dados do Spotify. Por favor, faça login novamente.")
            logout()

if __name__ == "__main__":
    main()
