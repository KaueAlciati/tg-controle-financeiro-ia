from telegram import Update
from telegram.ext import ContextTypes
import os
import aiohttp

async def _download_file(file_id, bot_instance, target_path):
    file = await bot_instance.get_file(file_id)
    await file.download_to_drive(target_path)

async def handle_incoming_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from fincontrol_ia_bot.services import audio_service, image_service, ai_service

    message = update.message
    bot = context.bot

    if message.text:
        text = message.text
        # Process the text message using the AI service
        response = await ai_service.gerar_resposta(text, 'text')
        await update.message.reply_text(response)
    elif message.voice or message.audio:
         # Process audio message
        file_id = message.voice.file_id if message.voice else message.audio.file_id
        target_path = os.path.join(os.getcwd(), 'tmp_audio.ogg') # Basic temp file
        await _download_file(file_id, bot, target_path)

        text_from_audio = await audio_service.processar_audio(target_path)
        response = await ai_service.gerar_resposta(text_from_audio, 'audio')

        # Cleanup
        if os.path.exists(target_path):
             os.remove(target_path)

        await update.message.reply_text(response)
    elif message.photo:
         # Process photo message
        # Get highest res photo
        photo = message.photo[-1]
        file_id = photo.file_id
        target_path = os.path.join(os.getcwd(), 'tmp_image.jpg') # Basic temp file
        await _download_file(file_id, bot, target_path)

        image_description = await image_service.processar_imagem(target_path)
        response = await ai_service.gerar_resposta(image_description, 'image')

        # Cleanup
        if os.path.exists(target_path):
             os.remove(target_path)

        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Desculpe, eu não entendi esse formato de arquivo!")
