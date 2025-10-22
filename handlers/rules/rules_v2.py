# handlers/rules.py
# Tartib qoidalar bilan bog'liq handlerlar (ko‘p tilli versiya)

import os
from telegram import Update
from telegram.ext import ContextTypes
# from keyboards import get_rules_keyboard, get_rules_detail_keyboard
from keyboards_all_lang import get_rules_keyboard, get_rules_detail_keyboard
from config import PDF_FILES
from utils import t, lang


async def show_rules_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tartib qoidalar asosiy menyusi"""
    context.user_data['state'] = 'rules_main'

    await update.message.reply_text(
        t('rules_main_intro', context),
        reply_markup=get_rules_keyboard(lang(context))
    )


async def show_grading_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Baholash jarayoni"""
    context.user_data['state'] = 'rules_grading'
    context.user_data['current_pdf'] = 'grading'

    await update.message.reply_text(
        t('grading_rules_text', context),
        reply_markup=get_rules_detail_keyboard(lang(context))
    )


async def show_exam_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Imtihon jarayoni"""
    context.user_data['state'] = 'rules_exam'
    context.user_data['current_pdf'] = 'exam'

    await update.message.reply_text(
        t('exam_rules_text', context),
        reply_markup=get_rules_detail_keyboard(lang(context))
    )


async def show_general_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Umumiy tartib qoidalar"""
    context.user_data['state'] = 'rules_general'
    context.user_data['current_pdf'] = 'rules'

    await update.message.reply_text(
        t('general_rules_text', context),
        reply_markup=get_rules_detail_keyboard(lang(context))
    )


async def download_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PDF faylni yuklash"""
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
                caption=t('rules_pdf_caption', context).format(pdf_name=pdf_name)
            )
    else:
        await update.message.reply_text(t('rules_pdf_not_found', context))
