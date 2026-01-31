# keyboards.py
# ReplyKeyboard klaviaturalari

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config.config import COURSES, COMPLAINT_TYPES, FACULTIES, FACULTY_DIRECTIONS, EDUCATION_TYPE, \
    EDUCATION_LANG, LANGS

from utils.utils import get_text


def get_language_keyboard():
    """Til tanlash klaviaturasi"""
    # Bu yerda context kerak emas, chunki bu birinchi qadam
    keyboard = [[KeyboardButton(lang_name)] for lang_name in LANGS.values()]
    # Til tanlashda "Orqaga" tugmasi shart emas yoki hardcoded bo'lishi mumkin
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
    """Yo'nalishlar klaviaturasi"""
    from config.config import ALL_DIRECTIONS
    keyboard = [[KeyboardButton(get_text(val, context))] for val in ALL_DIRECTIONS.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_dynamic_keyboard(items: dict, context, prefix="dir_"):
    from telegram import ReplyKeyboardMarkup, KeyboardButton

    buttons = []
    for code, val in items.items():
        # Agarda value o'zi tarjima kaliti bo'lsa
        label = get_text(val, context)
        buttons.append([KeyboardButton(label)])
        
    buttons.append([KeyboardButton(get_text('btn_back', context))])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_faculties_keyboard(context):
    """Fajultetlar klaviaturasi"""
    from config.config import FACULTIES
    keyboard = [[KeyboardButton(get_text(val, context))] for val in FACULTIES.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_education_type_keyboard(context):
    """Talim turi klaviaturasi"""
    from config.config import EDUCATION_TYPE
    keyboard = [[KeyboardButton(get_text(val, context))] for val in EDUCATION_TYPE.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_education_lang_keyboard(context):
    """Talim tili klaviaturasi"""
    from config.config import EDUCATION_LANG
    keyboard = [[KeyboardButton(get_text(val, context))] for val in EDUCATION_LANG.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_courses_keyboard(context):
    """Kurslar klaviaturasi - fakultetga qarab tegishli kurslarni ko'rsatadi"""
    from config.config import COURSES_REGULAR, COURSES_MAGISTR
    
    faculty = context.user_data.get('faculty', '')
    
    # Magistratura uchun faqat 1-2 magistr kurslari
    if faculty == 'magistratura':
        courses = COURSES_MAGISTR
    else:
        # Oddiy fakultetlar uchun faqat 1-4 kurslar
        courses = COURSES_REGULAR
    
    keyboard = [[KeyboardButton(get_text(val, context))] for val in courses.values()]
    keyboard.append([KeyboardButton(get_text('btn_back', context))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_complaint_types_keyboard(context):
    """Murojaat turlari klaviaturasi"""
    from config.config import COMPLAINT_TYPES
    keyboard = [[KeyboardButton(get_text(val, context))] for val in COMPLAINT_TYPES.values()]
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
