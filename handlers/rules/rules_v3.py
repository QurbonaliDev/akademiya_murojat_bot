from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards_all_lang_v2 import get_rules_keyboard, get_rules_detail_keyboard
from config.config import PDF_FILES
from utils.utils_v2 import t, lang
from text.texts_v2 import TEXTS
from main_v2 import show_main_menu
import os

async def show_rules_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'rules_main'
    await update.message.reply_text(
        t('rules_main_intro', context),
        reply_markup=get_rules_keyboard(context)
    )

async def show_grading_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'rules_grading'
    context.user_data['current_pdf'] = 'grading'
    await update.message.reply_text(
        t('grading_rules_text', context),
        reply_markup=get_rules_detail_keyboard(context)
    )

async def show_exam_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'rules_exam'
    context.user_data['current_pdf'] = 'exam'
    await update.message.reply_text(
        t('exam_rules_text', context),
        reply_markup=get_rules_detail_keyboard(context)
    )

async def show_general_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 'rules_general'
    context.user_data['current_pdf'] = 'rules'
    await update.message.reply_text(
        t('general_rules_text', context),
        reply_markup=get_rules_detail_keyboard(context)
    )

async def download_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_type = context.user_data.get('current_pdf')
    if not pdf_type:
        await update.message.reply_text(t('rules_select_first', context))
        return
    pdf_name = PDF_FILES.get(pdf_type, 'document.pdf')
    if os.path.exists(pdf_name):
        with open(pdf_name, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=pdf_name,
                caption=t('rules_pdf_caption', context, pdf_name=pdf_name)
            )
    else:
        await update.message.reply_text(t('rules_pdf_not_found', context))

async def handle_rules_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_lang = lang(context)
    rules_menu = TEXTS["rules"][user_lang]
    handlers = {
        rules_menu[0]: show_grading_rules,
        rules_menu[1]: show_exam_rules,
        rules_menu[2]: show_general_rules,
        rules_menu[3]: show_main_menu,
        t('download_pdf', context): download_pdf,
    }
    handler = handlers.get(text, show_rules_main)
    await handler(update, context)