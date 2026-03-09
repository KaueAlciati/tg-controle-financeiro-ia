import logging
import os
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Configura o cliente Gemini
client = genai.Client()

async def processar_imagem(caminho_arquivo: str) -> str:
    """
    Usa o modelo Gemini 2.5 Flash para extrair dados (OCR ou descrição visual) da imagem.
    """
    logger.info(f"Processando imagem localizada em: {caminho_arquivo}")

    if not os.path.exists(caminho_arquivo):
        logger.error("Arquivo de imagem não encontrado.")
        return "Erro: Arquivo de imagem não pode ser lido."

    try:
        # Faz upload temporário para a File API do Gemini (ótimo para visão)
        uploaded_file = client.files.upload(file=caminho_arquivo)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                uploaded_file, 
                "Olhe para esta imagem (provavelmente é uma fatura, boleto ou recibo financeiro). "
                "Extraia o máximo de informações possíveis como Valor Total, Local, Data, "
                "e faça um breve parágrafo descrevendo o contexto principal."
            ]
        )
        
        description = response.text.strip()
        logger.info("Imagem processada com sucesso pelo Vision.")
        
        # Opcional, excluir arquivo.
        client.files.delete(name=uploaded_file.name)
        
        return description

    except Exception as e:
        logger.error(f"Erro ao processar imagem via Gemini: {e}")
        return "(Falha ao processar e ler a imagem. Tente descrever em texto.)"
