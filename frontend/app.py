import streamlit as st
import sys
import os

# 1. Configuração da página (Interface Moderna)
# Substituímos o emoji pela sua nova logo na aba do navegador
st.set_page_config(page_title="GlobalClause AI", page_icon="logo_global_pro.png")

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

# --- INTERFACE VISUAL MODERNA ---
# Exibe sua nova logo tecnológica no topo
if os.path.exists("logo_global_pro.png"):
    st.image("logo_global_pro.png", width=180)
else:
    # Caso a imagem ainda não tenha sido subida, mantém o título limpo
    st.title("GLOBALCLAUSE AI")

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

# --- LÓGICA DE PROCESSAMENTO (CORRIGIDA PARA NUVEM) ---
if botao_gerar:
    if not pergunta or not senha:
        st.warning("Por favor, preencha a pergunta e a senha antes de continuar.")
    else:
        with st.spinner("A IA está analisando sua solicitação e gerando o documento seguro..."):
            try:
                # SOLUÇÃO DEFINITIVA PARA O ERRO [Errno 2]:
                # Usamos a pasta /tmp, que é o padrão de gravação para servidores Linux (Streamlit Cloud)
                nome_arquivo_baixar = "Analise_GlobalClause.pdf"
                caminho_seguro = os.path.join("/tmp", nome_arquivo_baixar)
                
                # 1. O backend gera o PDF direto no caminho autorizado (/tmp)
                gerar_pdf_protegido(pergunta, senha, caminho_seguro)
                
                # 2. Sucesso!
                st.success("✅ Relatório gerado com sucesso!")
                
                # 3. Lemos o arquivo da pasta temporária para disponibilizar o download
                with open(caminho_seguro, "rb") as f:
                    st.download_button(
                        label="📥 Baixar Relatório (PDF)",
                        data=f,
                        file_name=nome_arquivo_baixar,
                        mime="application/pdf"
                    )
            except Exception as error:
                # Exibe o erro de forma clara se algo falhar
                st.error(f"Ocorreu um erro técnico na geração: {error}")

# Rodapé discreto
st.markdown("---")
st.caption("GlobalClause AI © 2026 | Inteligência Jurídica & Engenharia")