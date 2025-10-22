# handlers/survey.py
# So'rovnoma bilan bog'liq handlerlar (dinamik til bilan)

from telegram import Update
from telegram.ext import ContextTypes
# from keyboards import get_survey_keyboard, get_survey_links_keyboard
from keyboards_all_lang import get_survey_keyboard, get_back_keyboard
from config import SURVEY_LINKS
from utils import t, lang


async def show_survey_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma asosiy menyusi"""
    context.user_data['state'] = 'survey_main'

    await update.message.reply_text(
        t('s_r', context),
        reply_markup=get_survey_keyboard(lang(context))
    )


async def show_teachers_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilar haqida so'rovnoma"""
    context.user_data['state'] = 'survey_teachers'
    context.user_data['current_survey'] = 'teachers'

    link = SURVEY_LINKS.get('teachers')

    text = t('survey_teachers_text', context).format(link=link)
    await update.message.reply_text(text, reply_markup=get_back_keyboard(lang(context)))


async def show_education_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ta'lim sifati so'rovnomasi"""
    context.user_data['state'] = 'survey_education'
    context.user_data['current_survey'] = 'education'

    link = SURVEY_LINKS.get('education')

    text = t('survey_education_text', context).format(link=link)
    await update.message.reply_text(text, reply_markup=get_back_keyboard(lang(context)))


async def show_employers_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ish beruvchilar so'rovnomasi"""
    context.user_data['state'] = 'survey_employers'
    context.user_data['current_survey'] = 'employers'

    link = SURVEY_LINKS.get('employers')

    text = t('survey_employers_text', context).format(link=link)
    await update.message.reply_text(text, reply_markup=get_back_keyboard(lang(context)))


async def open_survey_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma havolasini ochish"""
    survey_type = context.user_data.get('current_survey')

    if not survey_type:
        await update.message.reply_text(t('survey_choose_first', context))
        return

    link = SURVEY_LINKS.get(survey_type)

    if link:
        await update.message.reply_text(
            t('survey_open_link', context).format(link=link)
        )
    else:
        await update.message.reply_text(t('survey_link_not_found', context))


async def show_survey_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma natijalarini ko'rsatish"""
    survey_type = context.user_data.get('current_survey')

    if not survey_type:
        await update.message.reply_text(t('survey_choose_first', context))
        return

    link = SURVEY_LINKS.get(survey_type)

    if link:
        results_link = f"{link}&viewanalytics=1"
        await update.message.reply_text(
            t('survey_results', context).format(link=results_link)
        )
    else:
        await update.message.reply_text(t('survey_link_not_found', context))
