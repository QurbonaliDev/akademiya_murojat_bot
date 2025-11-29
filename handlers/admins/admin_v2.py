import logging
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards_all_lang_v2 import get_admin_keyboard, get_back_keyboard
from utils.utils_v2 import is_admin, get_direction_name, get_course_name, get_complaint_type_name, t, lang
from database import get_all_complaints, get_statistics
from config.export import export_to_excel
from text.texts_v2 import TEXTS
from menu import show_main_menu

logger = logging.getLogger(__name__)

async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panelni ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(t('admin_access_denied', context))
        return
    context.user_data['state'] = 'admin_panel'
    await update.message.reply_text(
        t('admin_panel_intro', context),
        reply_markup=get_admin_keyboard(context)
    )

async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikalarni ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(t('admin_access_denied', context))
        return
    stats = get_statistics()
    user_lang = lang(context)
    stats_text = t('admin_stats_intro', context)
    stats_text += t('admin_stats_total', context, total=stats['total'])
    stats_text += t('admin_stats_by_direction', context)
    for direction, count in stats['by_direction']:
        stats_text += t('admin_stats_item', context, name=get_direction_name(direction, user_lang), count=count)
    stats_text += t('admin_stats_by_type', context)
    for complaint_type, count in stats['by_type']:
        stats_text += t('admin_stats_item', context, name=get_complaint_type_name(complaint_type, user_lang), count=count)
    stats_text += t('admin_stats_by_course', context)
    for course, count in stats['by_course']:
        stats_text += t('admin_stats_item', context, name=get_course_name(course, user_lang), count=count)
    stats_text += t('admin_stats_weekly', context)
    if stats['weekly']:
        for date_str, count in stats['weekly']:
            stats_text += t('admin_stats_item', context, name=date_str, count=count)
    else:
        stats_text += t('admin_stats_no_data', context)
    await update.message.reply_text(stats_text, reply_markup=get_back_keyboard(context))

async def view_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaatlarni ko'rish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(t('admin_access_denied', context))
        return
    complaints = get_all_complaints(limit=10)
    user_lang = lang(context)
    if not complaints:
        response = t('admin_no_complaints', context)
    else:
        response = t('admin_complaints_intro', context)
        for comp in complaints:
            response += t('admin_complaint_item', context,
                         id=comp[0],
                         direction=get_direction_name(comp[1], user_lang),
                         course=get_course_name(comp[2], user_lang),
                         complaint_type=get_complaint_type_name(comp[3], user_lang),
                         subject=comp[4] or '',
                         teacher=comp[5] or '',
                         message=comp[6][:100] + '...' if len(comp[6]) > 100 else comp[6],
                         date=comp[7])
            response += '─' * 30 + '\n'
    await update.message.reply_text(response, reply_markup=get_back_keyboard(context))

async def export_to_excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel faylga export qilish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(t('admin_access_denied', context))
        return
    await update.message.reply_text(t('admin_export_processing', context))
    try:
        filename = export_to_excel()
        if filename:
            with open(filename, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=filename,
                    caption=t('admin_export_success', context)
                )
            await update.message.reply_text(t('admin_export_completed', context))
        else:
            await update.message.reply_text(t('admin_export_error', context))
    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        await update.message.reply_text(t('admin_export_error', context))

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dashboard ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(t('admin_access_denied', context))
        return
    stats = get_statistics()
    user_lang = lang(context)
    dashboard_text = t('admin_dashboard_intro', context,
                      today=stats['today'],
                      week=stats['week'],
                      month=stats['month'])
    if stats['top_direction'][0]:
        dashboard_text += t('admin_dashboard_top_direction', context,
                           direction=get_direction_name(stats['top_direction'][0], user_lang),
                           count=stats['top_direction'][1])
    await update.message.reply_text(dashboard_text, reply_markup=get_back_keyboard(context))

async def handle_admin_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin jarayonini boshqarish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(t('admin_access_denied', context))
        return
    text = update.message.text
    user_lang = lang(context)
    admin_menu = TEXTS["admin"][user_lang]
    handlers = {
        admin_menu[0]: show_statistics,
        admin_menu[1]: view_complaints,
        admin_menu[2]: export_to_excel_handler,
        admin_menu[3]: show_dashboard,
        admin_menu[4]: show_main_menu,
    }
    handler = handlers.get(text, show_admin_panel)
    logger.debug(f"Admin handler for text: {text}")
    await handler(update, context)