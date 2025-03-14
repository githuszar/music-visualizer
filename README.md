# Music Visualizer

Este é um aplicativo Streamlit que gera insights baseados nas preferências musicais do usuário no Spotify.

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/music-visualizer.git
   cd music-visualizer
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

## Configuração de Segredos no Streamlit

1. No Streamlit Cloud, adicione as seguintes credenciais em **secrets.toml**:
   ```toml
   CLIENT_ID = "SEU_CLIENT_ID"
   CLIENT_SECRET = "SEU_CLIENT_SECRET"
   REDIRECT_URI = "https://musicvisualizer.streamlit.app/callback"
   ```

2. Faça o deploy da aplicação no Streamlit Cloud.

## Deploy no Streamlit Cloud

1. Crie um repositório no GitHub e envie os arquivos.
2. Acesse [Streamlit Cloud](https://share.streamlit.io) e conecte o repositório.
3. Configure `app.py` como arquivo principal e faça o deploy.
