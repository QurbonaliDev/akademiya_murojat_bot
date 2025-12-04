# main.py
# Asosiy bot fayli - barcha komponentlarni birlashtiradi

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import qilish
from config.config import BOT_TOKEN, SELECTED_LANGUAGE
from database import init_database
from keyboards.keyboards import get_main_menu_keyboard
from utils.utils import is_admin

# Handlerlarni import qilish
from handlers.complaints.complaint import (
    start_complaint,
    handle_faculty_choice,
    handle_direction_choice,
    handle_education_type_choice,
    handle_education_lang_choice,
    handle_course_choice,
    handle_complaint_type_choice,
    handle_subject_entry,
    handle_teacher_entry,
    handle_complaint_message
)

from handlers.ratings.lesson_daily_rating import (
    start_lesson_daily_rating,
    handle_lesson_direction_choice,
    handle_lesson_course_choice,
    handle_subject_name,
    handle_teacher_name,
    handle_rating
)
from handlers.rules.rules import (
    show_rules_main,
    show_grading_rules,
    show_exam_rules,
    show_general_rules,
    download_pdf
)
from handlers.surveys.survey import (
    show_survey_main,
    show_teachers_survey,
    show_education_survey,
    show_employers_survey,
    open_survey_link,
    show_survey_results
)
from handlers.admins.admin import (
    show_admin_panel,
    show_statistics,
    view_complaints,
    export_to_excel_handler,
    export_to_daily_lesson_excel_handler,
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
    text = update.message.text

    if text == "📝 Murojaat":
        await start_complaint(update, context)

    elif text == "📋 Tartib qoidalar":
        await show_rules_main(update, context)

    elif text == "📊 So'rovnoma":
        await show_survey_main(update, context)

    elif text == "👨‍💼 Admin":
        await show_admin_panel(update, context)

    elif text == "🧑‍🏫 Kunlik darsni baholash":
        await start_lesson_daily_rating(update, context)

    elif text == "🌐 Til tanlash" :
        await start(update, context)

    elif text == "🔙 Asosiy menyu" or text == "🔙 Orqaga":
        await start(update, context)



async def handle_select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Til tanlash jarayonini boshqarish"""
    language = update.message.text
    context.user_data['language'] = language
    SELECTED_LANGUAGE = language
    await start(update, context)


async def handle_complaint_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text

    # 🔙 Orqaga tugmasi
    if text == "🔙 Orqaga":
        if state in ['choosing_faculty', 'rules_main', 'survey_main', 'admin_panel']:
            await start(update, context)

        elif state in ['choosing_direction']:
            context.user_data['state'] = 'choosing_faculty'
            await start_complaint(update, context)

        elif state in ['choosing_course', 'choosing_complaint_type']:
            await start_complaint(update, context)

        elif state in ['entering_subject', 'entering_teacher', 'entering_message']:
            context.user_data['state'] = 'choosing_complaint_type'
            await handle_course_choice(update, context)

        elif state in ['rules_grading', 'rules_exam', 'rules_general']:
            await show_rules_main(update, context)

        elif state in ['survey_teachers', 'survey_education', 'survey_employers']:
            await show_survey_main(update, context)

        return

    # =============================
    # 🔽 Murojaat jarayoni oqimi
    # =============================

    # 1️⃣ Fakultet tanlash
    if state == 'choosing_faculty':
        await handle_faculty_choice(update, context)
        return

    # 2️⃣ Yo‘nalish tanlash
    elif state == 'choosing_direction':
        await handle_direction_choice(update, context)
        return

    # 2️⃣ Ta'lim yo'nalishini
    elif state == 'choosing_education_type':
        await handle_education_type_choice(update, context)
        return

    # 2️⃣ Ta'lim tilini tanlash
    elif state == 'choosing_education_lang':
        await handle_education_lang_choice(update, context)
        return

    # 3️⃣ Kurs tanlash
    elif state == 'choosing_course':
        await handle_course_choice(update, context)
        return

    # 4️⃣ Murojaat turi
    elif state == 'choosing_complaint_type':
        await handle_complaint_type_choice(update, context)
        return

    # 5️⃣ Fan kiritish
    elif state == 'entering_subject':
        await handle_subject_entry(update, context)
        return

    # 6️⃣ O‘qituvchi ismi kiritish
    elif state == 'entering_teacher':
        await handle_teacher_entry(update, context)
        return

    # 7️⃣ Murojaat matnini kiritish
    elif state == 'entering_message':
        await handle_complaint_message(update, context)
        return



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

    elif text == "📤 Kunlik dars hisoboti excel":
        await export_to_daily_lesson_excel_handler(update, context)

    elif text == "📈 Dashboard":
        await show_dashboard(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha matnli xabarlarni boshqarish"""
    text = update.message.text
    state = context.user_data.get('state', '')

    # Asosiy menyu
    if text in ["📝 Murojaat", "📋 Tartib qoidalar",
                "📊 So'rovnoma", "🧑‍🏫 Kunlik darsni baholash",
                "👨‍💼 Admin", "🔙 Asosiy menyu"]:
        await handle_main_menu(update, context)
        return

    # Murojaat jarayoni
    if state in ['choosing_faculty','choosing_direction',
                 'choosing_education_type', 'choosing_education_lang', 'choosing_course', 'choosing_complaint_type',
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

    state = context.user_data.get('state')

    # Kunlik darsni baholash jarayoni
    if state == 'rating_direction':
        return await handle_lesson_direction_choice(update, context)
    if state == 'rating_course':
        return await handle_lesson_course_choice(update, context)
    if state == 'rating_subject':
        return await handle_subject_name(update, context)
    if state == 'rating_teacher':
        return await handle_teacher_name(update, context)
    if state == 'rating_process':
        return await handle_rating(update, context)

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