# keyboards.py
# ReplyKeyboard klaviaturalari - DINAMIK (bazadan o'qiydi)

from telegram import ReplyKeyboardMarkup, KeyboardButton
from utils.utils import (
    get_text, get_faculties, get_education_types, get_education_languages,
    get_complaint_types, get_courses, get_regular_courses, get_magistr_courses,
    get_active_languages, get_all_directions
)


def get_language_keyboard():
    """Til tanlash klaviaturasi (BAZADAN)"""
    languages = get_active_languages()
    keyboard = [[KeyboardButton(lang_name)] for lang_name in languages.values()]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_main_menu_keyboard(context):
    """Asosiy menyu klaviaturasi (Dinamik)"""
    keyboard = [
        [KeyboardButton(get_text('btn_complaint', context))],
        [KeyboardButton(get_text('btn_rules', context))],
        [KeyboardButton(get_text('btn_survey', context))],
        [KeyboardButton(get_text('btn_lesson_rating', context))],
        [KeyboardButton(get_text('btn_admin', context))],
        [KeyboardButton(get_text('btn_lang', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_directions_keyboard(context):
    """Yo'nalishlar klaviaturasi (BAZADAN)"""
    all_directions = get_all_directions()
    keyboard = [[KeyboardButton(get_text(val, context))] for val in all_directions.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_dynamic_keyboard(items: dict, context, prefix="dir_"):
    """Dinamik keyboard yaratish"""
    buttons = []
    for code, val in items.items():
        label = get_text(val, context)
        buttons.append([KeyboardButton(label)])
        
    buttons.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_faculties_keyboard(context):
    """Fakultetlar klaviaturasi (BAZADAN)"""
    faculties = get_faculties()
    keyboard = [[KeyboardButton(get_text(val, context))] for val in faculties.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_education_type_keyboard(context):
    """Ta'lim turi klaviaturasi (BAZADAN)"""
    edu_types = get_education_types()
    keyboard = [[KeyboardButton(get_text(val, context))] for val in edu_types.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_education_lang_keyboard(context):
    """Ta'lim tili klaviaturasi (BAZADAN)"""
    edu_langs = get_education_languages()
    keyboard = [[KeyboardButton(get_text(val, context))] for val in edu_langs.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_courses_keyboard(context):
    """Kurslar klaviaturasi - fakultetga qarab (BAZADAN)"""
    faculty = context.user_data.get('faculty', '')
    
    if faculty == 'magistratura':
        courses = get_magistr_courses()
    else:
        courses = get_regular_courses()
    
    keyboard = [[KeyboardButton(get_text(val, context))] for val in courses.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_complaint_types_keyboard(context):
    """Murojaat turlari klaviaturasi (BAZADAN)"""
    complaint_types = get_complaint_types()
    keyboard = [[KeyboardButton(get_text(val, context))] for val in complaint_types.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_keyboard(context):
    """Tartib qoidalar klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_grading', context))],
        [KeyboardButton(get_text('btn_exam', context))],
        [KeyboardButton(get_text('btn_general', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_detail_keyboard(context):
    """Qoidalar detali klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_download_pdf', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_keyboard(context):
    """So'rovnoma asosiy klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_survey_teachers', context))],
        [KeyboardButton(get_text('btn_survey_edu', context))],
        [KeyboardButton(get_text('btn_survey_emp', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_links_keyboard(context):
    """So'rovnoma havolalari klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_survey_link', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_keyboard(context):
    """Admin panel klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_stats', context))],
        [KeyboardButton(get_text('btn_view_complaints', context))],
        [KeyboardButton(get_text('btn_export_menu', context))],
        [KeyboardButton(get_text('btn_dashboard', context))],
        [KeyboardButton(get_text('btn_settings', context))],  # YANGI - Sozlamalar
        [KeyboardButton(get_text('btn_back_main', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_export_menu_keyboard(context):
    """Excel export qilinadigan narsalar klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_export_excel', context))],
        [KeyboardButton(get_text('btn_export_lesson', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_yes_no_keyboard(context):
    """Ha/Yo'q klaviaturasi (Lokalizatsiya qilingan)"""
    keyboard = [[
        KeyboardButton(get_text('btn_yes', context)),
        KeyboardButton(get_text('btn_no', context))
    ]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_back_keyboard(context):
    """Faqat orqaga tugmasi"""
    return ReplyKeyboardMarkup([[KeyboardButton(get_text('btn_back', context))]], resize_keyboard=True)


# ============================================
# ADMIN CRUD KEYBOARDS
# ============================================

def get_settings_keyboard(context):
    """Sozlamalar menyusi klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_manage_admins', context))],
        [KeyboardButton(get_text('btn_manage_faculties', context))],
        [KeyboardButton(get_text('btn_manage_directions', context))],
        [KeyboardButton(get_text('btn_manage_questions', context))],
        [KeyboardButton(get_text('btn_manage_languages', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_crud_keyboard(context):
    """CRUD operatsiyalari klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_add', context))],
        [KeyboardButton(get_text('btn_list', context))],
        [KeyboardButton(get_text('btn_delete', context))],
        [KeyboardButton(get_text('btn_back', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_confirm_keyboard(context):
    """Tasdiqlash klaviaturasi"""
    keyboard = [
        [KeyboardButton(get_text('btn_confirm', context))],
        [KeyboardButton(get_text('btn_cancel', context))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
