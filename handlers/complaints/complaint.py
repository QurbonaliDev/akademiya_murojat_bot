# handlers/complaint.py
# Murojaat bilan bog'liq handlerlar

from telegram import Update
from telegram.ext import ContextTypes

from config.config import COURSES, COMPLAINT_TYPES, DIRECTIONS_IIXM, DIRECTIONS_MSHF, \
    DIRECTIONS_ISLOMSHUNOSLIK, EDUCATION_TYPE, EDUCATION_LANG
from database import save_complaint
from keyboards.keyboards import (
    get_courses_keyboard,
    get_complaint_types_keyboard,
    get_back_keyboard,
    get_main_menu_keyboard, get_faculties_keyboard, get_dynamic_keyboard, get_education_type_keyboard,
    get_education_lang_keyboard
)
from utils.utils import (
    get_course_code,
    get_complaint_type_code,
    get_direction_name,
    get_course_name,
    get_complaint_type_name, get_faculty_code, get_faculty_name
)


async def start_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data['state'] = 'choosing_faculty'

    await update.message.reply_text(
        "🏛 Fakultetingizni tanlang:",
        reply_markup=get_faculties_keyboard()
    )


# ============================
# Fakultet tanlash
# ============================
async def handle_faculty_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faculty_name = update.message.text

    if faculty_name not in ['IIXM', 'MSHF', 'Islomshunoslik', 'Magistratura']:
        return

    faculty_code = get_faculty_code(faculty_name)
    context.user_data['faculty'] = faculty_code
    context.user_data['state'] = 'choosing_direction'

    # Shu fakultetga tegishli yo'nalishlar
    directions = get_directions_by_faculty(faculty_code)
    context.user_data['directions_map'] = directions

    await update.message.reply_text(
        f"🏛 Fakultet: {faculty_name}\n\n🎯 Yo'nalishingizni tanlang:",
        reply_markup=get_dynamic_keyboard(directions)
    )


# ============================
# Yo'nalish tanlash
# ============================
async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    direction_name = update.message.text
    directions = context.user_data.get('directions_map', {})

    if direction_name not in directions:
        return

    # Tanlangan yo'nalishni saqlaymiz
    context.user_data['direction'] = directions[direction_name]
    context.user_data['state'] = 'choosing_education_type'

    await update.message.reply_text(
        f"📘 Yo'nalish: {direction_name}\n\n🎓 Endi talim turini tanlang:",
        reply_markup=get_education_type_keyboard()  # Talim turlari tugmalari
    )

# ============================
# Talim turini tanlash
# ============================
async def handle_education_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    education_type = update.message.text
    education_types = context.user_data.get('education_type_map', EDUCATION_TYPE)

    if education_type not in education_types:
        return

    # Ta’lim turini saqlaymiz
    context.user_data['education_type'] = education_types[education_type]
    context.user_data['state'] = 'choosing_education_lang'

    await update.message.reply_text(
        f"🎓 Ta'lim turi: {education_type}\n\n🌐 Endi ta'lim tilini tanlang:",
        reply_markup=get_education_lang_keyboard()
    )

async def handle_education_lang_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_name = update.message.text
    lang_map = context.user_data.get('education_lang_map', EDUCATION_LANG)

    if lang_name not in lang_map:
        return

    context.user_data['education_language'] = lang_map[lang_name]
    context.user_data['state'] = 'choosing_course'

    await update.message.reply_text(
        f"🌐 Ta'lim tili: {lang_name}\n\n📚 Endi kursni tanlang:",
        reply_markup=get_courses_keyboard()
    )


async def handle_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    course_name = update.message.text

    if course_name in COURSES:
        context.user_data['course'] = get_course_code(course_name)
        context.user_data['state'] = 'choosing_complaint_type'

        await update.message.reply_text(
            "📝 Murojaat turini tanlang:",
            reply_markup=get_complaint_types_keyboard()
        )


# async def handle_faculty_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     faculty_name = update.message.text
#
#     if faculty_name in FACULTIES:
#         context.user_data['faculty'] = get_faculty_code(faculty_name)
#         context.user_data['state'] = 'choosing_direction'
#
#         await update.message.reply_text(
#             f"🏛 Fakultet: {faculty_name}\n\n🎯 Endi yo'nalishingizni tanlang:",
#             reply_markup=get_dynamic_keyboard()
#         )
#
# async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     direction_name = update.message.text
#
#     faculty = context.user_data.get('faculty')
#     directions = get_directions_by_faculty(faculty)
#
#     if direction_name in directions:
#         context.user_data['direction'] = directions[direction_name]
#         context.user_data['state'] = 'choosing_course'
#
#         await update.message.reply_text(
#             f"📘 Yo'nalish: {direction_name}\n\n📚 Endi kursni tanlang:",
#             reply_markup=get_courses_keyboard()
#         )


# async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     direction_name = update.message.text
#
#     if direction_name in DIRECTIONS:
#         context.user_data['direction'] = get_direction_code(direction_name)
#         context.user_data['state'] = 'choosing_course'
#
#         await update.message.reply_text(
#             f"📘 Yo'nalish: {direction_name}\n\n📚 Endi kursni tanlang:",
#             reply_markup=get_courses_keyboard()
#         )


# async def handle_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Yo'nalish tanlanganida"""
#     direction_name = update.message.text
#
#     if direction_name in DIRECTIONS:
#         context.user_data['direction'] = get_direction_code(direction_name)
#         context.user_data['state'] = 'choosing_course'
#
#         await update.message.reply_text(
#             f"✅ Yo'nalish: {direction_name}\n\n📚 Kursni tanlang:",
#             reply_markup=get_faculties_keyboard()
#         )

# async def handle_faculty_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Fakultet tanlanganida"""
#     faculty_name = update.message.text
#
#     if faculty_name in FACULTIES:
#         context.user_data['faculty'] = get_faculty_code(faculty_name)
#         context.user_data['state'] = 'choosing_complaint_type'
#
#         direction_name = get_direction_name(context.user_data['direction'])
#
#         await update.message.reply_text(
#             f"\n\n📝 Murojaat turini tanlang:",
#             reply_markup=get_courses_keyboard()
#         )

# async def handle_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
# """Kurs tanlanganida"""
# course_name = update.message.text
#
# if course_name in COURSES:
#     context.user_data['course'] = get_course_code(course_name)
#     context.user_data['state'] = 'choosing_complaint_type'
#
#     direction_name = get_direction_name(context.user_data['direction'])
#
#     await update.message.reply_text(
#         f"\n\n📝 Murojaat turini tanlang:",
#         reply_markup=get_complaint_types_keyboard()
#     )


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
    faculty_name = get_faculty_name(context.user_data['faculty'])
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
        'faculty': context.user_data['faculty'],
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
    faculty_name = get_faculty_name(context.user_data['faculty'])
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


def get_directions_by_faculty(faculty_code):
    if faculty_code == 'iixm':
        return DIRECTIONS_IIXM
    elif faculty_code == 'mshf':
        return DIRECTIONS_MSHF
    elif faculty_code == 'islomshunoslik':
        return DIRECTIONS_ISLOMSHUNOSLIK
    else:
        return {}
