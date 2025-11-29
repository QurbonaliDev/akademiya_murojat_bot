# keyboards.py
# Клавиатуры ReplyKeyboard

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config.config import DIRECTIONS, COURSES, COMPLAINT_TYPES


def get_main_menu_keyboard():
    """Главное меню"""
    keyboard = [
        [KeyboardButton("📝 Обращение")],
        [KeyboardButton("📋 Правила и порядок")],
        [KeyboardButton("📊 Опрос")],
        [KeyboardButton("👨‍💼 Админ")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_directions_keyboard():
    """Клавиатура направлений"""
    keyboard = [[KeyboardButton(direction)] for direction in DIRECTIONS.keys()]
    keyboard.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_courses_keyboard():
    """Клавиатура курсов"""
    keyboard = [[KeyboardButton(course)] for course in COURSES.keys()]
    keyboard.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_complaint_types_keyboard():
    """Клавиатура типов обращений"""
    keyboard = [[KeyboardButton(complaint)] for complaint in COMPLAINT_TYPES.keys()]
    keyboard.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_keyboard():
    """Клавиатура правил и порядка"""
    keyboard = [
        [KeyboardButton("📊 Процесс оценки")],
        [KeyboardButton("📝 Процесс экзамена")],
        [KeyboardButton("📋 Общие правила")],
        [KeyboardButton("🔙 Главная страница")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_detail_keyboard():
    """Клавиатура деталей правил"""
    keyboard = [
        [KeyboardButton("📥 Скачать PDF")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_keyboard():
    """Основная клавиатура опроса"""
    keyboard = [
        [KeyboardButton("👨‍🏫 Об учителях")],
        [KeyboardButton("🎓 Качество обучения")],
        [KeyboardButton("💼 Работодатели")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_links_keyboard():
    """Клавиатура ссылок на опрос"""
    keyboard = [
        # [KeyboardButton("🔗 Перейти к опросу")],
        # [KeyboardButton("📊 Просмотреть результаты")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_keyboard():
    """Клавиатура панели администратора"""
    keyboard = [
        [KeyboardButton("📊 Статистика")],
        [KeyboardButton("📋 Просмотреть обращения")],
        [KeyboardButton("📤 Экспорт в Excel")],
        [KeyboardButton("📈 Панель управления")],
        [KeyboardButton("🔙 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_back_keyboard():
    """Кнопка 'Назад'"""
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 Назад")]], resize_keyboard=True)
