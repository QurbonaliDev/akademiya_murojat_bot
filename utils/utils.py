# utils.py
# Yordamchi funksiyalar - DINAMIK (bazadan o'qiydi)

from telegram import KeyboardButton, ReplyKeyboardMarkup


def get_text(key: str, context) -> str:
    """
    Berilgan kalit bo'yicha tarjimani qaytaradi (BAZADAN).
    Til context.user_data['language'] dan olinadi (default: 'uz').
    """
    lang_code = context.user_data.get('language', 'uz')
    
    # Avval bazadan o'qishga harakat qilamiz
    try:
        from database_models import get_translation
        value = get_translation(key, lang_code)
        if value and value != key:
            return value
    except Exception:
        pass
    
    # Fallback: eski locales.py dan
    from config.locales import LOCALES
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
    Fakultet kodiga qarab yo'nalishlar lug'atini qaytaradi (BAZADAN)
    """
    try:
        from database_models import get_directions_by_faculty as db_get_directions
        return db_get_directions(faculty_code)
    except Exception:
        # Fallback
        from config.config import FACULTY_DIRECTIONS
        return FACULTY_DIRECTIONS.get(faculty_code.lower(), {})


def get_all_directions():
    """Barcha yo'nalishlarni olish (BAZADAN)"""
    try:
        from database_models import get_all_directions_dict
        return get_all_directions_dict()
    except Exception:
        from config.config import ALL_DIRECTIONS
        return ALL_DIRECTIONS


def get_faculties():
    """Barcha fakultetlarni olish (BAZADAN)"""
    try:
        from database_models import get_faculties_dict
        return get_faculties_dict()
    except Exception:
        from config.config import FACULTIES
        return FACULTIES


def get_education_types():
    """Ta'lim turlarini olish (BAZADAN)"""
    try:
        from database_models import get_education_types_dict
        return get_education_types_dict()
    except Exception:
        from config.config import EDUCATION_TYPE
        return EDUCATION_TYPE


def get_education_languages():
    """Ta'lim tillarini olish (BAZADAN)"""
    try:
        from database_models import get_education_languages_dict
        return get_education_languages_dict()
    except Exception:
        from config.config import EDUCATION_LANG
        return EDUCATION_LANG


def get_courses(course_type=None):
    """Kurslarni olish (BAZADAN)"""
    try:
        from database_models import get_courses_dict
        return get_courses_dict(course_type)
    except Exception:
        from config.config import COURSES
        return COURSES


def get_regular_courses():
    """Oddiy kurslarni olish"""
    try:
        from database_models import get_regular_courses as db_get_regular
        return db_get_regular()
    except Exception:
        from config.config import COURSES_REGULAR
        return COURSES_REGULAR


def get_magistr_courses():
    """Magistratura kurslarini olish"""
    try:
        from database_models import get_magistr_courses as db_get_magistr
        return db_get_magistr()
    except Exception:
        from config.config import COURSES_MAGISTR
        return COURSES_MAGISTR


def get_complaint_types():
    """Murojaat turlarini olish (BAZADAN)"""
    try:
        from database_models import get_complaint_types_dict
        return get_complaint_types_dict()
    except Exception:
        from config.config import COMPLAINT_TYPES
        return COMPLAINT_TYPES


def get_survey_links():
    """So'rovnoma havolalarini olish (BAZADAN)"""
    try:
        from database_models import get_survey_links_dict
        return get_survey_links_dict()
    except Exception:
        from config.config import SURVEY_LINKS
        return SURVEY_LINKS


def get_active_languages():
    """Faol tillarni olish (BAZADAN)"""
    try:
        from database_models import get_active_languages as db_get_langs
        return db_get_langs()
    except Exception:
        from config.config import LANGS
        return LANGS


def get_direction_name(direction_code, context):
    """Yo'nalish kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    all_directions = get_all_directions()
    trans_key = all_directions.get(direction_code)
    if trans_key:
        return get_text(trans_key, context)
    return "Noma'lum"


def get_direction_code(direction_name):
    """Yo'nalish nomini kodga o'zgartirish (Faqat loglar uchun)"""
    all_directions = get_all_directions()
    return all_directions.get(direction_name, '')


def get_faculty_name(faculty_code, context):
    """Fakultet kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    faculties = get_faculties()
    trans_key = faculties.get(faculty_code)
    if trans_key:
        return get_text(trans_key, context)
    return "Noma'lum"


def get_faculty_code(faculty_name):
    """Fakultet nomini kodga o'zgartirish"""
    faculties = get_faculties()
    return faculties.get(faculty_name, '')


def get_education_lang_name(education_lang_code, context):
    """Til kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    edu_langs = get_education_languages()
    trans_key = edu_langs.get(education_lang_code)
    if trans_key:
        return get_text(trans_key, context)
    return "Noma'lum"


def get_course_name(course_code, context):
    """Kurs kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    courses = get_courses()
    trans_key = courses.get(course_code)
    if trans_key:
        return get_text(trans_key, context)
    return "Noma'lum"


def get_course_code(course_name):
    """Kurs nomini kodga o'zgartirish"""
    courses = get_courses()
    return courses.get(course_name, '')


def get_complaint_type_name(complaint_code, context):
    """Murojaat turi kodini nomga o'zgartirish (Lokalizatsiya qilingan)"""
    complaint_types = get_complaint_types()
    trans_key = complaint_types.get(complaint_code)
    if trans_key:
        return get_text(trans_key, context)
    return "Noma'lum"


def get_complaint_type_code(complaint_name):
    """Murojaat turi nomini kodga o'zgartirish"""
    complaint_types = get_complaint_types()
    return complaint_types.get(complaint_name, '')


def is_admin(user_id):
    """Foydalanuvchi admin ekanligini tekshirish (BAZADAN)"""
    try:
        from database_models import get_admin_ids
        admin_ids = get_admin_ids()
        return user_id in admin_ids
    except Exception:
        # Fallback
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
    
    try:
        from database_models import get_all_translations, get_active_languages
        languages = get_active_languages()
        for lang_code in languages.keys():
            translations = get_all_translations(lang_code)
            for key in keys:
                btn_text = translations.get(key)
                if btn_text:
                    buttons.append(btn_text)
    except Exception:
        # Fallback
        from config.locales import LOCALES
        for lang_code in LOCALES:
            for key in keys:
                btn_text = LOCALES[lang_code].get(key)
                if btn_text:
                    buttons.append(btn_text)
    
    return buttons