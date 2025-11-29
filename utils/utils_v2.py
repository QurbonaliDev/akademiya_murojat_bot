from text.texts import TEXTS
from telegram.ext import ContextTypes
from config.config import ADMIN_IDS

def lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Foydalanuvchi tilini olish"""
    return context.user_data.get('language', 'uz')

def t(key: str, context: ContextTypes.DEFAULT_TYPE, **kwargs) -> str:
    """Tarjima qilingan matnni formatlash bilan qaytarish"""
    user_lang = lang(context)
    text = TEXTS.get(key, {}).get(user_lang, TEXTS.get(key, {}).get('uz', key))
    return text.format(**kwargs) if kwargs else text

def get_button(key: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Tugma matnini olish"""
    return t(key, context)

def is_admin(user_id: int) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish"""
    return user_id in ADMIN_IDS

def get_direction_name(direction_code: str, lang: str = 'uz') -> str:
    """Yo'nalish kodini nomga o'zgartirish"""
    directions = TEXTS.get('directions', {}).get(lang, {})
    for name, code in directions.items():
        if code == direction_code:
            return name
    return 'Noma\'lum'

def get_direction_code(direction_name: str, lang: str = 'uz') -> str:
    """Yo'nalish nomini kodga o'zgartirish"""
    return TEXTS.get('directions', {}).get(lang, {}).get(direction_name, '')

def get_course_name(course_code: str, lang: str = 'uz') -> str:
    """Kurs kodini nomga o'zgartirish"""
    courses = TEXTS.get('courses', {}).get(lang, {})
    for name, code in courses.items():
        if code == course_code:
            return name
    return 'Noma\'lum'

def get_course_code(course_name: str, lang: str = 'uz') -> str:
    """Kurs nomini kodga o'zgartirish"""
    return TEXTS.get('courses', {}).get(lang, {}).get(course_name, '')

def get_complaint_type_name(complaint_code: str, lang: str = 'uz') -> str:
    """Murojaat turi kodini nomga o'zgartirish"""
    types = TEXTS.get('complaint_types', {}).get(lang, {})
    for name, code in types.items():
        if code == complaint_code:
            return name
    return 'Noma\'lum'

def get_complaint_type_code(complaint_name: str, lang: str = 'uz') -> str:
    """Murojaat turi nomini kodga o'zgartirish"""
    return TEXTS.get('complaint_types', {}).get(lang, {}).get(complaint_name, '')