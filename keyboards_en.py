# keyboards.py
# ReplyKeyboard layouts

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import DIRECTIONS, COURSES, COMPLAINT_TYPES


def get_main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [KeyboardButton("📝 Complaint")],
        [KeyboardButton("📋 Rules & Regulations")],
        [KeyboardButton("📊 Survey")],
        [KeyboardButton("👨‍💼 Admin")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_directions_keyboard():
    """Directions keyboard"""
    keyboard = [[KeyboardButton(direction)] for direction in DIRECTIONS.keys()]
    keyboard.append([KeyboardButton("🔙 Back")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_courses_keyboard():
    """Courses keyboard"""
    keyboard = [[KeyboardButton(course)] for course in COURSES.keys()]
    keyboard.append([KeyboardButton("🔙 Back")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_complaint_types_keyboard():
    """Complaint types keyboard"""
    keyboard = [[KeyboardButton(complaint)] for complaint in COMPLAINT_TYPES.keys()]
    keyboard.append([KeyboardButton("🔙 Back")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_keyboard():
    """Rules & Regulations keyboard"""
    keyboard = [
        [KeyboardButton("📊 Evaluation Process")],
        [KeyboardButton("📝 Examination Process")],
        [KeyboardButton("📋 General Rules")],
        [KeyboardButton("🔙 Home")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_rules_detail_keyboard():
    """Rules detail keyboard"""
    keyboard = [
        [KeyboardButton("📥 Download PDF")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_keyboard():
    """Survey main keyboard"""
    keyboard = [
        [KeyboardButton("👨‍🏫 About Teachers")],
        [KeyboardButton("🎓 Education Quality")],
        [KeyboardButton("💼 Employers")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_survey_links_keyboard():
    """Survey links keyboard"""
    keyboard = [
        # [KeyboardButton("🔗 Go to Survey")],
        # [KeyboardButton("📊 View Results")],
        [KeyboardButton("🔙 Back")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_keyboard():
    """Admin panel keyboard"""
    keyboard = [
        [KeyboardButton("📊 Statistics")],
        [KeyboardButton("📋 View Complaints")],
        [KeyboardButton("📤 Export to Excel")],
        [KeyboardButton("📈 Dashboard")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_back_keyboard():
    """Back button only"""
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 Back")]], resize_keyboard=True)
