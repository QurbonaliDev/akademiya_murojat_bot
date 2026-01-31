# handlers/admin.py
# Admin panel bilan bog'liq handlerlar

import logging
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards import get_admin_keyboard, get_export_menu_keyboard
from utils.utils import is_admin, get_direction_name, get_course_name, get_complaint_type_name, get_faculty_name, get_text
from database import get_all_complaints, get_statistics
from config.export import export_to_excel , export_to_excel_for_lesson_ratings

logger = logging.getLogger(__name__)


async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panelni ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    context.user_data['state'] = 'admin_panel'

    await update.message.reply_text(
        get_text('admin_panel_title', context),
        reply_markup=get_admin_keyboard(context)
    )


async def show_export_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel export menyusini ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    context.user_data['state'] = 'admin_export_menu'

    await update.message.reply_text(
        get_text('export_menu_title', context),
        reply_markup=get_export_menu_keyboard(context)
    )


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikalarni ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    stats = get_statistics()

    stats_text = get_text('stats_title', context).format(total=stats['total'])
    
    stats_text += get_text('stats_by_direction', context) + "\n"
    for direction, count in stats['by_direction']:
        stats_text += f"  • {get_direction_name(direction, context)}: {count} ta\n"

    stats_text += get_text('stats_by_type', context) + "\n"
    for complaint_type, count in stats['by_type']:
        stats_text += f"  • {get_complaint_type_name(complaint_type, context)}: {count} ta\n"

    stats_text += get_text('stats_by_course', context) + "\n"
    for course, count in stats['by_course']:
        stats_text += f"  • {get_course_name(course, context)}: {count} ta\n"

    stats_text += get_text('stats_weekly', context) + "\n"
    if stats['weekly']:
        for date_str, count in stats['weekly']:
            stats_text += f"  • {date_str}: {count} ta\n"
    else:
        stats_text += get_text('no_data', context) + "\n"

    await update.message.reply_text(stats_text)


async def view_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaatlarni ko'rish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    complaints = get_all_complaints(limit=10)

    if not complaints:
        response = get_text('no_complaints', context)
    else:
        response = get_text('last_10_complaints', context) + "\n"
        for comp in complaints:
            # Schema: id[0], faculty[1], direction[2], course[3], edu_type[4], edu_lang[5], 
            #         complaint_type[6], subject[7], teacher[8], message[9], date[10]
            response += f"🆔 ID: {comp[0]}\n"
            response += f"🏛 {get_faculty_name(comp[1], context)}\n"
            response += f"🎯 {get_direction_name(comp[2], context)}\n"
            response += f"📚 {get_course_name(comp[3], context)}\n"
            response += f"📝 {get_complaint_type_name(comp[6], context)}\n"

            if comp[7]:  # Fan nomi
                response += f"📖 Fan: {comp[7]}\n"
            if comp[8]:  # O'qituvchi
                response += f"👨‍🏫 O'qituvchi: {comp[8]}\n"

            msg = comp[9] if comp[9] else ""
            response += f"💬 Xabar: {msg[:100]}...\n" if len(msg) > 100 else f"💬 Xabar: {msg}\n"
            response += f"📅 Sana: {comp[10]}\n"
            response += "─" * 30 + "\n"

    await update.message.reply_text(response)


async def export_to_excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel faylga export qilish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    try:
        await update.message.reply_text(get_text('excel_preparing', context))

        filename = export_to_excel()

        if filename:
            with open(filename, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=filename,
                    caption="📊 Excel Report"
                )
            await update.message.reply_text(get_text('excel_success', context))
        else:
            await update.message.reply_text(get_text('excel_error', context))

    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        await update.message.reply_text(get_text('excel_error', context))

async def export_to_daily_lesson_excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel faylga export qilish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    try:
        await update.message.reply_text(get_text('excel_preparing', context))

        filename = export_to_excel_for_lesson_ratings()

        if filename:
            with open(filename, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=filename,
                    caption="📊 Daily Lesson Ratings"
                )
            await update.message.reply_text(get_text('excel_success', context))
        else:
            await update.message.reply_text(get_text('excel_error', context))

    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        await update.message.reply_text(get_text('excel_error', context))


async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dashboard ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('no_permission', context))
        return

    stats = get_statistics()

    dashboard_text = get_text('dashboard_title', context).format(
        today=stats['today'],
        week=stats['week'],
        month=stats['month']
    )

    if stats['top_direction'][0]:
        dashboard_text += get_text('dashboard_top_direction', context).format(
            direction=get_direction_name(stats['top_direction'][0], context),
            count=stats['top_direction'][1]
        )

    await update.message.reply_text(dashboard_text)