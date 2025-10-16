# handlers/rules.py
# Tartib qoidalar bilan bog'liq handlerlar

import os
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_rules_keyboard, get_rules_detail_keyboard
from config import PDF_FILES


async def show_rules_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tartib qoidalar asosiy menyusi"""
    context.user_data['state'] = 'rules_main'

    await update.message.reply_text(
        "📋 Tartib qoidalar bo'limi:\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=get_rules_keyboard()
    )


async def show_grading_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Baholash jarayoni"""
    context.user_data['state'] = 'rules_grading'
    context.user_data['current_pdf'] = 'grading'

    text = (
        "📊 Baholash jarayoni:\n\n"
        "Talabalarning bilim darajasi 100 ballik tizim asosida baholanadi:\n\n"
        "• 86-100 ball - A'lo\n"
        "• 71-85 ball - Yaxshi\n"
        "• 56-70 ball - Qoniqarli\n"
        "• 55 va undan past - Qoniqarsiz\n\n"
        "Baholash amaliy, nazariy va mustaqil ishlar asosida amalga oshiriladi."
    )

    await update.message.reply_text(
        text,
        reply_markup=get_rules_detail_keyboard()
    )


async def show_exam_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Imtihon jarayoni"""
    context.user_data['state'] = 'rules_exam'
    context.user_data['current_pdf'] = 'exam'

    text = (
        "📝 Imtihon jarayoni:\n\n"
        "Imtihonlar semestr davomida va oxirida o'tkaziladi:\n\n"
        "• O'rta nazorat (midterm) - 30%\n"
        "• Amaliy topshiriqlar - 20%\n"
        "• Yakuniy imtihon - 50%\n\n"
        "Imtihonlar ochiq va yopiq shaklda o'tkazilishi mumkin."
    )

    await update.message.reply_text(
        text,
        reply_markup=get_rules_detail_keyboard()
    )


async def show_general_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Umumiy tartib qoidalar"""
    context.user_data['state'] = 'rules_general'
    context.user_data['current_pdf'] = 'rules'

    text = (
        "📋 Umumiy tartib qoidalar:\n\n"
        "1. Darslarga vaqtida kelish majburiy\n"
        "2. O'qituvchilarga hurmatli munosabat\n"
        "3. Akademik halollik prinsipi\n"
        "4. O'quv jarayonida faol ishtirok\n"
        "5. Muhokamalarda adabiy til\n\n"
        "Qoidalarni buzgan talabalar intizomiy javobgarlikka tortiladi."
    )

    await update.message.reply_text(
        text,
        reply_markup=get_rules_detail_keyboard()
    )


async def download_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PDF faylni yuklash"""
    pdf_type = context.user_data.get('current_pdf')

    if not pdf_type:
        await update.message.reply_text("❌ Avval qoidalar bo'limini tanlang.")
        return

    pdf_name = PDF_FILES.get(pdf_type, 'document.pdf')

    if os.path.exists(pdf_name):
        with open(pdf_name, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=pdf_name,
                caption=f"📥 {pdf_name} fayli"
            )
    else:
        await update.message.reply_text(
            f"❌ {pdf_name} fayli hozircha mavjud emas.\n"
            "Keyinroq urinib ko'ring yoki administratorga murojaat qiling."
        )