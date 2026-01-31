# main.py
# Asosiy bot fayli - barcha komponentlarni birlashtiradi

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import qilish
# Import qilish
from config.config import BOT_TOKEN, LANGS
from database import init_database
from keyboards.keyboards import (
    get_main_menu_keyboard,
    get_language_keyboard,
    get_faculties_keyboard,
    get_dynamic_keyboard,
    get_education_type_keyboard,
    get_education_lang_keyboard,
    get_courses_keyboard,
    get_complaint_types_keyboard,
    get_back_keyboard
)
from utils.utils import (
    is_admin,
    get_text,
    get_main_menu_buttons,
    get_directions_by_faculty,
    get_faculty_name
)

# Handlerlarni import qilish
from handlers.complaints.complaint import (
    start_complaint,
    handle_faculty_choice,
    handle_direction_choice,
    handle_education_type_choice,
    handle_education_lang_choice,
    handle_course_choice,
    handle_complaint_type_choice,
    handle_subject_entry,
    handle_teacher_entry,
    handle_complaint_message
)

from handlers.ratings.lesson_daily_rating import (
    start_lesson_daily_rating,
    handle_lesson_direction_choice,
    handle_lesson_course_choice,
    handle_subject_name,
    handle_teacher_name,
    handle_rating
)
from handlers.rules.rules import (
    show_rules_main,
    show_grading_rules,
    show_exam_rules,
    show_general_rules,
    download_pdf
)
from handlers.surveys.survey import (
    show_survey_main,
    show_teachers_survey,
    show_education_survey,
    show_employers_survey,
    open_survey_link,
    show_survey_results
)
from handlers.admins.admin import (
    show_admin_panel,
    show_statistics,
    view_complaints,
    export_to_excel_handler,
    export_to_daily_lesson_excel_handler,
    show_dashboard,
    show_export_menu # <--- ADDED
)

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda"""
    # Agar til tanlanmagan bo'lsa, til tanlashga yuboramiz
    if 'language' not in context.user_data:
        await update.message.reply_text(
            "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please select a language:",
            reply_markup=get_language_keyboard()
        )
        return

    # context.user_data.clear() # Buni o'chiramiz, chunki tilni o'chirib yuboradi

    welcome_text = get_text('welcome', context)

    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(context)
    )


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Tarjimalarni tekshirish (chunki tugma matni tilga qarab o'zgaradi)
    # Eng yaxshi yo'l - har bir til uchun variantlarni tekshirish yoki callback_query ishlatish.
    # Lekin hozirgi strukturada utils.get_text orqali kalit so'zlarni solishtiramiz.
    
    # QAYD: Tugma matnini tekshirish biroz qiyinroq, chunki biz key'ni bilmaymiz.
    # Shuning uchun barcha tillardagi variantlarni tekshiramiz.
    
    # Keling, oddiyroq yo'l tutamiz: 
    # Hozircha hardcode qilingan stringlarni utils.get_text bilan almashtiramiz.
    
    if text == get_text('btn_complaint', context):
        await start_complaint(update, context)

    elif text == get_text('btn_rules', context):
        await show_rules_main(update, context)

    elif text == get_text('btn_survey', context):
        await show_survey_main(update, context)

    elif text == get_text('btn_admin', context):
        await show_admin_panel(update, context)

    elif text == get_text('btn_lesson_rating', context):
        await start_lesson_daily_rating(update, context)

    elif text == get_text('btn_lang', context):
        await update.message.reply_text(
            get_text('btn_lang', context) + ":",
            reply_markup=get_language_keyboard()
        )

    elif text == get_text('btn_back_main', context) or text == get_text('btn_back', context):
        await start(update, context)



async def handle_select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Til tanlash jarayonini boshqarish"""
    text = update.message.text
    
    # LANGS values (🇺🇿 O'zbekcha, 🇷🇺 Русский...) orqali kodni topamiz
    selected_lang_code = None
    for code, name in LANGS.items():
        if text == name:
            selected_lang_code = code
            break
            
    if selected_lang_code:
        context.user_data['language'] = selected_lang_code
        # Tanlangandan keyin holatni tozalaymiz va asosiy menyuga o'tamiz
        context.user_data['state'] = ''
        await start(update, context)
    else:
        # Noto'g'ri tanlov
        await update.message.reply_text(
            "Iltimos, tugmalardan birini tanlang / Пожалуйста, выберите одну из кнопок"
        )


