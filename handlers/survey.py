# handlers/survey.py
# So'rovnoma bilan bog'liq handlerlar

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_survey_keyboard, get_survey_links_keyboard
from config import SURVEY_LINKS


async def show_survey_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma asosiy menyusi"""
    context.user_data['state'] = 'survey_main'

    await update.message.reply_text(
        "📊 So'rovnoma bo'limi:\n\nQuyidagi so'rovnomalardan birini tanlang:",
        reply_markup=get_survey_keyboard()
    )


async def show_teachers_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilar haqida so'rovnoma"""
    context.user_data['state'] = 'survey_teachers'
    context.user_data['current_survey'] = 'teachers'

    link = SURVEY_LINKS.get('teachers')

    text = (
        "👨‍🏫 O'qituvchilar haqida so'rovnoma\n\n"
        "Ushbu so'rovnomada o'qituvchilarning dars o'tish uslubi, "
        "talabalar bilan muloqoti va kasbiy mahorati haqida fikr bildiring.\n\n"
        f"🔗 Havola: {link}\n\n"
        "So'rovnoma to'liq anonim tarzda o'tkaziladi."
    )

    await update.message.reply_text(text, reply_markup=get_survey_links_keyboard())


async def show_education_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ta'lim sifati so'rovnomasi"""
    context.user_data['state'] = 'survey_education'
    context.user_data['current_survey'] = 'education'

    link = SURVEY_LINKS.get('education')

    text = (
        "🎓 Ta'lim sifati so'rovnomasi\n\n"
        "Bu so'rovnomada ta'lim jarayoni, o'quv dasturlari va ta'lim sifati "
        "haqida fikr bildiring.\n\n"
        f"🔗 Havola: {link}\n\n"
        "So'rovnoma to'liq anonim shaklda o'tkaziladi."
    )

    await update.message.reply_text(text, reply_markup=get_survey_links_keyboard())


async def show_employers_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ish beruvchilar so'rovnomasi"""
    context.user_data['state'] = 'survey_employers'
    context.user_data['current_survey'] = 'employers'

    link = SURVEY_LINKS.get('employers')

    text = (
        "💼 Ish beruvchilar so'rovnomasi\n\n"
        "Ushbu so'rovnomada bitiruvchilarning kasbiy ko'nikmalari "
        "va mehnat bozoriga tayyorgarligi haqida fikr bildiring.\n\n"
        f"🔗 Havola: {link}\n\n"
        "So'rovnoma to'liq anonim tarzda o'tkaziladi."
    )

    await update.message.reply_text(text, reply_markup=get_survey_links_keyboard())


async def open_survey_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma havolasini ochish"""
    survey_type = context.user_data.get('current_survey')

    if not survey_type:
        await update.message.reply_text("❌ Avval so'rovnoma turini tanlang.")
        return

    link = SURVEY_LINKS.get(survey_type)

    if link:
        await update.message.reply_text(
            f"🔗 Quyidagi havola orqali so'rovnomaga o'ting:\n\n{link}"
        )
    else:
        await update.message.reply_text("❌ Havola topilmadi.")


async def show_survey_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma natijalarini ko'rsatish"""
    survey_type = context.user_data.get('current_survey')

    if not survey_type:
        await update.message.reply_text("❌ Avval so'rovnoma turini tanlang.")
        return

    link = SURVEY_LINKS.get(survey_type)

    if link:
        results_link = f"{link}&viewanalytics=1"
        await update.message.reply_text(
            f"📊 So'rovnoma natijalarini ko'rish:\n\n{results_link}"
        )
    else:
        await update.message.reply_text("❌ Havola topilmadi.")
