import streamlit as st
import sys
import os

# 1. Configuração da página (Deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="GlobalClause AI", page_icon="⚖️")

# 2. A PONTE: Faz o Python enxergar a pasta 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Importa as funções do seu motor jurídico
    from backend.main import gerar_pdf_protegido
    backend_conectado = True
except Exception as e:
    st.error(f"Erro ao conectar com o backend: {e}")
    backend_conectado = False
    st.stop()

# --- INTERFACE VISUAL ---
st.title("⚖️ GlobalClause AI")
st.subheader("Gerador de Relatórios Jurídicos Seguros")
st.write("Desenvolvido por: **Genailma Couto**")

# Seletor de Idioma
idioma = st.selectbox(
    "Selecione o Idioma / Select Language", 
    ["Português", "English", "Montenegrin"]
)

# Formulário de entrada de dados
with st.form("form_relatorio"):
    pergunta = st.text_area(
        "O que você deseja analisar?", 
        placeholder="Ex: Requisitos para cidadania em Montenegro ou Contratos de Real Estate em SP..."
    )
    
    senha = st.text_input(
        "Defina uma senha para proteger o seu PDF:", 
        type="password",
        help="Esta senha será necessária para abrir o arquivo PDF gerado."
    )
    
    botao_gerar = st.form_submit_button("Gerar Relatório Seguro")

# Lógica de processamento
if botao_gerar:
    if not pergunta or not senha:
        st.warning("Por favor, preencha a pergunta e a senha antes de continuar.")
    else:
        with st.spinner("A IA está analisando sua solicitação e gerando o documento seguro..."):
            try:
                nome_arquivo = "Analise_GlobalClause.pdf"
                
                # Chama a função do backend para gerar o PDF
                gerar_pdf_protegido(pergunta, senha, nome_arquivo)
                
                # Exibe o sucesso e o botão de download
                st.success("✅ Relatório gerado com sucesso!")
                
                with open(nome_arquivo, "rb") as f:
                    st.download_button(
                        label="📥 Baixar Relatório (PDF)",
                        data=f,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )
            except Exception as error:
                st.error(f"Ocorreu um erro técnico na geração: {error}")