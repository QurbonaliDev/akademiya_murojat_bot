# utils.py
# Yordamchi funksiyalar
from telegram import KeyboardButton, ReplyKeyboardMarkup

from config.config import ALL_DIRECTIONS, COURSES, COMPLAINT_TYPES, FACULTIES, FACULTY_DIRECTIONS, EDUCATION_LANG
from config.locales import LOCALES

def get_text(key: str, context) -> str:
    """
    Berilgan kalit bo'yicha tarjimani qaytaradi.
    Til context.user_data['language'] dan olinadi (default: 'uz').
    """
    lang_code = context.user_data.get('language', 'uz')
    return LOCALES.get(lang_code, LOCALES['uz']).get(key, key)

def get_code_by_text(text: str, code_map: dict, context) -> str:
    """
    Foydalanuvchi yuborgan tarjima qilingan matndan tegishli kodni topadi.
    code_map: { 'code': 'translation_key' }
    """
    for code, trans_key in code_map.items():
        if text == get_text(trans_key, context):
            return code
    return None


def get_directions_by_faculty(faculty_code: str):
    """
    Fakultet kodiga qarab yo'nalishlar lug'atini qaytaradi
    """
    return FACULTY_DIRECTIONS.get(faculty_code.lower(), {})



def get_direction_name(direction_code, context):
    """Yo'nalish kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    trans_key = ALL_DIRECTIONS.get(direction_code)
    if trans_key:
        return get_text(trans_key, context)
    return 'Noma\'lum'


def get_direction_code(direction_name):
    """Yo'nalish nomini kodga o'zgartirish (Faqat loglar uchun)"""
    return ALL_DIRECTIONS.get(direction_name, '')

def get_faculty_name(faculty_code, context):
    """Fakultet kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    trans_key = FACULTIES.get(faculty_code)
    if trans_key:
        return get_text(trans_key, context)
    return 'Noma\'lum'

def get_education_lang_name(education_lang_code, context):
    """Til kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    trans_key = EDUCATION_LANG.get(education_lang_code)
    if trans_key:
        return get_text(trans_key, context)
    return 'Noma\'lum'

def get_course_name(course_code, context):
    """Kurs kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    trans_key = COURSES.get(course_code)
    if trans_key:
        return get_text(trans_key, context)
    return 'Noma\'lum'

def get_faculty_code(course_name):
    """Fakultet nomini kodga o'zgartirish"""
    return FACULTIES.get(course_name, '')

def get_course_code(course_name):
    """Kurs nomini kodga o'zgartirish"""
    return COURSES.get(course_name, '')


def get_complaint_type_name(complaint_code, context):
    """Murojaat turi kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    trans_key = COMPLAINT_TYPES.get(complaint_code)
    if trans_key:
        return get_text(trans_key, context)
    return 'Noma\'lum'


def get_complaint_type_code(complaint_name):
    """Murojaat turi nomini kodga o'zgartirish"""
    return COMPLAINT_TYPES.get(complaint_name, '')


def is_admin(user_id):
    """Foydalanuvchi admin ekanligini tekshirish"""
    from config.config import ADMIN_IDS
    return user_id in ADMIN_IDS


def lang(context) -> str:
    """
    Foydalanuvchi tilini olish - QISQA VA OSON!
    """
    return context.user_data.get('language', 'uz')

def get_main_menu_buttons():
    """Barcha tillardagi asosiy menyu tugmalarini qaytaradi"""
    keys = ['btn_complaint', 'btn_rules', 'btn_survey', 'btn_lesson_rating', 'btn_admin', 'btn_lang', 'btn_back_main']
    buttons = []
    for lang_code in LOCALES:
        for key in keys:
            btn_text = LOCALES[lang_code].get(key)
            if btn_text:
                buttons.append(btn_text)
    return buttons