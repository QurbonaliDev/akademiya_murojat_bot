# keyboards.py
# Universal 3-language keyboard system (UZ / EN / RU)

from telegram import ReplyKeyboardMarkup, KeyboardButton
from text.texts import TEXTS

# === TRANSLATIONS ===

def get_language_keyboard():
    """Language selection keyboard"""
    buttons = [
        [KeyboardButton("🇺🇿 O'zbek tili")],
        [KeyboardButton("🇬🇧 English")],
        [KeyboardButton("🇷🇺 Русский")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_main_menu_keyboard(lang="uz"):
    """Main menu keyboard"""
    buttons = [[KeyboardButton(text)] for text in TEXTS["main_menu"][lang]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_settings_keyboard(lang="uz"):
    """Settings keyboard"""
    buttons = [[KeyboardButton(text)] for text in TEXTS["settings"][lang]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# def get_directions_keyboard(lang="uz"):
#     """Directions keyboard"""
#     buttons = [[KeyboardButton(direction)] for direction in DIRECTIONS.keys()]
#     buttons.append([KeyboardButton(TEXTS["back"][lang])])
#     return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
#
#
# def get_courses_keyboard(lang="uz"):
#     """Courses keyboard"""
#     buttons = [[KeyboardButton(course)] for course in COURSES.keys()]
#     buttons.append([KeyboardButton(TEXTS["back"][lang])])
#     return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
#
#
# def get_complaint_types_keyboard(lang="uz"):
#     """Complaint types keyboard"""
#     buttons = [[KeyboardButton(complaint)] for complaint in COMPLAINT_TYPES.keys()]
#     buttons.append([KeyboardButton(TEXTS["back"][lang])])
#     return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_directions_keyboard(lang="uz"):
    """Directions keyboard - dinamik til bilan"""
    directions = TEXTS['directions'][lang]  # dict: {display_name: code}
    buttons = [[KeyboardButton(name)] for name in directions.keys()]
    buttons.append([KeyboardButton(TEXTS['back'][lang])])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_courses_keyboard(lang="uz"):
    """Courses keyboard - dinamik til bilan"""
    courses = TEXTS['courses'][lang]  # dict: {display_name: code}
    buttons = [[KeyboardButton(name)] for name in courses.keys()]
    buttons.append([KeyboardButton(TEXTS['back'][lang])])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_complaint_types_keyboard(lang="uz"):
    """Complaint types keyboard - dinamik til bilan"""
    complaints = TEXTS['complaint_types'][lang]  # dict: {display_name: code}
    buttons = [[KeyboardButton(name)] for name in complaints.keys()]
    buttons.append([KeyboardButton(TEXTS['back'][lang])])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_rules_keyboard(lang="uz"):
    """Rules keyboard"""
    texts = TEXTS["rules"][lang]
    buttons = [[KeyboardButton(text)] for text in texts]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_rules_detail_keyboard(lang="uz"):
    """Rules details keyboard"""
    buttons = [
        [KeyboardButton(TEXTS["download_pdf"][lang])],
        [KeyboardButton(TEXTS["back"][lang])]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_survey_keyboard(lang="uz"):
    """Survey keyboard"""
    texts = TEXTS["survey"][lang]
    buttons = [[KeyboardButton(text)] for text in texts]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_admin_keyboard(lang="uz"):
    """Admin panel keyboard"""
    texts = TEXTS["admin"][lang]
    buttons = [[KeyboardButton(text)] for text in texts]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_back_keyboard(lang="uz"):
    """Back button only"""
    return ReplyKeyboardMarkup([[KeyboardButton(TEXTS["back"][lang])]], resize_keyboard=True)


def get_text(key, lang="uz"):
    """Get translated text by key"""
    if key in TEXTS:
        return TEXTS[key].get(lang, TEXTS[key]["uz"])
    return ""