async def handle_complaint_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaat jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text

    # 🔙 Orqaga tugmasi (Mantiqiy zanjir)
    if text == get_text('btn_back', context):
        if state == 'choosing_faculty':
            await start(update, context)
        
        elif state == 'choosing_direction':
            await start_complaint(update, context)

        elif state == 'choosing_education_type':
            # Fakultetni aniqlaymiz va yo'nalishlar keyboardini qayta chiqaramiz
            faculty_code = context.user_data.get('faculty')
            directions = get_directions_by_faculty(faculty_code)
            context.user_data['state'] = 'choosing_direction'
            faculty_name = get_faculty_name(faculty_code, context)
            await update.message.reply_text(
                f"🏛 {faculty_name}\n\n{get_text('choose_direction', context)}",
                reply_markup=get_dynamic_keyboard(directions, context)
            )

        elif state == 'choosing_education_lang':
            context.user_data['state'] = 'choosing_education_type'
            await update.message.reply_text(
                get_text('choose_edu_type', context),
                reply_markup=get_education_type_keyboard(context)
            )

        elif state == 'choosing_course':
            faculty = context.user_data.get('faculty', '')
            if faculty == 'magistratura':
                # Magistratura - yo'nalish tanlashga qaytadi
                directions = context.user_data.get('directions_map', {})
                faculty_name = get_faculty_name(faculty, context)
                context.user_data['state'] = 'choosing_direction'
                await update.message.reply_text(
                    f"🏛 {faculty_name}\n\n{get_text('choose_direction', context)}",
                    reply_markup=get_dynamic_keyboard(directions, context)
                )
            else:
                context.user_data['state'] = 'choosing_education_lang'
                await update.message.reply_text(
                    get_text('choose_edu_lang', context),
                    reply_markup=get_education_lang_keyboard(context)
                )

        elif state == 'choosing_complaint_type':
            context.user_data['state'] = 'choosing_course'
            await update.message.reply_text(
                get_text('choose_course', context),
                reply_markup=get_courses_keyboard(context)
            )

        elif state == 'entering_subject':
            context.user_data['state'] = 'choosing_complaint_type'
            await update.message.reply_text(
                get_text('choose_complaint_type', context),
                reply_markup=get_complaint_types_keyboard(context)
            )

        elif state == 'entering_teacher':
            context.user_data['state'] = 'entering_subject'
            await update.message.reply_text(
                get_text('enter_subject', context),
                reply_markup=get_back_keyboard(context)
            )

        elif state == 'entering_message':
            complaint_type = context.user_data.get('complaint_type')
            if complaint_type == 'teacher':
                context.user_data['state'] = 'entering_teacher'
                await update.message.reply_text(
                    get_text('enter_teacher', context),
                    reply_markup=get_back_keyboard(context)
                )
            else:
                context.user_data['state'] = 'choosing_complaint_type'
                await update.message.reply_text(
                    get_text('choose_complaint_type', context),
                    reply_markup=get_complaint_types_keyboard(context)
                )
        return

    # =============================
    # 🔽 Murojaat jarayoni oqimi
    # =============================

    # 1️⃣ Fakultet tanlash
    if state == 'choosing_faculty':
        await handle_faculty_choice(update, context)
        return

    # 2️⃣ Yo‘nalish tanlash
    elif state == 'choosing_direction':
        await handle_direction_choice(update, context)
        return

    # 2️⃣ Ta'lim yo'nalishini
    elif state == 'choosing_education_type':
        await handle_education_type_choice(update, context)
        return

    # 2️⃣ Ta'lim tilini tanlash
    elif state == 'choosing_education_lang':
        await handle_education_lang_choice(update, context)
        return

    # 3️⃣ Kurs tanlash
    elif state == 'choosing_course':
        await handle_course_choice(update, context)
        return

    # 4️⃣ Murojaat turi
    elif state == 'choosing_complaint_type':
        await handle_complaint_type_choice(update, context)
        return

    # 5️⃣ Fan kiritish
    elif state == 'entering_subject':
        await handle_subject_entry(update, context)
        return

    # 6️⃣ O‘qituvchi ismi kiritish
    elif state == 'entering_teacher':
        await handle_teacher_entry(update, context)
        return

    # 7️⃣ Murojaat matnini kiritish
    elif state == 'entering_message':
        await handle_complaint_message(update, context)
        return



