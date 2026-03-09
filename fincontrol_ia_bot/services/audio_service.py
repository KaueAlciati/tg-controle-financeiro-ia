import logging
import os
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Configura o cliente Gemini usando a variável de ambiente GEMINI_API_KEY
client = genai.Client()

async def processar_audio(caminho_arquivo: str) -> str:
    """
    Usa o modelo Gemini 2.5 Flash para transcrever e entender o áudio.
    """
    logger.info(f"Processando áudio localizado em: {caminho_arquivo}")

    if not os.path.exists(caminho_arquivo):
        logger.error("Arquivo de áudio não encontrado.")
        return "Erro: Arquivo de áudio não pode ser lido."

    try:
        # Envia o arquivo temporário diretamente para o Gemini 
        # (Dependendo da SDK, um upload pode ser necessário para arquivos grandes,
        # mas para notas de voz curtas podemos anexar)
        
        # O Gemini 1.5 e 2.5 suportam áudio!
        uploaded_file = client.files.upload(file=caminho_arquivo)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                uploaded_file, 
                "Transcreva perfeitamente o que foi falado neste áudio. Não adicione comentários, apenas o texto falado."
            ]
        )
        
        transcript = response.text.strip()
        logger.info(f"Áudio transcrito com sucesso: {transcript}")
        
        # Deletar arquivo remotamente para economizar espaço
        client.files.delete(name=uploaded_file.name)
        
        return transcript

    except Exception as e:
        logger.error(f"Erro ao processar áudio via Gemini: {e}")
        return "(Falha ao transcrever o áudio enviado. Tente enviar texto.)"
