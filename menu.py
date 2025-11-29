from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards_all_lang_v2 import get_main_menu_keyboard
from utils.utils_v2 import t, lang
import logging

logger = logging.getLogger(__name__)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyuni ko'rsatish"""
    context.user_data['state'] = 'main_menu'
    logger.debug("Showing main menu")
    await update.message.reply_text(
        t('welcome', context),
        reply_markup=get_main_menu_keyboard(context)
    )