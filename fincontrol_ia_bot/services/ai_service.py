import logging
import os
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Configura o cliente Gemini usando a variável de ambiente GEMINI_API_KEY
# Se a variável não estiver definida, a biblioteca genai usará o padrão ou falhará na chamada
client = genai.Client() 

# Instruções de como a IA deve se comportar (System Prompt)
SYSTEM_INSTRUCTION = """
Você é o FincontrolIA, um assistente financeiro inteligente, amigável e direto.
O seu objetivo é ajudar o usuário a controlar seus gastos, classificar despesas e receitas, 
e fornecer conselhos financeiros curtos. 

Regras de comportamento:
1. Seja sempre prestativo, mas não seja prolixo. Resuma.
2. Se o usuário mandar um valor que parece um gasto, sugira uma categoria (ex: Alimentação, Transporte).
3. Nunca invente dados financeiros do usuário. Trabalhe apenas com o que ele te enviou.
4. Mantenha um tom profissional mas moderno (use emojis sem exagerar).
"""

async def gerar_resposta(conteudo: str, tipo_origem: str) -> str:
    """
    Função principal para gerar resposta baseada na entrada do usuário usando o Google Gemini.
    """
    logger.info(f"Gerando resposta Gemini para conteúdo do tipo: {tipo_origem}")

    try:
        # Preparar o prompt dependendo da origem
        if tipo_origem == "text":
            prompt = f"O usuário enviou a seguinte mensagem de texto:\n'{conteudo}'\n\nResponda diretamente a ele como o assistente FincontrolIA."
        elif tipo_origem == "audio":
            prompt = f"O usuário gravou um áudio que foi transcrito para:\n'{conteudo}'\n\nResponda diretamente a ele interpretando o que ele disse no áudio."
        elif tipo_origem == "image":
            prompt = f"O sistema de visão analisou uma imagem enviada pelo usuário e descreveu o seguinte:\n'{conteudo}'\n\nResponda ao usuário com base no que foi detectado na imagem."
        else:
            prompt = conteudo

        # Chamada para o modelo Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            )
        )
        
        return response.text
        
    except Exception as e:
        logger.error(f"Erro ao chamar a API do Gemini: {e}")
        return "Desculpe, tive um problema de conexão com meu cérebro de IA no momento. Tente novamente mais tarde!"

async def gerar_resposta_json(conteudo: str, tipo_origem: str) -> str:
    """
    Função dedicada para a integração Web no app.py que exige retornos estruturados 
    (JSON) para parsear e injetar no Banco de Dados automaticamente.
    """
    logger.info(f"Gerando JSON de resposta via Gemini para conteúdo: {tipo_origem}")

    JSON_INSTRUCTION = """
Você é o FincontrolIA. O usuário está no painel web.
Você DEVE SEMPRE responder em formato JSON estrito, sem textos adicionais fora do JSON.
Nenhum markdown extra em volta. Apenas o JSON puro ou num bloco ```json.

Formato OBRIGATÓRIO de retorno:
{
  "reply": "Sua resposta amigável formatada para humanos aqui.",
  "action": {
    "type": "expense" ou "income",
    "amount": 50.00,
    "category": "Food & Drink", 
    "description": "Starbucks"
  }
}
Se não for uma transação, apenas retorne "action": null.
Use categorias em inglês como: 'Housing', 'Groceries', 'Entertainment', 'Salary', 'Electronics', 'Food & Drink', 'Others'.
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=conteudo, 
            config=types.GenerateContentConfig(
                system_instruction=JSON_INSTRUCTION,
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        logger.error(f"Erro ao gerar JSON via Gemini: {e}")
        return '{"reply": "Erro de conexão com IA. Tente novamente.", "action": null}'
