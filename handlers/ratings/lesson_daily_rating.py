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
    get_code_by_text,
    get_all_directions,
    get_courses
)
from database import save_lesson_rating


# Lesson daily rating savollari - ENDI BAZADAN OLINADI
def get_questions(context):
    """Savollarni bazadan olish"""
    try:
        from database_models import get_rating_questions
        questions = get_rating_questions()
        result = []
        for question_number, translation_key, answer_type in questions:
            result.append({
                'text': get_text(translation_key, context),
                'type': answer_type,
                'number': question_number
            })
        return result
    except Exception:
        # Fallback - eski usul
        return [
            {'text': get_text('rating_q1', context), 'type': 'scale', 'number': 1},
            {'text': get_text('rating_q2', context), 'type': 'scale', 'number': 2},
            {'text': get_text('rating_q3', context), 'type': 'scale', 'number': 3},
            {'text': get_text('rating_q4', context), 'type': 'scale', 'number': 4},
            {'text': get_text('rating_q5', context), 'type': 'scale', 'number': 5},
            {'text': get_text('rating_q6', context), 'type': 'yes_no', 'number': 6},
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
        f"{questions[0]['text']}\n\n{get_text('rating_score_query', context) if questions[0]['type'] == 'scale' else get_text('rating_yes_no_query', context)}",
        reply_markup=get_rating_keyboard(context) if questions[0]['type'] == 'scale' else get_yes_no_keyboard(context)
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data['question_index']
    rating_text = update.message.text

    questions = get_questions(context)
    current_question = questions[i] if i < len(questions) else None

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
            prev_q = questions[idx]
            query_text = get_text('rating_score_query', context) if prev_q['type'] == 'scale' else get_text('rating_yes_no_query', context)
            keyboard = get_rating_keyboard(context) if prev_q['type'] == 'scale' else get_yes_no_keyboard(context)
            await update.message.reply_text(
                f"{prev_q['text']}\n\n{query_text}",
                reply_markup=keyboard
            )
            return

    # --- Savol turi tekshiruvi ---
    if current_question['type'] == 'yes_no':
        yes_text = get_text('btn_yes', context)
        no_text = get_text('btn_no', context)
        
        if rating_text not in [yes_text, no_text]:
            return await update.message.reply_text(
                f"⚠️ {get_text('error_yes_no', context)}",
                reply_markup=get_yes_no_keyboard(context)
            )

        # Javobni saqlaymiz
        save_lesson_rating({
            'direction': context.user_data.get('direction', ''),
            'course': context.user_data.get('course', ''),
            'subject_name': context.user_data.get('subject_name', ''),
            'teacher_name': context.user_data.get('teacher_name', ''),
            'question_number': current_question['number'],
            'question': current_question['text'],
            'rating': rating_text
        })
    else:
        # Scale turi - 1-5 ball
        if rating_text not in ["1", "2", "3", "4", "5"]:
            return await update.message.reply_text(get_text('error_select_number', context))

        rating = int(rating_text)

        save_lesson_rating({
            'direction': context.user_data['direction'],
            'course': context.user_data['course'],
            'subject_name': context.user_data['subject_name'],
            'teacher_name': context.user_data['teacher_name'],
            'question_number': current_question['number'],
            'question': current_question['text'],
            'rating': rating
        })

    # Keyingi savolga o'tish
    context.user_data['question_index'] += 1
    next_idx = context.user_data['question_index']

    # Agar savollar tugasa
    if next_idx >= len(questions):
        await update.message.reply_text(
            get_text('rating_thanks', context),
            reply_markup=get_main_menu_keyboard(context)
        )
        keys_to_remove = ['state', 'direction', 'course', 'subject_name', 'teacher_name', 'question_index']
        for key in keys_to_remove:
            context.user_data.pop(key, None)
        return

    # Keyingi savol
    next_q = questions[next_idx]
    query_text = get_text('rating_score_query', context) if next_q['type'] == 'scale' else get_text('rating_yes_no_query', context)
    keyboard = get_rating_keyboard(context) if next_q['type'] == 'scale' else get_yes_no_keyboard(context)
    
    await update.message.reply_text(
        f"{next_q['text']}\n\n{query_text}",
        reply_markup=keyboard
    )
