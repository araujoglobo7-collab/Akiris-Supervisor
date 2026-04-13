import streamlit as st
import subprocess
import os

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Bruxo ZIP Master", layout="wide")
st.markdown("<style>.stButton>button { background-color: #ff8c00; color: white; }</style>", unsafe_allow_html=True)

st.title("🧙‍♂️ Automação de Compactação: RNEST")

# CAMINHOS FIXOS
SETE_ZIP = r"C:\Program Files\7-Zip\7z.exe"
CAMINHO_ORIGEM = r"R:\GRUPOS-UDA\Qualidade\01.Controle da Qualidade\20 -UDA - SGP\Automatização\BOOK"
CAMINHO_DESTINO = r"R:\GRUPOS-UDA\Qualidade\01.Controle da Qualidade\20 -UDA - SGP\Automatização\ZIPS_PRONTOS"

# Cria a pasta de destino automaticamente se ela não existir
if not os.path.exists(CAMINHO_DESTINO):
    os.makedirs(CAMINHO_DESTINO)

st.info(f"📁 **Origem:** {CAMINHO_ORIGEM}\n\n🎯 **Destino dos Zips:** {CAMINHO_DESTINO}")

if os.path.exists(CAMINHO_ORIGEM):
    subpastas = [f for f in os.listdir(CAMINHO_ORIGEM) if os.path.isdir(os.path.join(CAMINHO_ORIGEM, f))]
    st.write(f"Encontradas **{len(subpastas)}** pastas prontas.")
else:
    st.error("Caminho de Origem não encontrado! Verifique a conexão com o drive R:")
    subpastas = []

if st.button("🚀 ZIPAR E MOVER EM LOTE"):
    if not os.path.exists(SETE_ZIP):
        st.error(f"7-Zip não encontrado em: {SETE_ZIP}")
    elif not subpastas:
        st.warning("Nada para processar.")
    else:
        barra = st.progress(0)
        status = st.empty()
        
        for i, pasta in enumerate(subpastas):
            c_origem = os.path.join(CAMINHO_ORIGEM, pasta)
            arquivo_saida = os.path.join(CAMINHO_DESTINO, f"{pasta}.zip")
            
            status.text(f"Processando: {pasta} ({i+1}/{len(subpastas)})")
            
            # Comando com aspas duplas para evitar erro em caminhos com espaços
            comando = f'"{SETE_ZIP}" a -tzip "{arquivo_saida}" "{c_origem}"'
            subprocess.run(comando, shell=True)
            
            barra.progress((i + 1) / len(subpastas))
        st.success("✅ Processo concluído com sucesso!")