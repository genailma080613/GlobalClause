import os
from groq import Groq
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def testar_agente():
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Olá! Você é o agente GlobalClause. Confirme se está pronto para analisar leis de Montenegro."}]
    )
    print("--- RESPOSTA DA IA ---")
    print(completion.choices[0].message.content)

testar_agente()