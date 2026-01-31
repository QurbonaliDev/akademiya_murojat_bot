# handlers/rules.py
# Tartib qoidalar bilan bog'liq handlerlar

import os
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards import get_rules_keyboard, get_rules_detail_keyboard
from config.config import PDF_FILES
from utils.utils import get_text


async def show_rules_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tartib qoidalar asosiy menyusi"""
    context.user_data['state'] = 'rules_main'

    await update.message.reply_text(
        get_text('rules_main', context),
        reply_markup=get_rules_keyboard(context)
    )


async def show_grading_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Baholash jarayoni"""
    context.user_data['state'] = 'rules_grading'
    context.user_data['current_pdf'] = 'grading'

    text = get_text('rules_grading_text', context)

    await update.message.reply_text(
        text,
        reply_markup=get_rules_detail_keyboard(context)
    )


async def show_exam_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Imtihon jarayoni"""
    context.user_data['state'] = 'rules_exam'
    context.user_data['current_pdf'] = 'exam'

    text = get_text('rules_exam_text', context)

    await update.message.reply_text(
        text,
        reply_markup=get_rules_detail_keyboard(context)
    )


async def show_general_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Umumiy tartib qoidalar"""
    context.user_data['state'] = 'rules_general'
    context.user_data['current_pdf'] = 'rules'

    text = get_text('rules_general_text', context)

    await update.message.reply_text(
        text,
        reply_markup=get_rules_detail_keyboard(context)
    )


async def download_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PDF faylni yuklash"""
    pdf_type = context.user_data.get('current_pdf')

    if not pdf_type:
        await update.message.reply_text(get_text('error_no_rules_type', context))
        return

    pdf_path = PDF_FILES.get(pdf_type, 'document.pdf')

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=os.path.basename(pdf_path),
                caption=get_text('btn_download_pdf', context)
            )
    else:
        await update.message.reply_text(get_text('error_pdf_not_found', context))