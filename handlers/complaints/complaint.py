# handlers/complaint.py
# Murojaat bilan bog'liq handlerlar

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import (
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


async def start_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshlash"""
    context.user_data.clear()
    context.user_data['state'] = 'choosing_direction'

    await update.message.reply_text(
        "🎯 Yo'nalishingizni tanlang:",
        reply_markup=get_directions_keyboard()
    )


async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish tanlanganida"""
    direction_name = update.message.text

    if direction_name in DIRECTIONS:
        context.user_data['direction'] = get_direction_code(direction_name)
        context.user_data['state'] = 'choosing_course'

        await update.message.reply_text(
            f"✅ Yo'nalish: {direction_name}\n\n📚 Kursni tanlang:",
            reply_markup=get_courses_keyboard()
        )


async def handle_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs tanlanganida"""
    course_name = update.message.text

    if course_name in COURSES:
        context.user_data['course'] = get_course_code(course_name)
        context.user_data['state'] = 'choosing_complaint_type'

        direction_name = get_direction_name(context.user_data['direction'])

        await update.message.reply_text(
            f"\n\n📝 Murojaat turini tanlang:",
            reply_markup=get_complaint_types_keyboard()
        )


async def handle_complaint_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat turi tanlanganida"""
    complaint_type_name = update.message.text

    if complaint_type_name in COMPLAINT_TYPES:
        complaint_type_code = get_complaint_type_code(complaint_type_name)
        context.user_data['complaint_type'] = complaint_type_code

        if complaint_type_code == 'teacher':
            context.user_data['state'] = 'entering_subject'
            await update.message.reply_text(
                "📚 Qaysi fan haqida murojaat qilmoqchisiz?\n\nFan nomini kiriting:",
                reply_markup=get_back_keyboard()
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
        f"📚 Fan: {subject_name}\n\n👨‍🏫 O'qituvchining ismini kiriting:",
        reply_markup=get_back_keyboard()
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

    text = (
        f"📝 Murojaat ma'lumotlari:\n\n"
        f"📋 Turi: {complaint_type_name}\n"
    )

    if context.user_data['complaint_type'] == 'teacher':
        text += f"📖 Fan: {context.user_data.get('subject_name', '')}\n"
        text += f"👨‍🏫 O'qituvchi: {context.user_data.get('teacher_name', '')}\n"

    text += (
        f"\n🔒 **DIQQAT: Bu tizim butunlay anonim!**\n"
        "Sizning shaxsingiz hech qanday shaklda saqlanmaydi.\n\n"
        "✍️ Endi o'z murojaatingizni yozing va yuboring:"
    )

    await update.message.reply_text(text, reply_markup=get_back_keyboard())


async def handle_complaint_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat xabari kiritilganida"""
    message_text = update.message.text

    # Ma'lumotlarni to'plash
    complaint_data = {
        'direction': context.user_data['direction'],
        'course': context.user_data['course'],
        'complaint_type': context.user_data['complaint_type'],
        'message': message_text
    }

    if context.user_data['complaint_type'] == 'teacher':
        complaint_data['subject_name'] = context.user_data.get('subject_name', '')
        complaint_data['teacher_name'] = context.user_data.get('teacher_name', '')

    # Bazaga saqlash
    save_complaint(complaint_data)

    # Tasdiqlash xabari
    direction_name = get_direction_name(context.user_data['direction'])
    course_name = get_course_name(context.user_data['course'])
    complaint_type_name = get_complaint_type_name(context.user_data['complaint_type'])

    confirmation_text = (
        f"✅ Murojaatingiz qabul qilindi!\n\n"
        f"📊 Ma'lumotlar:\n"
        f"📋 Turi: {complaint_type_name}\n"
    )

    if context.user_data['complaint_type'] == 'teacher':
        confirmation_text += f"📖 Fan: {context.user_data.get('subject_name', '')}\n"
        confirmation_text += f"👨‍🏫 O'qituvchi: {context.user_data.get('teacher_name', '')}\n"

    confirmation_text += (
        f"\n🙏 Rahmat! Sizning fikringiz biz uchun muhim.\n"
        f"🔒 Murojaatingiz butunlay anonim shaklda saqlandi.\n\n"
        f"Yana murojaat qoldirmoqchi bo'lsangiz, '📝 Murojaat' tugmasini bosing."
    )

    await update.message.reply_text(
        confirmation_text,
        reply_markup=get_main_menu_keyboard()
    )

    # Contextni tozalash
    context.user_data.clear()