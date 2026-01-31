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
    get_text,
    get_code_by_text
)
from database import save_lesson_rating
from config.config import ALL_DIRECTIONS, COURSES

# Lesson daily rating savollari
# Lesson daily rating savollari - ENDI LOCALES dan olinadi
def get_questions(context):
    return [
        get_text('rating_q1', context),
        get_text('rating_q2', context),
        get_text('rating_q3', context),
        get_text('rating_q4', context),
        get_text('rating_q5', context),
        get_text('rating_q6', context)
    ]

def get_rating_keyboard(context):
    from telegram import ReplyKeyboardMarkup, KeyboardButton
    keyboard = [
        ["1", "2", "3", "4", "5"],
        [get_text('btn_back', context)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start_lesson_daily_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data.clear() # TILNI SAQLASH UCHUN
    context.user_data['state'] = 'rating_direction'

    await update.message.reply_text(
        get_text('rating_intro', context) + "\n\n" + get_text('choose_direction', context),
        reply_markup=get_directions_keyboard(context)
    )


async def handle_lesson_direction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    direction_text = update.message.text
    
    # 🔙 Orqaga tugmasi
    if direction_text == get_text('btn_back', context):
        from main import start
        return await start(update, context)

    # ALL_DIRECTIONS dan topamiz
    from config.config import ALL_DIRECTIONS
    direction_code = get_code_by_text(direction_text, ALL_DIRECTIONS, context)

    if direction_code:
        context.user_data['direction'] = direction_code
        context.user_data['state'] = 'rating_course'

        await update.message.reply_text(
            f"✅ {direction_text}\n\n{get_text('choose_course', context)}",
            reply_markup=get_courses_keyboard(context)
        )
    else:
        await update.message.reply_text(
            f"⚠️ {get_text('choose_direction', context)}",
            reply_markup=get_directions_keyboard(context)
        )


async def handle_lesson_course_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    course_text = update.message.text

    # 🔙 Orqaga tugmasi
    if course_text == get_text('btn_back', context):
        context.user_data['state'] = 'rating_direction'
        return await update.message.reply_text(
            get_text('choose_direction', context),
            reply_markup=get_directions_keyboard(context)
        )

    course_code = get_code_by_text(course_text, COURSES, context)

    if course_code:
        context.user_data['course'] = course_code
        context.user_data['state'] = 'rating_subject'

        await update.message.reply_text(
            get_text('enter_subject', context),
            reply_markup=get_back_keyboard(context)
        )
    else:
        await update.message.reply_text(
            f"⚠️ {get_text('choose_course', context)}",
            reply_markup=get_courses_keyboard(context)
        )


async def handle_subject_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subject_name = update.message.text

    if subject_name == get_text('btn_back', context):
        context.user_data['state'] = 'rating_course'
        return await update.message.reply_text(
            get_text('choose_course', context),
            reply_markup=get_courses_keyboard(context)
        )

    context.user_data['subject_name'] = subject_name
    context.user_data['state'] = 'rating_teacher'

    await update.message.reply_text(
        get_text('enter_teacher', context),
        reply_markup=get_back_keyboard(context)
    )


async def handle_teacher_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teacher_name = update.message.text

    if teacher_name == get_text('btn_back', context) or teacher_name == "🔙 Orqaga":
        context.user_data['state'] = 'rating_subject'
        return await update.message.reply_text(
            get_text('enter_subject', context),
            reply_markup=get_back_keyboard(context)
        )

    context.user_data['teacher_name'] = teacher_name
    context.user_data['question_index'] = 0
    context.user_data['state'] = 'rating_process'

    questions = get_questions(context)
    await update.message.reply_text(
        f"{questions[0]}\n\n{get_text('rating_score_query', context)}",
        reply_markup=get_rating_keyboard(context)
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data['question_index']
    rating_text = update.message.text

    # --- 6-savol uchun alohida tekshiruv ---
    questions = get_questions(context)

    # --- Orqaga qaytish ---
    if rating_text == get_text('btn_back', context):
        if i == 0:
            context.user_data['state'] = 'rating_teacher'
            return await update.message.reply_text(
                get_text('enter_teacher', context),
                reply_markup=get_back_keyboard(context)
            )
        else:
            context.user_data['question_index'] -= 1
            idx = context.user_data['question_index']
            await update.message.reply_text(
                f"{questions[idx]}\n\n{get_text('rating_score_query', context)}",
                reply_markup=get_rating_keyboard(context)
            )
            return

    # --- 6-savol uchun alohida tekshiruv (Ha/Yo'q) ---
    if i == 5:  # 6-savol
        yes_text = get_text('btn_yes', context)
        no_text = get_text('btn_no', context)
        
        if rating_text not in [yes_text, no_text]:
            return await update.message.reply_text(
                f"⚠️ {get_text('error_yes_no', context)}",
                reply_markup=get_yes_no_keyboard(context)
            )

        # Tozalangan javobni saqlaymiz
        save_lesson_rating({
            'direction': context.user_data.get('direction', ''),
            'course': context.user_data.get('course', ''),
            'subject_name': context.user_data.get('subject_name', ''),
            'teacher_name': context.user_data.get('teacher_name', ''),
            'question_number': 6,
            'question': questions[5],
            'rating': rating_text  # Ha / Yo'q sifatida saqlanadi
        })

        # Tugadi
        await update.message.reply_text(
            get_text('rating_thanks', context),
            reply_markup=get_main_menu_keyboard(context)
        )
        # context.user_data.clear() # TILNI SAQLASH
        keys_to_remove = ['state', 'direction', 'course', 'subject_name', 'teacher_name', 'question_index']
        for key in keys_to_remove:
            context.user_data.pop(key, None)
        return

    # --- 1–5 savollar uchun (1–5 ball) ---
    if rating_text not in ["1", "2", "3", "4", "5"]:
        return await update.message.reply_text(get_text('error_select_number', context))

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
            f"{questions[5]}\n\n{get_text('rating_yes_no_query', context)}",
            reply_markup=get_yes_no_keyboard(context)
        )
    else:
        # Oddiy navbatdagi savol
        await update.message.reply_text(
            f"{questions[i+1]}\n\n{get_text('rating_score_query', context)}",
            reply_markup=get_rating_keyboard(context)
        )