async def handle_rules_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tartib qoidalar jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text

    if text == get_text('btn_grading', context):
        await show_grading_rules(update, context)

    elif text == get_text('btn_exam', context):
        await show_exam_rules(update, context)

    elif text == get_text('btn_general', context):
        await show_general_rules(update, context)

    elif text == get_text('btn_download_pdf', context):
        await download_pdf(update, context)

    elif text == get_text('btn_back', context):
        if state == 'rules_main':
            await start(update, context)
        else:
            # Har qanday qoida ichidan asosiy qoidalar menyusiga qaytamiz
            await show_rules_main(update, context)


async def handle_survey_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnoma jarayonini boshqarish"""
    state = context.user_data.get('state', '')
    text = update.message.text

    if text == get_text('btn_survey_teachers', context):
        await show_teachers_survey(update, context)

    elif text == get_text('btn_survey_edu', context):
        await show_education_survey(update, context)

    elif text == get_text('btn_survey_emp', context):
        await show_employers_survey(update, context)

    elif text == get_text('btn_survey_link', context):
        await open_survey_link(update, context)

    elif text == get_text('btn_back', context):
        if state == 'survey_main':
            await start(update, context)
        else:
            await show_survey_main(update, context)


async def handle_admin_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel jarayonini boshqarish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    text = update.message.text

    if text == get_text('btn_stats', context):
        await show_statistics(update, context)

    elif text == get_text('btn_view_complaints', context):
        await view_complaints(update, context)

    elif text == get_text('btn_export_menu', context):
        await show_export_menu(update, context)

    elif text == get_text('btn_dashboard', context):
        await show_dashboard(update, context)
    
    elif text == get_text('btn_back_main', context):
        await start(update, context)


async def handle_admin_export_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel export jarayonini boshqarish"""
    text = update.message.text

    if text == get_text('btn_export_excel', context):
        await export_to_excel_handler(update, context)

    elif text == get_text('btn_export_lesson', context):
        await export_to_daily_lesson_excel_handler(update, context)

    elif text == get_text('btn_back', context):
        await show_admin_panel(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha matnli xabarlarni boshqarish"""
    text = update.message.text
    state = context.user_data.get('state', '')

    # 1. Global: Til tanlash (Har qanday holatda ishlaydi)
    if text in LANGS.values():
        await handle_select_language(update, context)
        return

    # 2. Global: Asosiy menyu tugmalari
    # Har bir tildagi variantlarni tekshirish kerak (Endi utils orqali)
    main_menu_buttons = get_main_menu_buttons()

    if text in main_menu_buttons:
        # Menyu tugmasi bosilsa, holatdan qat'iy nazar menyuga ishlov beramiz
        await handle_main_menu(update, context)
        return

    # 3. Holatga qarab boshqarish
    if not state:
        await start(update, context)
        return

    # Murojaat jarayoni
    if state in ['choosing_faculty','choosing_direction',
                 'choosing_education_type', 'choosing_education_lang', 'choosing_course', 'choosing_complaint_type',
                 'entering_subject', 'entering_teacher', 'entering_message']:
        await handle_complaint_flow(update, context)
        return

    # Tartib qoidalar
    if state in ['rules_main', 'rules_grading', 'rules_exam', 'rules_general']:
        await handle_rules_flow(update, context)
        return

    # So'rovnoma
    if state in ['survey_main', 'survey_teachers', 'survey_education', 'survey_employers']:
        await handle_survey_flow(update, context)
        return

    # Admin panel
    if state == 'admin_panel':
        await handle_admin_flow(update, context)
        return
    
    if state == 'admin_export_menu':
        await handle_admin_export_flow(update, context)
        return

    # Kunlik darsni baholash jarayoni
    if state == 'rating_direction':
        await handle_lesson_direction_choice(update, context)
        return
    if state == 'rating_course':
        await handle_lesson_course_choice(update, context)
        return
    if state == 'rating_subject':
        await handle_subject_name(update, context)
        return
    if state == 'rating_teacher':
        await handle_teacher_name(update, context)
        return
    if state == 'rating_process':
        await handle_rating(update, context)
        return

    # Default - asosiy menyuga qaytish
    await start(update, context)


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin komandasi"""
    await show_admin_panel(update, context)


def main():
    """Asosiy funksiya - botni ishga tushirish"""
    # Ma'lumotlar bazasini yaratish
    init_database()
    logger.info("Ma'lumotlar bazasi ishga tushirildi")

    # Bot applicationni yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Botni ishga tushirish
    logger.info("Bot ishga tushmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()