from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards import (
    get_directions_keyboard,
    get_courses_keyboard,
    get_back_keyboard,
    get_main_menu_keyboard,
    get_yes_no_keyboard
)
from utils.utils import (
    get_direction_code,
    get_course_code,
)
from database import save_lesson_rating
from config.config import DIRECTIONS, COURSES

# Lesson daily rating savollari
questions = [
    "1) Dars o'tish sifati qanday?",
    "2) O'qituvchining tushuntirishi qanchalik aniq?",
    "3) Savollarga javob berish darajasi?",
    "4) Darsning qiziqarliligi qanday?",
    "5) O'qtuvching talabalar bilan muomala madaniyati qanday?",
    "6) Bugungi darsdan yangi bilib oldingizmi?"
]

def get_rating_keyboard():
    from telegram import ReplyKeyboardMarkup
    return ReplyKeyboardMarkup([["1", "2", "3", "4", "5"]], resize_keyboard=True)


async def start_lesson_daily_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data['state'] = 'rating_direction'

    await update.message.reply_text(
        "🎯 Yo'nalishingizni tanlang:",
        reply_markup=get_directions_keyboard()
    )


async def handle_lesson_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    direction_name = update.message.text

    if direction_name in DIRECTIONS:
        context.user_data['direction'] = get_direction_code(direction_name)
        context.user_data['state'] = 'rating_course'

        await update.message.reply_text(
            f"✅ Yo'nalish: {direction_name}\n\n📚 Kursni tanlang:",
            reply_markup=get_courses_keyboard()
        )


async def handle_lesson_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    course_name = update.message.text

    if course_name in COURSES:
        context.user_data['course'] = get_course_code(course_name)
        context.user_data['state'] = 'rating_subject'

        await update.message.reply_text(
            "📖 Fan nomini kiriting:",
            reply_markup=get_back_keyboard()
        )


async def handle_subject_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subject_name = update.message.text

    if subject_name == "🔙 Orqaga":
        context.user_data['state'] = 'rating_course'
        return await update.message.reply_text(
            "📚 Kursni tanlang:",
            reply_markup=get_courses_keyboard()
        )

    context.user_data['subject_name'] = subject_name
    context.user_data['state'] = 'rating_teacher'

    await update.message.reply_text(
        "👨‍🏫 O'qituvchi ismini kiriting:",
        reply_markup=get_back_keyboard()
    )


async def handle_teacher_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teacher_name = update.message.text

    if teacher_name == "🔙 Orqaga":
        context.user_data['state'] = 'rating_subject'
        return await update.message.reply_text(
            "📖 Fan nomini kiriting:",
            reply_markup=get_back_keyboard()
        )

    context.user_data['teacher_name'] = teacher_name
    context.user_data['question_index'] = 0
    context.user_data['state'] = 'rating_process'

    await update.message.reply_text(
        f"{questions[0]}\n\nNechi ball bilan baholaysiz?",
        reply_markup=get_rating_keyboard()
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data['question_index']
    rating_text = update.message.text

    # --- 6-savol uchun alohida tekshiruv ---
    if i == 5:  # 6-savol
        if rating_text not in ["Ha", "Yo'q"]:
            return await update.message.reply_text("Iltimos 'Ha' yoki 'Yo'q' ni tanlang!")

        save_lesson_rating({
            'direction': context.user_data['direction'],
            'course': context.user_data['course'],
            'subject_name': context.user_data['subject_name'],
            'teacher_name': context.user_data['teacher_name'],
            'question_number': 6,
            'question': questions[5],
            'rating': rating_text  # Ha / Yo'q sifatida saqlanadi
        })

        # Tugadi
        await update.message.reply_text(
            "✅ Rahmat! Sizning baholashingiz qabul qilindi!",
            reply_markup=get_main_menu_keyboard()
        )
        return context.user_data.clear()

    # --- 1–5 savollar uchun (1–5 ball) ---
    if rating_text not in ["1", "2", "3", "4", "5"]:
        return await update.message.reply_text("Iltimos 1 dan 5 gacha sonni tanlang!")

    rating = int(rating_text)

    save_lesson_rating({
        'direction': context.user_data['direction'],
        'course': context.user_data['course'],
        'subject_name': context.user_data['subject_name'],
        'teacher_name': context.user_data['teacher_name'],
        'question_number': i + 1,
        'question': questions[i],
        'rating': rating
    })

    # Keyingi savolga o'tish
    context.user_data['question_index'] += 1

    # Agar keyingi savol 6-savol bo'lsa → Ha/Yo'q klaviaturasini yuboramiz
    if context.user_data['question_index'] == 5:
        return await update.message.reply_text(
            f"{questions[5]}\n\nJavobingiz:",
            reply_markup=get_yes_no_keyboard()
        )
    else:
        # Oddiy navbatdagi savol
        await update.message.reply_text(
            f"{questions[i+1]}\n\nNechi ball bilan baholaysiz?",
            reply_markup=get_rating_keyboard()
        )
