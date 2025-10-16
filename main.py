# main.py
# Asosiy bot fayli - barcha komponentlarni birlashtiradi

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import qilish
from config import BOT_TOKEN, DIRECTIONS, COURSES, COMPLAINT_TYPES
from database import init_database
from keyboards import get_main_menu_keyboard
from utils import is_admin

# Handlerlarni import qilish
from handlers.complaint import (
    start_complaint,
    handle_direction_choice,
    handle_course_choice,
    handle_complaint_type_choice,
    handle_subject_entry,
    handle_teacher_entry,
    handle_complaint_message
)
from handlers.rules import (
    show_rules_main,
    show_grading_rules,
    show_exam_rules,
    show_general_rules,
    download_pdf
)
from handlers.survey import (
    show_survey_main,
    show_teachers_survey,
    show_education_survey,
    show_employers_survey,
    open_survey_link,
    show_survey_results
)
from handlers.admin import (
    show_admin_panel,
    show_statistics,
    view_complaints,
    export_to_excel_handler,
    show_dashboard
)

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda"""
    context.user_data.clear()

    welcome_text = (
        "🎓 Talim tizimi monitoring botiga xush kelibsiz!\n\n"
        "Bu bot orqali siz:\n"
        "📝 Anonim murojaat qilishingiz\n"
        "📋 Tartib qoidalar bilan tanishishingiz\n"
        "📊 So'rovnomalarda qatnashishingiz mumkin\n\n"
        "Quyidagi tugmalardan birini tanlang:"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyu tugmalarini boshqarish"""
    text = update.message.text

    if text == "📝 Murojaat":
        await start_complaint(update, context)

    elif text == "📋 Tartib qoidalar":
        await show_rules_main(update, context)

    elif text == "📊 So'rovnoma":
        await show_survey_main(update, context)

    elif text == "👨‍💼 Admin":
        await show_admin_panel(update, context)

    elif text == "🔙 Asosiy menyu" or text == "🔙 Orqaga":
        await start(update, context)


async def handle_complaint_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text

    # Orqaga tugmasi
    if text == "🔙 Orqaga":
        if state in ['choosing_direction', 'rules_main', 'survey_main', 'admin_panel']:
            await start(update, context)
        elif state == 'choosing_course':
            await start_complaint(update, context)
        elif state == 'choosing_complaint_type':
            await start_complaint(update, context)
        elif state in ['entering_subject', 'entering_teacher', 'entering_message']:
            context.user_data['state'] = 'choosing_complaint_type'
            await handle_course_choice(update, context)
        elif state in ['rules_grading', 'rules_exam', 'rules_general']:
            await show_rules_main(update, context)
        elif state in ['survey_teachers', 'survey_education', 'survey_employers']:
            await show_survey_main(update, context)
        return

    # Murojaat jarayoni
    if state == 'choosing_direction':
        await handle_direction_choice(update, context)

    elif state == 'choosing_course':
        await handle_course_choice(update, context)

    elif state == 'choosing_complaint_type':
        await handle_complaint_type_choice(update, context)

    elif state == 'entering_subject':
        await handle_subject_entry(update, context)

    elif state == 'entering_teacher':
        await handle_teacher_entry(update, context)

    elif state == 'entering_message':
        await handle_complaint_message(update, context)


async def handle_rules_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tartib qoidalar jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text

    if text == "📊 Baholash jarayoni":
        await show_grading_rules(update, context)

    elif text == "📝 Imtihon jarayoni":
        await show_exam_rules(update, context)

    elif text == "📋 Umumiy tartib qoida":
        if state == 'rules_main':
            await show_general_rules(update, context)
        else:
            await show_rules_main(update, context)

    elif text == "🔙 Bosh sahifa":
            await start(update, context)

    elif text == "📥 PDF yuklab olish":
        await download_pdf(update, context)

    elif text == "🔙 Orqaga":
        await show_rules_main(update, context)


async def handle_survey_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma jarayonini boshqarish"""
    text = update.message.text

    if text == "👨‍🏫 O'qituvchilar haqida":
        await show_teachers_survey(update, context)

    elif text == "🎓 Talim sifati":
        await show_education_survey(update, context)

    elif text == "💼 Ish beruvchilar":
        await show_employers_survey(update, context)

    elif text == "🔗 So'rovnomaga o'tish":
        await open_survey_link(update, context)

    elif text == "📊 Natijalarni ko'rish":
        await show_survey_results(update, context)

    elif text == "🔙 Orqaga":
        await handle_main_menu(update, context)


async def handle_admin_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel jarayonini boshqarish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    text = update.message.text

    if text == "📊 Statistikalar":
        await show_statistics(update, context)

    elif text == "📋 Murojaatlarni ko'rish":
        await view_complaints(update, context)

    elif text == "📤 Excel export":
        await export_to_excel_handler(update, context)

    elif text == "📈 Dashboard":
        await show_dashboard(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha matnli xabarlarni boshqarish"""
    text = update.message.text
    state = context.user_data.get('state', '')

    # Asosiy menyu
    if text in ["📝 Murojaat", "📋 Tartib qoidalar", "📊 So'rovnoma", "👨‍💼 Admin", "🔙 Asosiy menyu"]:
        await handle_main_menu(update, context)
        return

    # Murojaat jarayoni
    if state in ['choosing_direction', 'choosing_course', 'choosing_complaint_type',
                 'entering_subject', 'entering_teacher', 'entering_message']:
        await handle_complaint_flow(update, context)
        return

    # Tartib qoidalar
    if state in ['rules_main', 'rules_grading', 'rules_exam', 'rules_general']:
        await handle_rules_flow(update, context)
        return

    # So'rovnoma
    if state in ['survey_main', 'survey_teachers', 'survey_education', 'survey_employers']:
        await handle_survey_flow(update, context)
        return

    # Admin panel
    if state == 'admin_panel':
        await handle_admin_flow(update, context)
        return

    # Default - asosiy menyuga qaytish
    await start(update, context)


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin komandasi"""
    await show_admin_panel(update, context)


def main():
    """Asosiy funksiya - botni ishga tushirish"""
    # Ma'lumotlar bazasini yaratish
    init_database()
    logger.info("Ma'lumotlar bazasi ishga tushirildi")

    # Bot applicationni yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Botni ishga tushirish
    logger.info("Bot ishga tushmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()