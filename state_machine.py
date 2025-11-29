from telegram import Update
from telegram.ext import ContextTypes
from menu import show_main_menu
from handlers.complaints.complaint_v2 import (
    start_complaint, handle_direction_choice, handle_course_choice,
    handle_complaint_type_choice, handle_subject_entry, handle_teacher_entry,
    handle_complaint_message
)
from handlers.rules.rules_v2 import show_rules_main
from handlers.surveys.survey_v2 import show_survey_main
from handlers.admins.admin_v2 import show_admin_panel, handle_admin_flow
from utils.utils_v2 import t,lang
import logging


logger = logging.getLogger(__name__)

class StateMachine:
    def __init__(self):
        self.transitions = {
            'choosing_direction': {
                'handler': handle_direction_choice,
                'back': show_main_menu,
                'next': 'choosing_course'
            },
            'choosing_course': {
                'handler': handle_course_choice,
                'back': start_complaint,
                'next': 'choosing_complaint_type'
            },
            'choosing_complaint_type': {
                'handler': handle_complaint_type_choice,
                'back': handle_course_choice,
                'next': 'entering_subject'
            },
            'entering_subject': {
                'handler': handle_subject_entry,
                'back': handle_complaint_type_choice,
                'next': 'entering_teacher'
            },
            'entering_teacher': {
                'handler': handle_teacher_entry,
                'back': handle_complaint_type_choice,
                'next': 'entering_message'
            },
            'entering_message': {
                'handler': handle_complaint_message,
                'back': handle_complaint_type_choice
            },
            'rules_main': {
                'handler': show_rules_main,
                'back': show_main_menu
            },
            'survey_main': {
                'handler': show_survey_main,
                'back': show_main_menu
            },
            'admin_panel': {
                'handler': handle_admin_flow,
                'back': show_main_menu
            },
        }

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get('state', 'main_menu')
        text = update.message.text
        logger.debug(f"StateMachine: state={state}, text={text}")

        if text == t('back', context):
            transition = self.transitions.get(state, {})
            back_handler = transition.get('back', show_main_menu)
            await back_handler(update, context)
            return

        transition = self.transitions.get(state, {})
        if transition and 'handler' in transition:
            await transition['handler'](update, context)
        else:
            await show_main_menu(update, context)