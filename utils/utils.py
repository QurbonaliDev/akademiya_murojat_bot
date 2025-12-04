# utils.py
# Yordamchi funksiyalar
from telegram import KeyboardButton, ReplyKeyboardMarkup

from config.config import DIRECTIONS, COURSES, COMPLAINT_TYPES, FACULTIES, FACULTY_DIRECTIONS, EDUCATION_LANG
from text.texts import TEXTS


def get_directions_by_faculty(faculty_code: str):
    """
    Fakultet kodiga qarab yo'nalishlar lug'atini qaytaradi
    """
    return FACULTY_DIRECTIONS.get(faculty_code.upper(), {})


def get_dynamic_keyboard(items: dict):
    """
    Lug'atdan telegram keyboard yaratadi
    """
    buttons = [[KeyboardButton(name)] for name in items.keys()]
    buttons.append([KeyboardButton("🔙 Orqaga")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_direction_name(direction_code):
    """Yo'nalish kodini nomga o'zgartirish"""
    directions = {v: k for k, v in DIRECTIONS.items()}
    return directions.get(direction_code, 'Noma\'lum')


def get_direction_code(direction_name):
    """Yo'nalish nomini kodga o'zgartirish"""
    return DIRECTIONS.get(direction_name, '')

def get_faculty_name(course_code):
    """Kurs kodini nomga o'zgartirish"""
    faculties = {v: k for k, v in FACULTIES.items()}
    return faculties.get(course_code, 'Noma\'lum')

def get_education_lang_name(education_lang_code):
    """Kurs kodini nomga o'zgartirish"""
    education_lang = {v: k for k, v in EDUCATION_LANG.items()}
    return education_lang.get(education_lang_code, 'Noma\'lum')

def get_course_name(course_code):
    """Kurs kodini nomga o'zgartirish"""
    courses = {v: k for k, v in COURSES.items()}
    return courses.get(course_code, 'Noma\'lum')

def get_faculty_code(course_name):
    """Fakultet nomini kodga o'zgartirish"""
    return FACULTIES.get(course_name, '')

def get_course_code(course_name):
    """Kurs nomini kodga o'zgartirish"""
    return COURSES.get(course_name, '')


def get_complaint_type_name(complaint_code):
    """Murojaat turi kodini nomga o'zgartirish"""
    types = {v: k for k, v in COMPLAINT_TYPES.items()}
    return types.get(complaint_code, 'Noma\'lum')


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

    Endi har joyda faqat lang(context) yozasan va bo'ldi!
    """
    return context.user_data.get('language', 'uz')


def t(key: str, context, **kwargs) -> str:
    """
    Tarjima olish - SUPER OSON!

    Foydalanish:
        t('welcome', context)
        t('error_message', context, name="Ali")
    """
    user_lang = lang(context)

    if key in TEXTS:
        text = TEXTS[key].get(user_lang, TEXTS[key].get('uz', ''))

        # Agar parametrlar berilgan bo'lsa (masalan, ismni qo'yish uchun)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass

        return text

    return key


def get_button(button_name: str, context) -> str:
    """
    Tugma matnini olish

    Foydalanish:
        get_button('back', context)
    """
    return t(button_name, context)