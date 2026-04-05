import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Ferramentas para um layout profissional que pula linha sozinho
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pypdf import PdfReader, PdfWriter

# 1. Configurações de Soberania (Ambiente)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def gerar_pdf_protegido(texto, nome_arquivo, senha):
    """Cria um PDF profissional com ajuste automático de texto e senha"""
    temp_pdf = "temp.pdf"
    
    # Configura o documento com margens seguras
    doc = SimpleDocTemplate(temp_pdf, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []

    # Cabeçalho da sua marca (Sua "Hapa")
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph("<b>GENAILMA COUTO - GESTÃO & TECH</b>", estilos["Title"]))
    elementos.append(Paragraph(f"<i>GlobalClause Intelligence | Gerado em: {agora}</i>", estilos["Italic"]))
    elementos.append(Spacer(1, 24))

    # Conteúdo: O Paragraph faz o texto pular linha sozinho e aceita negrito!
    texto_com_quebras = texto.replace('\n', '<br/>')
    elementos.append(Paragraph(texto_com_quebras, estilos["Normal"]))
    
    # Constrói o PDF básico
    doc.build(elementos)

    # 2. Adicionando o "Cadeado" (Criptografia)
    reader = PdfReader(temp_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    
    writer.encrypt(senha)
    with open(nome_arquivo, "wb") as f:
        writer.write(f)
    
    os.remove(temp_pdf) # Limpa o rascunho
    print(f"✅ Documento '{nome_arquivo}' gerado e trancado com sucesso!")

def executar_global_clause():
    print("\n--- 🌍 BEM-VINDA AO GLOBALCLAUSE ---")
    
    # 1. Entrada de dados dinâmica
    pergunta = input("O que você deseja analisar hoje? ")
    senha = input("Defina a senha para este relatório: ")
    
    print("\n🤖 Consultando a inteligência artificial...")
    
    # 2. Chamada da IA (Usa o modelo que você já configurou)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": pergunta}]
    )
    
    resposta = completion.choices[0].message.content
    
    # 3. Geração do Relatório Personalizado
    nome_doc = "Relatorio_GlobalClause.pdf"
    gerar_pdf_protegido(resposta, nome_doc, senha)
    
    print(f"\n🚀 Finalizado! O arquivo {nome_doc} está pronto para uso.")

if __name__ == "__main__":
    executar_global_clause()