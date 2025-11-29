import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.config import BOT_TOKEN
from database import init_database
from keyboards.keyboards_all_lang_v2 import get_language_keyboard
from dispatcher import HandlerDispatcher
from handlers.admins.admin_v2 import show_admin_panel
from utils.utils_v2 import t, lang

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data['state'] = 'choosing_language'
    logger.debug("Start command: setting state to choosing_language")
    await update.message.reply_text(
        t('choose_language', context),
        reply_markup=get_language_keyboard()
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Handling text: {update.message.text}, state: {context.user_data.get('state')}")
    dispatcher = HandlerDispatcher()
    await dispatcher.dispatch(update, context)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Admin command triggered")
    await show_admin_panel(update, context)

def main():
    init_database()
    logger.info("Ma'lumotlar bazasi ishga tushirildi")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    logger.info("Bot ishga tushmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()