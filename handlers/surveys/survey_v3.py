from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards_all_lang_v2 import get_survey_keyboard, get_back_keyboard
from config.config import SURVEY_LINKS
from utils.utils_v2 import t, lang
from text.texts_v2 import TEXTS

async def show_survey_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'survey_main'
    await update.message.reply_text(
        t('s_r', context),
        reply_markup=get_survey_keyboard(context)
    )

async def show_teachers_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'survey_teachers'
    context.user_data['current_survey'] = 'teachers'
    link = SURVEY_LINKS.get('teachers')
    await update.message.reply_text(
        t('survey_teachers_text', context, link=link),
        reply_markup=get_back_keyboard(context)
    )

async def show_education_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'survey_education'
    context.user_data['current_survey'] = 'education'
    link = SURVEY_LINKS.get('education')
    await update.message.reply_text(
        t('survey_education_text', context, link=link),
        reply_markup=get_back_keyboard(context)
    )

async def show_employers_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'survey_employers'
    context.user_data['current_survey'] = 'employers'
    link = SURVEY_LINKS.get('employers')
    await update.message.reply_text(
        t('survey_employers_text', context, link=link),
        reply_markup=get_back_keyboard(context)
    )

async def open_survey_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    survey_type = context.user_data.get('current_survey')
    if not survey_type:
        await update.message.reply_text(t('survey_choose_first', context))
        return
    link = SURVEY_LINKS.get(survey_type)
    await update.message.reply_text(
        t('survey_open_link', context, link=link) if link else t('survey_link_not_found', context)
    )

async def show_survey_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    survey_type = context.user_data.get('current_survey')
    if not survey_type:
        await update.message.reply_text(t('survey_choose_first', context))
        return
    link = SURVEY_LINKS.get(survey_type)
    await update.message.reply_text(
        t('survey_results', context, link=f"{link}&viewanalytics=1") if link else t('survey_link_not_found', context)
    )

async def handle_survey_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_lang = lang(context)
    survey_menu = TEXTS["survey"][user_lang]
    handlers = {
        survey_menu[0]: show_teachers_survey,
        survey_menu[1]: show_education_survey,
        survey_menu[2]: show_employers_survey,
        t('survey_open', context): open_survey_link,
        t('survey_results', context): show_survey_results,
    }
    handler = handlers.get(text, show_survey_main)
    await handler(update, context)