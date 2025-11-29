from telegram import ReplyKeyboardMarkup, KeyboardButton
from text.texts_v2 import TEXTS
from utils.utils_v2 import lang

def get_language_keyboard():
    return ReplyKeyboardMarkup([
        ["🇺🇿 O'zbek tili", "🇬🇧 English", "🇷🇺 Русский"]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_main_menu_keyboard(context):
    user_lang = lang(context)
    main_menu = TEXTS["main_menu"][user_lang]
    return ReplyKeyboardMarkup([
        [main_menu[0], main_menu[1]],
        [main_menu[2], main_menu[3]],
        [main_menu[4]]
    ], resize_keyboard=True)

def get_back_keyboard(context):
    user_lang = lang(context)
    return ReplyKeyboardMarkup([[TEXTS["back"][user_lang]]], resize_keyboard=True)

def get_admin_keyboard(context):
    user_lang = lang(context)
    admin_menu = TEXTS["admin"][user_lang]
    return ReplyKeyboardMarkup([
        [admin_menu[0], admin_menu[1]],
        [admin_menu[2], admin_menu[3]],
        [admin_menu[4]]
    ], resize_keyboard=True)

def get_complaint_direction_keyboard(context):
    user_lang = lang(context)
    directions = TEXTS["directions"][user_lang]
    return ReplyKeyboardMarkup([[d] for d in directions] + [[TEXTS["back"][user_lang]]], resize_keyboard=True)

def get_complaint_course_keyboard(context):
    user_lang = lang(context)
    courses = TEXTS["courses"][user_lang]
    return ReplyKeyboardMarkup([[c] for c in courses] + [[TEXTS["back"][user_lang]]], resize_keyboard=True)

def get_complaint_type_keyboard(context):
    user_lang = lang(context)
    complaint_types = TEXTS["complaint_types"][user_lang]
    return ReplyKeyboardMarkup([[t] for t in complaint_types] + [[TEXTS["back"][user_lang]]], resize_keyboard=True)