# handlers/admin.py
# Admin panel bilan bog'liq handlerlar

import logging
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.keyboards import get_admin_keyboard
from utils.utils import is_admin, get_direction_name, get_course_name, get_complaint_type_name
from database import get_all_complaints, get_statistics
from config.export import export_to_excel , export_to_excel_for_lesson_ratings

logger = logging.getLogger(__name__)


async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panelni ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    context.user_data['state'] = 'admin_panel'

    await update.message.reply_text(
        "👨‍💼 **Admin paneli**\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=get_admin_keyboard()
    )


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistikalarni ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    stats = get_statistics()

    stats_text = f"📊 Umumiy statistikalar\n\n"
    stats_text += f"📈 Jami murojaatlar: {stats['total']} ta\n\n"

    stats_text += "🎯 Yo'nalishlar bo'yicha: \n"
    for direction, count in stats['by_direction']:
        stats_text += f"  • {get_direction_name(direction)}: {count} ta\n"

    stats_text += "\n📝 Murojaat turlari bo'yicha:\n"
    for complaint_type, count in stats['by_type']:
        stats_text += f"  • {get_complaint_type_name(complaint_type)}: {count} ta\n"

    stats_text += "\n📚 Kurslar bo'yicha:\n"
    for course, count in stats['by_course']:
        stats_text += f"  • {get_course_name(course)}: {count} ta\n"

    stats_text += "\n📅 So'nggi 7 kun:\n"
    if stats['weekly']:
        for date_str, count in stats['weekly']:
            stats_text += f"  • {date_str}: {count} ta\n"
    else:
        stats_text += "  Ma'lumot yo'q\n"

    await update.message.reply_text(stats_text)


async def view_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Murojaatlarni ko'rish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    complaints = get_all_complaints(limit=10)

    if not complaints:
        response = "📭 Hozircha murojaatlar mavjud emas."
    else:
        response = "📊 So'nggi 10 ta murojaat:\n\n"
        for comp in complaints:
            response += f"🆔 ID: {comp[0]}\n"
            response += f"🎯 Yo'nalish: {get_direction_name(comp[1])}\n"
            response += f"📚 Kurs: {get_course_name(comp[2])}\n"
            response += f"📝 Turi: {get_complaint_type_name(comp[3])}\n"

            if comp[4]:  # Fan nomi
                response += f"📖 Fan: {comp[4]}\n"
            if comp[5]:  # O'qituvchi
                response += f"👨‍🏫 O'qituvchi: {comp[5]}\n"

            response += f"💬 Xabar: {comp[6][:100]}...\n" if len(comp[6]) > 100 else f"💬 Xabar: {comp[6]}\n"
            response += f"📅 Sana: {comp[7]}\n"
            response += "─" * 30 + "\n"

    await update.message.reply_text(response)


async def export_to_excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel faylga export qilish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    try:
        await update.message.reply_text("⏳ Excel fayl tayyorlanmoqda...")

        filename = export_to_excel()

        if filename:
            with open(filename, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=filename,
                    caption="📊 Barcha murojaatlar (Excel format)"
                )
            await update.message.reply_text("✅ Excel fayli muvaffaqiyatli yuklandi!")
        else:
            await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Ma'lumotlar bazasini tekshiring.")

async def export_to_daily_lesson_excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel faylga export qilish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    try:
        await update.message.reply_text("⏳ Excel fayl tayyorlanmoqda...")

        filename = export_to_excel_for_lesson_ratings()

        if filename:
            with open(filename, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=filename,
                    caption="📊 Barcha murojaatlar (Excel format)"
                )
            await update.message.reply_text("✅ Excel fayli muvaffaqiyatli yuklandi!")
        else:
            await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi. Ma'lumotlar bazasini tekshiring.")


async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dashboard ko'rsatish"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Sizga ruxsat berilmagan!")
        return

    stats = get_statistics()

    dashboard_text = (
        "📊 Monitoring Dashboard\n\n"
        f"📅 Bugun: {stats['today']} ta murojaat\n"
        f"📅 So'nggi 7 kun: {stats['week']} ta murojaat\n"
        f"📅 So'nggi 30 kun: {stats['month']} ta murojaat\n\n"
    )

    if stats['top_direction'][0]:
        dashboard_text += (
            f"🏆 Eng faol yo'nalish: "
            f"{get_direction_name(stats['top_direction'][0])} "
            f"({stats['top_direction'][1]} ta)\n"
        )

    await update.message.reply_text(dashboard_text)