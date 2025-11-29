from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards_all_lang_v2 import (
    get_complaint_direction_keyboard, get_complaint_course_keyboard,
    get_complaint_type_keyboard, get_back_keyboard, get_main_menu_keyboard
)
from utils.utils_v2 import (
    get_direction_name, get_course_name, get_complaint_type_name, t, lang
)
from database import save_complaint
from text.texts_v2 import TEXTS
import logging

logger = logging.getLogger(__name__)

async def start_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshlash"""
    # Faqat murojaat bilan bog'liq ma'lumotlarni tozalash
    context.user_data['complaint'] = {}
    context.user_data['state'] = 'choosing_direction'
    logger.debug("Starting complaint process, state=choosing_direction")
    await update.message.reply_text(
        t('complaint_direction', context),
        reply_markup=get_complaint_direction_keyboard(context)
    )

async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish tanlashni boshqarish"""
    text = update.message.text
    current_lang = lang(context)
    directions = TEXTS['directions'][current_lang]
    logger.debug(f"Direction choice: text={text}, state={context.user_data.get('state')}")
    if text == t('back', context):
        from menu import show_main_menu
        await show_main_menu(update, context)
        return
    if text in directions:
        context.user_data['complaint']['direction'] = get_direction_name(text, current_lang)
        context.user_data['state'] = 'choosing_course'
        await update.message.reply_text(
            t('complaint_course', context),
            reply_markup=get_complaint_course_keyboard(context)
        )
    else:
        await update.message.reply_text(
            t('complaint_direction', context),
            reply_markup=get_complaint_direction_keyboard(context)
        )

async def handle_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs tanlashni boshqarish"""
    text = update.message.text
    current_lang = lang(context)
    courses = TEXTS['courses'][current_lang]
    logger.debug(f"Course choice: text={text}, state={context.user_data.get('state')}")
    if text == t('back', context):
        await start_complaint(update, context)
        return
    if text in courses:
        context.user_data['complaint']['course'] = get_course_name(text, current_lang)
        context.user_data['state'] = 'choosing_complaint_type'
        await update.message.reply_text(
            t('complaint_type', context),
            reply_markup=get_complaint_type_keyboard(context)
        )
    else:
        await update.message.reply_text(
            t('complaint_course', context),
            reply_markup=get_complaint_course_keyboard(context)
        )

async def handle_complaint_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat turi tanlashni boshqarish"""
    text = update.message.text
    current_lang = lang(context)
    complaint_types = TEXTS['complaint_types'][current_lang]
    logger.debug(f"Complaint type choice: text={text}, state={context.user_data.get('state')}")
    if text == t('back', context):
        await handle_course_choice(update, context)
        return
    if text in complaint_types:
        complaint_type = get_complaint_type_name(text, current_lang)
        context.user_data['complaint']['complaint_type'] = complaint_type
        context.user_data['state'] = 'entering_subject' if complaint_type == 'O‘qituvchi' else 'entering_message'
        await update.message.reply_text(
            t('complaint_subject' if complaint_type == 'O‘qituvchi' else 'complaint_message', context,
              complaint_type=complaint_type),
            reply_markup=get_back_keyboard(context)
        )
    else:
        await update.message.reply_text(
            t('complaint_type', context),
            reply_markup=get_complaint_type_keyboard(context)
        )

async def handle_subject_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fan nomini kiritishni boshqarish"""
    text = update.message.text
    logger.debug(f"Subject entry: text={text}, state={context.user_data.get('state')}")
    if text == t('back', context):
        await handle_complaint_type_choice(update, context)
        return
    context.user_data['complaint']['subject_name'] = text
    context.user_data['state'] = 'entering_teacher'
    await update.message.reply_text(
        t('complaint_teacher', context),
        reply_markup=get_back_keyboard(context)
    )

async def handle_teacher_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi nomini kiritishni boshqarish"""
    text = update.message.text
    logger.debug(f"Teacher entry: text={text}, state={context.user_data.get('state')}")
    if text == t('back', context):
        await handle_complaint_type_choice(update, context)
        return
    context.user_data['complaint']['teacher_name'] = text
    context.user_data['state'] = 'entering_message'
    await update.message.reply_text(
        t('complaint_message', context,
          complaint_type=context.user_data['complaint']['complaint_type'],
          subject=context.user_data['complaint'].get('subject_name', ''),
          teacher=context.user_data['complaint'].get('teacher_name', '')),
        reply_markup=get_back_keyboard(context)
    )

async def handle_complaint_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat xabarini boshqarish"""
    text = update.message.text
    logger.debug(f"Complaint message: text={text}, state={context.user_data.get('state')}")
    if text == t('back', context):
        await handle_complaint_type_choice(update, context)
        return
    complaint_data = {
        'direction': context.user_data['complaint'].get('direction'),
        'course': context.user_data['complaint'].get('course'),
        'complaint_type': context.user_data['complaint'].get('complaint_type'),
        'message': text
    }
    if context.user_data['complaint']['complaint_type'] == 'O‘qituvchi':
        complaint_data['subject_name'] = context.user_data['complaint'].get('subject_name', '')
        complaint_data['teacher_name'] = context.user_data['complaint'].get('teacher_name', '')
    save_complaint(complaint_data)
    await update.message.reply_text(
        t('complaint_saved', context,
          complaint_type=context.user_data['complaint']['complaint_type'],
          subject=context.user_data['complaint'].get('subject_name', ''),
          teacher=context.user_data['complaint'].get('teacher_name', '')),
        reply_markup=get_main_menu_keyboard(context)
    )
    context.user_data['state'] = 'main_menu'
    context.user_data['complaint'] = {}