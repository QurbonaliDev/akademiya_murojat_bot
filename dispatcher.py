from telegram import Update
from telegram.ext import ContextTypes
from text.texts_v2 import TEXTS
from utils.utils_v2 import t, lang
from menu import show_main_menu
from handlers.complaints.complaint_v2 import start_complaint
from handlers.rules.rules_v2 import show_rules_main
from handlers.surveys.survey_v2 import show_survey_main
from handlers.admins.admin_v2 import show_admin_panel, handle_admin_flow
from keyboards.keyboards_all_lang_v2 import get_language_keyboard
import logging

logger = logging.getLogger(__name__)

class HandlerDispatcher:
    def __init__(self):
        self.handlers = {
            'choosing_language': self.handle_language_choice,
            'settings': self.handle_settings,
            'main_menu': self.handle_main_menu,
            'complaint': self.handle_complaint,
            'rules': show_rules_main,
            'survey': show_survey_main,
            'admin': handle_admin_flow,
        }

    async def dispatch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get('state', 'main_menu')
        text = update.message.text
        user_lang = lang(context)
        main_menu_items = TEXTS["main_menu"].get(user_lang, [])

        logger.debug(f"Dispatch: state={state}, text={text}, user_lang={user_lang}")

        if text in main_menu_items:
            await self.handle_main_menu(update, context)
            return

        handler_key = 'complaint' if state in ['choosing_direction', 'choosing_course', 'choosing_complaint_type', 'entering_subject', 'entering_teacher', 'entering_message'] else \
                     'rules' if state in ['rules_main', 'rules_grading', 'rules_exam', 'rules_general'] else \
                     'survey' if state in ['survey_main', 'survey_teachers', 'survey_education', 'survey_employers'] else \
                     'admin' if state == 'admin_panel' else \
                     state
        handler = self.handlers.get(handler_key, show_main_menu)
        logger.debug(f"Calling handler for key: {handler_key}")
        await handler(update, context)

    async def handle_language_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        lang_map = {
            "🇺🇿 O'zbek tili": "uz",
            "🇬🇧 English": "en",
            "🇷🇺 Русский": "ru"
        }
        selected_lang = lang_map.get(text, "uz")
        context.user_data['language'] = selected_lang
        context.user_data['state'] = 'main_menu'
        logger.debug(f"Language selected: {selected_lang}")
        await update.message.reply_text(t('language_selected', context))
        await show_main_menu(update, context)

    async def handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        user_lang = lang(context)
        settings_menu = TEXTS["settings"][user_lang]
        if text == settings_menu[0]:
            context.user_data['state'] = 'choosing_language'
            await update.message.reply_text(
                t('choose_language', context),
                reply_markup=get_language_keyboard()
            )
        elif text == settings_menu[1]:
            await show_main_menu(update, context)

    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        user_lang = lang(context)
        main_menu = TEXTS["main_menu"][user_lang]
        handlers = {
            main_menu[0]: start_complaint,  # Murojaat
            main_menu[1]: show_rules_main,  # Tartib qoidalar
            main_menu[2]: show_survey_main,  # So'rovnoma
            main_menu[3]: show_admin_panel,  # Admin
            main_menu[4]: self.handle_settings,  # Sozlamalar
        }
        handler = handlers.get(text, show_main_menu)
        logger.debug(f"Main menu handler for text: {text}")
        context.user_data['state'] = {
            main_menu[0]: 'complaint',
            main_menu[1]: 'rules',
            main_menu[2]: 'survey',
            main_menu[3]: 'admin',
            main_menu[4]: 'settings'
        }.get(text, 'main_menu')
        await handler(update, context)

    async def handle_complaint(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from state_machine import StateMachine
        await StateMachine().handle(update, context)