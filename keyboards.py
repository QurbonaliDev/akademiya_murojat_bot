# keyboards.py
# ReplyKeyboard klaviaturalari

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import DIRECTIONS, COURSES, COMPLAINT_TYPES


def get_main_menu_keyboard():
    """Asosiy menyu klaviaturasi"""
    keyboard = [
        [KeyboardButton("📝 Murojaat")],
        [KeyboardButton("📋 Tartib qoidalar")],
        [KeyboardButton("📊 So'rovnoma")],
        [KeyboardButton("👨‍💼 Admin")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_directions_keyboard():
    """Yo'nalishlar klaviaturasi"""
    keyboard = [[KeyboardButton(direction)] for direction in DIRECTIONS.keys()]
    keyboard.append([KeyboardButton("🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_courses_keyboard():
    """Kurslar klaviaturasi"""
    keyboard = [[KeyboardButton(course)] for course in COURSES.keys()]
    keyboard.append([KeyboardButton("🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_complaint_types_keyboard():
    """Murojaat turlari klaviaturasi"""
    keyboard = [[KeyboardButton(complaint)] for complaint in COMPLAINT_TYPES.keys()]
    keyboard.append([KeyboardButton("🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_keyboard():
    """Tartib qoidalar klaviaturasi"""
    keyboard = [
        [KeyboardButton("📊 Baholash jarayoni")],
        [KeyboardButton("📝 Imtihon jarayoni")],
        [KeyboardButton("📋 Umumiy tartib qoida")],
        [KeyboardButton("🔙 Bosh sahifa")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_detail_keyboard():
    """Qoidalar detali klaviaturasi"""
    keyboard = [
        [KeyboardButton("📥 PDF yuklab olish")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_keyboard():
    """So'rovnoma asosiy klaviaturasi"""
    keyboard = [
        [KeyboardButton("👨‍🏫 O'qituvchilar haqida")],
        [KeyboardButton("🎓 Ta'lim sifati")],
        [KeyboardButton("💼 Ish beruvchilar")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_links_keyboard():
    """So'rovnoma havolalari klaviaturasi"""
    keyboard = [
        # [KeyboardButton("🔗 So'rovnomaga o'tish")],
        # [KeyboardButton("📊 Natijalarni ko'rish")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_keyboard():
    """Admin panel klaviaturasi"""
    keyboard = [
        [KeyboardButton("📊 Statistikalar")],
        [KeyboardButton("📋 Murojaatlarni ko'rish")],
        [KeyboardButton("📤 Excel export")],
        [KeyboardButton("📈 Dashboard")],
        [KeyboardButton("🔙 Asosiy menyu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_back_keyboard():
    """Faqat orqaga tugmasi"""
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 Orqaga")]], resize_keyboard=True)
