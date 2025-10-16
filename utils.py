# utils.py
# Yordamchi funksiyalar

from config import DIRECTIONS, COURSES, COMPLAINT_TYPES


def get_direction_name(direction_code):
    """Yo'nalish kodini nomga o'zgartirish"""
    directions = {v: k for k, v in DIRECTIONS.items()}
    return directions.get(direction_code, 'Noma\'lum')


def get_direction_code(direction_name):
    """Yo'nalish nomini kodga o'zgartirish"""
    return DIRECTIONS.get(direction_name, '')


def get_course_name(course_code):
    """Kurs kodini nomga o'zgartirish"""
    courses = {v: k for k, v in COURSES.items()}
    return courses.get(course_code, 'Noma\'lum')


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
    from config import ADMIN_IDS
    return user_id in ADMIN_IDS