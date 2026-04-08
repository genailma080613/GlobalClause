import streamlit as st
import os
import sys
import tempfile
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
        font-size: 3rem; font-weight: 800; text-align: center;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white; border-radius: 10px; padding: 15px; font-weight: bold; border: none;
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

# --- CABEÇALHO ---
st.markdown('<p class="titulo-tech">GLOBALCLAUSE AI</p>', unsafe_allow_html=True)
st.write("🛰️ **Data Intelligence & Legal Engineering** | Genailma Couto")

# --- NAVEGAÇÃO POR ABAS (As abas que você queria!) ---
aba1, aba2, aba3 = st.tabs(["⚖️ Jurídico Global", "🇲🇪 Módulo Montenegro", "📊 Business Intelligence"])

# Função para evitar repetição de código
def executar_geracao(pergunta_final, senha_final, nome_pdf):
    with st.spinner("🚀 Gerando inteligência de dados..."):
        try:
            import tempfile
            caminho_seguro = os.path.join(tempfile.gettempdir(), f"{nome_pdf}.pdf")
            
            gerar_pdf_protegido(pergunta_final, senha_final, caminho_seguro)
            
            time.sleep(2) 
            
            if os.path.exists(caminho_seguro):
                st.success("✅ Relatório pronto para download!")
                with open(caminho_seguro, "rb") as f:
                    st.download_button(
                        label=f"📥 BAIXAR {nome_pdf.upper()}",
                        data=f,
                        file_name=f"{nome_pdf}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("Erro: O arquivo não foi localizado.")
        except Exception as error:
            st.error(f"Erro técnico: {error}")

# --- CONTEÚDO DA ABA 1: JURÍDICO ---
with aba1:
    with st.form("form_juridico"):
        p1 = st.text_area("🔍 Análise Jurídica Geral", placeholder="Ex: Riscos de contratos internacionais...")
        idioma1 = st.selectbox("Idioma", ["Português", "English", "Español"], key="lang1")
        s1 = st.text_input("🔐 Senha do PDF", type="password", key="s1")
        if st.form_submit_button("GERAR RELATÓRIO JURÍDICO"):
            if p1 and s1:
                executar_geracao(f"Traduza para {idioma1} e analise: {p1}", s1, "Analise_Juridica")
            else:
                st.warning("Preencha todos os campos.")

# --- CONTEÚDO DA ABA 2: MONTENEGRO ---
with aba2:
    st.info("🇲🇪 Foco em Cidadania e Digital Nomad Visa")
    with st.form("form_mn"):
        p2 = st.selectbox("O que deseja saber sobre Montenegro?", 
                          ["Visto de Nômade Digital", "Cidadania por Investimento", "Abertura de Empresa (DOO)", "Compra de Imóveis"])
        extra = st.text_input("Detalhes adicionais (opcional)")
        s2 = st.text_input("🔐 Senha do PDF", type="password", key="s2")
        if st.form_submit_button("GERAR RELATÓRIO MONTENEGRO"):
            if s2:
                executar_geracao(f"Gere um relatório técnico sobre {p2} em Montenegro. Adicional: {extra}", s2, "Relatorio_Montenegro")
            else:
                st.warning("Defina uma senha.")

# --- CONTEÚDO DA ABA 3: BUSINESS ---
with aba3:
    with st.form("form_bi"):
        p3 = st.text_area("📊 Business Intelligence", placeholder="Ex: Viabilidade de prospecção imobiliária no Brooklin...")
        s3 = st.text_input("🔐 Senha do PDF", type="password", key="s3")
        if st.form_submit_button("GERAR ANÁLISE DE MERCADO"):
            if p3 and s3:
                executar_geracao(f"Aja como especialista em Business Intelligence e analise: {p3}", s3, "Analise_BI")
            else:
                st.warning("Preencha todos os campos.")

st.caption("GlobalClause AI © 2026")