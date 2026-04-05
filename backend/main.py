import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pypdf import PdfReader, PdfWriter

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def gerar_pdf_protegido(pergunta, senha, caminho_final):
    # 🤖 Chamada da IA
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": pergunta}]
    )
    texto_ia = completion.choices[0].message.content

    # 📂 Define rascunho temporário
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
    
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)