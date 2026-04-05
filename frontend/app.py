import streamlit as st
import sys
import os
import time

# 1. Configuração e Estilo
st.set_page_config(page_title="GlobalClause AI", page_icon="⚖️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .titulo-tech {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white; border-radius: 10px; padding: 15px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com o Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from backend.main import gerar_pdf_protegido
except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.stop()

# --- INTERFACE ---
st.markdown('<p class="titulo-tech">GLOBALCLAUSE AI</p>', unsafe_allow_html=True)
st.write("🛰️ **Data Intelligence & Legal Engineering** | Genailma Couto")

with st.form("form_relatorio"):
    pergunta = st.text_area("🔍 O que deseja analisar?", placeholder="Descreva o caso...")
    senha = st.text_input("🔐 Senha do PDF", type="password")
    botao_gerar = st.form_submit_button("GERAR RELATÓRIO SEGURO")

if botao_gerar:
    if not pergunta or not senha:
        st.warning("Preencha os campos.")
    else:
        with st.spinner("🚀 Gerando inteligência de dados..."):
            try:
                import tempfile
                # Usa o diretório temporário oficial do sistema (Linux/Windows)
                caminho_seguro = os.path.join(tempfile.gettempdir(), "Analise_GlobalClause.pdf")
                
                # Chamada do Motor
                gerar_pdf_protegido(pergunta, senha, caminho_seguro)
                
                time.sleep(2) 
                
                if os.path.exists(caminho_seguro):
                    st.success("✅ Relatório pronto para download!")
                    with open(caminho_seguro, "rb") as f:
                        st.download_button(
                            label="📥 BAIXAR RELATÓRIO PDF",
                            data=f,
                            file_name="Analise_GlobalClause.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error("Erro: O arquivo não foi gerado no diretório esperado.")
            except Exception as error:
                st.error(f"Erro técnico: {error}")

st.caption("GlobalClause AI © 2026")