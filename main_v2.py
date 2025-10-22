# main.py
# Asosiy bot fayli - SUPER OSON TIL TIZIMI

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import qilish
from config import BOT_TOKEN
from database import init_database
from keyboards_all_lang import (
    get_language_keyboard,
    get_main_menu_keyboard,
    get_settings_keyboard,
    TEXTS
)
from utils import is_admin, lang, t, get_button  # SUPER OSON HELPER!

# Handlerlarni import qilish
from handlers.complaints.complaint_v2 import (
    start_complaint,
    handle_direction_choice,
    handle_course_choice,
    handle_complaint_type_choice,
    handle_subject_entry,
    handle_teacher_entry,
    handle_complaint_message
)
from handlers.rules.rules_v2 import (
    show_rules_main,
    show_grading_rules,
    show_exam_rules,
    show_general_rules,
    download_pdf
)
from handlers.surveys.survey_v2 import (
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
    show_dashboard
)

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda - til tanlash"""
    context.user_data.clear()

    # Agar til tanlanmagan bo'lsa, til tanlash menyusini ko'rsatish
    if 'language' not in context.user_data:
        context.user_data['state'] = 'choosing_language'
        await update.message.reply_text(
            "🌐 Tilni tanlang / Choose language / Выберите язык:",
            reply_markup=get_language_keyboard()
        )
    else:
        # Agar til tanlangan bo'lsa, asosiy menyuni ko'rsatish
        await show_main_menu(update, context)


async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Til tanlash"""
    text = update.message.text

    # Tilni aniqlash
    if "🇺🇿" in text or "O'zbek tili" in text:
        selected_lang = "uz"
    elif "🇬🇧" in text or "English" in text:
        selected_lang = "en"
    elif "🇷🇺" in text or "Русский" in text:
        selected_lang = "ru"
    else:
        selected_lang = "uz"

    # Tilni saqlash
    context.user_data['language'] = selected_lang
    context.user_data['state'] = 'main_menu'

    # Tasdiqlash xabari - OSON!
    await update.message.reply_text(t('language_selected', context))

    # Asosiy menyuni ko'rsatish
    await show_main_menu(update, context)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyuni ko'rsatish - OSON!"""
    context.user_data['state'] = 'main_menu'

    await update.message.reply_text(
        t('welcome', context),  # Qara qanday oson!
        reply_markup=get_main_menu_keyboard(lang(context))
    )


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalarni ko'rsatish - OSON!"""
    context.user_data['state'] = 'settings'

    await update.message.reply_text(
        t('settings_menu', context),  # Oson!
        reply_markup=get_settings_keyboard(lang(context))
    )


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyu tugmalarini boshqarish"""
    text = update.message.text
    user_lang = lang(context)  # Bir marta oldik!

    # Til bo'yicha tugmalarni tekshirish
    main_menu = TEXTS["main_menu"][user_lang]

    if text == main_menu[0]:  # Murojaat
        await start_complaint(update, context)

    elif text == main_menu[1]:  # Tartib qoidalar
        await show_rules_main(update, context)

    elif text == main_menu[2]:  # So'rovnoma
        await show_survey_main(update, context)

    elif text == main_menu[3]:  # Admin
        await show_admin_panel(update, context)

    elif text == main_menu[4]:  # Sozlamalar
        await show_settings(update, context)

    # Orqaga tugmasi - hammasi bitta!
    elif text in [get_button("back", context)]:
        await show_main_menu(update, context)


async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar menyusini boshqarish"""
    text = update.message.text
    user_lang = lang(context)

    settings_menu = TEXTS["settings"][user_lang]

    if text == settings_menu[0]:  # Tilni o'zgartirish
        context.user_data['state'] = 'choosing_language'
        await update.message.reply_text(
            "🌐 Tilni tanlang / Choose language / Выберите язык:",
            reply_markup=get_language_keyboard()
        )

    elif text == settings_menu[1]:  # Orqaga
        await show_main_menu(update, context)


async def handle_complaint_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text
    back_btn = get_button("back", context)  # Bir marta oldik!

    # Orqaga tugmasi
    if text == back_btn:
        if state in ['choosing_direction', 'rules_main', 'survey_main', 'admin_panel']:
            await show_main_menu(update, context)
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
    user_lang = lang(context)

    rules_menu = TEXTS["rules"][user_lang]

    if text == rules_menu[0]:  # Baholash jarayoni
        await show_grading_rules(update, context)

    elif text == rules_menu[1]:  # Imtihon jarayoni
        await show_exam_rules(update, context)

    elif text == rules_menu[2]:  # Umumiy tartib qoida
        if state == 'rules_main':
            await show_general_rules(update, context)
        else:
            await show_rules_main(update, context)

    elif text == rules_menu[3]:  # Bosh sahifa
        await show_main_menu(update, context)

    elif text == t("download_pdf", context):
        await download_pdf(update, context)

    elif text == get_button("back", context):
        await show_rules_main(update, context)


async def handle_survey_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma jarayonini boshqarish"""
    text = update.message.text
    user_lang = lang(context)

    survey_menu = TEXTS["survey"][user_lang]

    if text == survey_menu[0]:  # O'qituvchilar haqida
        await show_teachers_survey(update, context)

    elif text == survey_menu[1]:  # Talim sifati
        await show_education_survey(update, context)

    elif text == survey_menu[2]:  # Ish beruvchilar
        await show_employers_survey(update, context)

    elif "So'rovnomaga" in text or "Survey" in text or "Опрос" in text:
        await open_survey_link(update, context)

    elif "Natijalar" in text or "Results" in text or "Результаты" in text:
        await show_survey_results(update, context)

    elif text == get_button("back", context):
        await show_main_menu(update, context)


async def handle_admin_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel jarayonini boshqarish"""
    if not is_admin(update.effective_user.id):
        # Xato xabari - super oson!
        error_messages = {
            "uz": "❌ Sizga ruxsat berilmagan!",
            "en": "❌ Access denied!",
            "ru": "❌ Доступ запрещен!"
        }
        await update.message.reply_text(error_messages[lang(context)])
        return

    text = update.message.text
    user_lang = lang(context)
    admin_menu = TEXTS["admin"][user_lang]

    if text == admin_menu[0]:  # Statistikalar
        await show_statistics(update, context)

    elif text == admin_menu[1]:  # Murojaatlarni ko'rish
        await view_complaints(update, context)

    elif text == admin_menu[2]:  # Excel export
        await export_to_excel_handler(update, context)

    elif text == admin_menu[3]:  # Dashboard
        await show_dashboard(update, context)

    elif text == admin_menu[4]:  # Asosiy menyu
        await show_main_menu(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha matnli xabarlarni boshqarish"""
    text = update.message.text
    state = context.user_data.get('state', '')

    # Til tanlash
    if state == 'choosing_language':
        await handle_language_choice(update, context)
        return

    # Sozlamalar
    if state == 'settings':
        await handle_settings(update, context)
        return

    # Asosiy menyu
    main_menu_items = []
    for l in ["uz", "en", "ru"]:
        main_menu_items.extend(TEXTS["main_menu"][l])

    if text in main_menu_items:
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
    await show_main_menu(update, context)


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