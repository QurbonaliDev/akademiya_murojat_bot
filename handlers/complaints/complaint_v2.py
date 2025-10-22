# handlers/complaint.py
# Murojaat bilan bog'liq handlerlar (ko‘p tilli versiya)

from telegram import Update
from telegram.ext import ContextTypes
from keyboards_all_lang import (
    get_directions_keyboard,
    get_courses_keyboard,
    get_complaint_types_keyboard,
    get_back_keyboard,
    get_main_menu_keyboard
)
from utils import (
    get_direction_code,
    get_course_code,
    get_complaint_type_code,
    get_direction_name,
    get_course_name,
    get_complaint_type_name
)
from database import save_complaint
from config import DIRECTIONS, COURSES, COMPLAINT_TYPES
from utils import t, lang
from texts import TEXTS


async def start_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshlash"""
    context.user_data.clear()
    context.user_data['state'] = 'choosing_direction'

    await update.message.reply_text(
        t('complaint_choose_direction', context),
        reply_markup=get_directions_keyboard(lang(context))
    )


# async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Yo'nalish tanlanganida"""
#     direction_name = update.message.text
#
#     if direction_name in DIRECTIONS:
#         context.user_data['direction'] = get_direction_code(direction_name)
#         context.user_data['state'] = 'choosing_course'
#
#         await update.message.reply_text(
#             t('complaint_choose_course', context),
#             reply_markup=get_courses_keyboard(lang(context))
#         )
#
#
# async def handle_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Kurs tanlanganida"""
#     course_name = update.message.text
#
#     if course_name in COURSES:
#         context.user_data['course'] = get_course_code(course_name)
#         context.user_data['state'] = 'choosing_complaint_type'
#
#         await update.message.reply_text(
#             t('complaint_choose_type', context),
#             reply_markup=get_complaint_types_keyboard(lang(context))
#         )
#
#
# async def handle_complaint_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Murojaat turi tanlanganida"""
#     complaint_type_name = update.message.text
#
#     if complaint_type_name in COMPLAINT_TYPES:
#         complaint_type_code = get_complaint_type_code(complaint_type_name)
#         context.user_data['complaint_type'] = complaint_type_code
#
#         if complaint_type_code == 'teacher':
#             context.user_data['state'] = 'entering_subject'
#             await update.message.reply_text(
#                 t('complaint_enter_subject', context),
#                 reply_markup=get_back_keyboard(lang(context))
#             )
#         else:
#             context.user_data['state'] = 'entering_message'
#             await ask_complaint_message(update, context)

async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish tanlanganida"""
    direction_name = update.message.text
    current_lang = lang(context)

    if direction_name in TEXTS['directions'][current_lang]:
        context.user_data['direction'] = get_direction_code(direction_name)
        context.user_data['state'] = 'choosing_course'

        await update.message.reply_text(
            TEXTS['complaint_choose_course'][current_lang],
            reply_markup=get_courses_keyboard(current_lang)
        )


async def handle_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs tanlanganida"""
    course_name = update.message.text
    current_lang = lang(context)

    if course_name in TEXTS['courses'][current_lang]:
        context.user_data['course'] = get_course_code(course_name)
        context.user_data['state'] = 'choosing_complaint_type'

        await update.message.reply_text(
            TEXTS['complaint_choose_type'][current_lang],
            reply_markup=get_complaint_types_keyboard(current_lang)
        )


async def handle_complaint_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat turi tanlanganida"""
    complaint_type_name = update.message.text
    current_lang = lang(context)

    if complaint_type_name in TEXTS['complaint_types'][current_lang]:
        complaint_type_code = get_complaint_type_code(complaint_type_name)
        context.user_data['complaint_type'] = complaint_type_code

        if complaint_type_code == 'teacher':
            context.user_data['state'] = 'entering_subject'
            await update.message.reply_text(
                TEXTS['complaint_enter_subject'][current_lang],
                reply_markup=get_back_keyboard(current_lang)
            )
        else:
            context.user_data['state'] = 'entering_message'
            await ask_complaint_message(update, context)



async def handle_subject_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fan nomi kiritilganida"""
    subject_name = update.message.text
    context.user_data['subject_name'] = subject_name
    context.user_data['state'] = 'entering_teacher'

    await update.message.reply_text(
        t('complaint_enter_teacher', context),
        reply_markup=get_back_keyboard(lang(context))
    )


async def handle_teacher_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi ismi kiritilganida"""
    teacher_name = update.message.text
    context.user_data['teacher_name'] = teacher_name
    context.user_data['state'] = 'entering_message'

    await ask_complaint_message(update, context)


async def ask_complaint_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat xabarini so'rash"""
    direction_name = get_direction_name(context.user_data['direction'])
    course_name = get_course_name(context.user_data['course'])
    complaint_type_name = get_complaint_type_name(context.user_data['complaint_type'])

    text = t('complaint_info_intro', context).format(
        complaint_type=complaint_type_name
    )

    if context.user_data['complaint_type'] == 'teacher':
        text += t('complaint_teacher_info', context).format(
            subject=context.user_data.get('subject_name', ''),
            teacher=context.user_data.get('teacher_name', '')
        )

    await update.message.reply_text(text, reply_markup=get_back_keyboard(lang(context)))


async def handle_complaint_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat xabari kiritilganida"""
    message_text = update.message.text

    complaint_data = {
        'direction': context.user_data['direction'],
        'course': context.user_data['course'],
        'complaint_type': context.user_data['complaint_type'],
        'message': message_text
    }

    if context.user_data['complaint_type'] == 'teacher':
        complaint_data['subject_name'] = context.user_data.get('subject_name', '')
        complaint_data['teacher_name'] = context.user_data.get('teacher_name', '')

    save_complaint(complaint_data)

    confirmation_text = t('complaint_confirmation', context).format(
        complaint_type=get_complaint_type_name(context.user_data['complaint_type']),
        subject=context.user_data.get('subject_name', ''),
        teacher=context.user_data.get('teacher_name', '')
    )

    await update.message.reply_text(
        confirmation_text,
        reply_markup=get_main_menu_keyboard(lang(context))
    )

    context.user_data.clear()
