import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from fincontrol_ia_bot.core.message_router import handle_incoming_message

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Handles connection with Telegram and routes messages to core/message_router.py
    """
    def __init__(self, token: str):
        self.token = token
        # Initialize Application
        self.app = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Register command and message handlers"""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))

        # Message handlers for text
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_incoming_message))
        
        # Message handlers for audio/voice notes
        self.app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_incoming_message))
        
        # Message handlers for images
        self.app.add_handler(MessageHandler(filters.PHOTO, handle_incoming_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        welcome_text = (
            "Olá! Eu sou o FincontrolIA. 🤖\n\n"
            "Envie-me suas transações financeiras em formato de:\n"
            "📝 Texto\n"
            "🎙️ Áudio\n"
            "📸 Imagem (recibos, notas fiscais, etc.)\n\n"
            "Estou aqui para te ajudar a manter o controle!"
        )
        await update.message.reply_text(welcome_text)

    def start(self):
        """Start the bot."""
        logger.info("Iniciando o FincontrolIA no Telegram...")
        # Run the bot until the user presses Ctrl-C
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
