import os
import sys
from dotenv import load_dotenv
import logging

# Adiciona o diretório raiz ao path do Python para encontrar o pacote 'fincontrol_ia_bot'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fincontrol_ia_bot.integrations.telegram_bot import TelegramBot

# Carrega as variáveis do arquivo .env para o os.environ
load_dotenv()

# Configuração básica de Logging para o projeto inteiro
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """
    Ponto de entrada principal para a aplicação FincontrolIA.
    """
    logger.info("Iniciando o sistema FincontrolIA...")

    # Agora buscamos do arquivo .env (que foi carregado pelo load_dotenv)
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "COLOQUE_SEU_TOKEN_AQUI":
        logger.error(
            "⚠️ ATENÇÃO: Token do Telegram não configurado ou inválido.\n"
            "Verifique se você criou o arquivo '.env' na raiz do projeto e "
            "inseriu a linha TELEGRAM_BOT_TOKEN=seu_token_aqui"
        )
        return

    # Inicia a plataforma selecionada (neste caso, Telegram)
    try:
        telegram_bot = TelegramBot(token=TELEGRAM_TOKEN)
        telegram_bot.start()
    except Exception as e:
        logger.error(f"Ocorreu um erro fatal ao iniciar o bot do Telegram: {e}")

if __name__ == "__main__":
    main()
