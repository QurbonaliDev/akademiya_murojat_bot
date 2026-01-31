# export.py
# Excel va CSV export funksiyalari (rangli dizayn bilan)

import logging
import sqlite3
from datetime import datetime

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font

from config.config import DATABASE_NAME

logger = logging.getLogger(__name__)


def export_to_excel():
    """Murojaatlarni Excel fayliga eksport qilish (rangli dizayn bilan)"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)

        df = pd.read_sql_query('''
            SELECT 
                id as "ID",
                faculty as "Fakultet",
                direction as "Yo'nalish",
                course as "Kurs",
                education_type as "Talim turi",
                education_lang as "Talim tili",
                complaint_type as "Murojaat turi",
                subject_name as "Fan nomi",
                teacher_name as "O'qituvchi",
                message as "Xabar",
                created_at as "Sana"
            FROM complaints 
            ORDER BY created_at ASC
        ''', conn)

        conn.close()

        filename = f"murojaatlar_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')

        # === Excel faylni ochamiz va dizayn beramiz ===
        wb = load_workbook(filename)
        ws = wb.active

        # --- Stil sozlamalari ---
        header_fill = PatternFill("solid", fgColor="2E7D32")  # To‘q yashil
        header_font = Font(bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style='thin', color='000000'),
            right=Side(style='thin', color='000000'),
            top=Side(style='thin', color='000000'),
            bottom=Side(style='thin', color='000000')
        )

        # --- Har bir katakni sozlash ---
        for r_idx, row in enumerate(ws.iter_rows(), start=1):
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(wrap_text=True, vertical="top")

                if r_idx == 1:  # sarlavha qatori
                    cell.fill = header_fill
                    cell.font = header_font

        # --- Ustun kengligini avtomatik belgilash ---
        max_col_width = 40
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                val = str(cell.value) if cell.value is not None else ""
                if len(val) > max_length:
                    max_length = len(val)
            ws.column_dimensions[col_letter].width = min(max_length + 2, max_col_width)

        # --- Filtr qo‘shish ---
        ws.auto_filter.ref = ws.dimensions

        wb.save(filename)

        logger.info(f"Excel fayl muvaffaqiyatli rangli tarzda yaratildi: {filename}")
        return filename

    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        return None


def export_to_excel_for_lesson_ratings():
    """Dars kunlik baholashni Excel fayliga eksport qilish (rangli dizayn bilan)"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)

        df = pd.read_sql_query('''
            SELECT
                id AS "ID",
                direction AS "Yo'nalish",
                course AS "Kurs",
                subject_name AS "Fan",
                teacher_name AS "O'qituvchi",
                question_number AS "Savol raqami",
                question AS "Savol ",
                rating AS "Bahosi",
                created_at AS "Sana"
            FROM lesson_ratings
            ORDER BY created_at DESC
        ''', conn)

        conn.close()

        filename = f"lesson_ratings_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')

        # === Excel faylni ichidan sozlash ===
        wb = load_workbook(filename)
        ws = wb.active

        # --- Stil sozlamalari ---
        header_fill = PatternFill("solid", fgColor="2E7D32")  # To‘q yashil
        header_font = Font(bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style='thin', color='000000'),
            right=Side(style='thin', color='000000'),
            top=Side(style='thin', color='000000'),
            bottom=Side(style='thin', color='000000')
        )

        # --- Har bir katakni ustida ish ---
        for r_idx, row in enumerate(ws.iter_rows(), start=1):
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(wrap_text=True, vertical="top")

                if r_idx == 1:  # sarlavha qatori
                    cell.fill = header_fill
                    cell.font = header_font

        # --- Ustun kengliklari ---
        max_col_width = 40
        for col in ws.columns:
            max_len = 0
            col_letter = col[0].column_letter
            for cell in col:
                text = str(cell.value) if cell.value else ""
                if len(text) > max_len:
                    max_len = len(text)
            ws.column_dimensions[col_letter].width = min(max_len + 2, max_col_width)

        # --- Filtr qo‘shish ---
        ws.auto_filter.ref = ws.dimensions

        wb.save(filename)

        logger.info(f"Excel muvaffaqiyatli yaratildi: {filename}")
        return filename

    except Exception as e:
        logger.error(f"Excel export xatosi: {e}")
        return None
