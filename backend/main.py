import os
import streamlit as st
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pypdf import PdfReader, PdfWriter

# 1. Carrega o .env (funciona apenas localmente no seu PC)
load_dotenv()

# 2. BUSCA A CHAVE NO LUGAR CERTO (O segredo está aqui!)
# Tenta pegar do 'Secrets' do Streamlit (nuvem). Se não achar, pega do '.env' (PC)
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("ERRO: API Key não encontrada! Verifique o painel Secrets no Streamlit.")
    st.stop()

# 3. Configura o cliente com a chave encontrada
client = Groq(api_key=api_key)

def gerar_pdf_protegido(pergunta, senha, caminho_final):
    # 🤖 Chamada da IA
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": pergunta}]
        )
        texto_ia = completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Erro na Groq: {e}")

    # 📂 Define rascunho temporário na mesma pasta do arquivo final
    pasta_temp = os.path.dirname(caminho_final)
    temp_pdf = os.path.join(pasta_temp, "rascunho_processo.pdf")
    
    doc = SimpleDocTemplate(temp_pdf, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []

    # Conteúdo do PDF
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph("<b>GLOBALCLAUSE AI - RELATÓRIO SEGURO</b>", estilos["Title"]))
    elementos.append(Paragraph(f"<i>Gerado por Genailma Couto em: {agora}</i>", estilos["Italic"]))
    elementos.append(Spacer(1, 24))
    
    texto_formatado = texto_ia.replace('\n', '<br/>')
    elementos.append(Paragraph(texto_formatado, estilos["Normal"]))
    doc.build(elementos)

    # 🔐 Criptografia
    reader = PdfReader(temp_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    
    writer.encrypt(senha)
    with open(caminho_final, "wb") as f:
        writer.write(f)
    
    # Limpa o arquivo temporário
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)