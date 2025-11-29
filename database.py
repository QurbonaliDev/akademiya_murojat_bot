# database.py
# Ma'lumotlar bazasi bilan ishlash

import sqlite3
import logging
from config.config import DATABASE_NAME

logger = logging.getLogger(__name__)


def init_database():
    """Ma'lumotlar bazasini yaratish"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty TEXT NOT NULL,
            direction TEXT NOT NULL,
            course TEXT NOT NULL,
            complaint_type TEXT NOT NULL,
            subject_name TEXT,
            teacher_name TEXT,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    init_lesson_rating_table()

    conn.commit()
    conn.close()
    logger.info("Ma'lumotlar bazasi muvaffaqiyatli yaratildi")

def init_lesson_rating_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lesson_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direction TEXT NOT NULL,
            course TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            teacher_name TEXT NOT NULL,
            question_number INTEGER NOT NULL,
            question TEXT NOT NULL,
            rating INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("Lesson ratings table initialized")

def save_complaint(data):
    """Murojaatni bazaga saqlash"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO complaints (faculty,direction, course, complaint_type, subject_name, teacher_name, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['faculty'],
        data['direction'],
        data['course'],
        data['complaint_type'],
        data.get('subject_name', ''),
        data.get('teacher_name', ''),
        data['message']
    ))

    conn.commit()
    conn.close()
    logger.info(f"Yangi murojaat saqlandi: {data['complaint_type']}")


def get_all_complaints(limit=None):
    """Barcha murojaatlarni olish"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = 'SELECT * FROM complaints ORDER BY created_at ASC'
    if limit:
        query += f' LIMIT {limit}'

    cursor.execute(query)
    complaints = cursor.fetchall()
    conn.close()

    return complaints

def save_lesson_rating(data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO lesson_ratings (direction, course, subject_name, teacher_name, question_number, question, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['direction'],
        data['course'],
        data['subject_name'],
        data['teacher_name'],
        data['question_number'],
        data['question'],
        data['rating']
    ))

    conn.commit()
    conn.close()
    logger.info("Yangi dars bahosi saqlandi")

def get_lesson_ratings(limit=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = "SELECT * FROM lesson_ratings ORDER BY created_at DESC"
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()

    return records


def get_statistics():
    """Statistikalarni olish"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    stats = {}

    # Umumiy soni
    cursor.execute('SELECT COUNT(*) FROM complaints')
    stats['total'] = cursor.fetchone()[0]

    # Yo'nalishlar bo'yicha
    cursor.execute('SELECT direction, COUNT(*) FROM complaints GROUP BY direction ORDER BY COUNT(*) ASC')
    stats['by_direction'] = cursor.fetchall()

    # Murojaat turlari bo'yicha
    cursor.execute('SELECT complaint_type, COUNT(*) FROM complaints GROUP BY complaint_type ORDER BY COUNT(*) ASC')
    stats['by_type'] = cursor.fetchall()

    # Kurslar bo'yicha
    cursor.execute('SELECT course, COUNT(*) FROM complaints GROUP BY course ORDER BY COUNT(*) ASC')
    stats['by_course'] = cursor.fetchall()

    # So'nggi 7 kun
    cursor.execute('''
        SELECT DATE(created_at), COUNT(*) 
        FROM complaints 
        WHERE created_at >= date("now", "-7 days") 
        GROUP BY DATE(created_at) 
        ORDER BY DATE(created_at)
    ''')
    stats['weekly'] = cursor.fetchall()

    # Bugungi
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE DATE(created_at) = DATE('now')")
    stats['today'] = cursor.fetchone()[0]

    # Haftalik
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE created_at >= date('now', '-7 days')")
    stats['week'] = cursor.fetchone()[0]

    # Oylik
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE created_at >= date('now', '-30 days')")
    stats['month'] = cursor.fetchone()[0]

    # Eng ko'p yo'nalish
    cursor.execute('SELECT direction, COUNT(*) FROM complaints GROUP BY direction ORDER BY COUNT(*) ASC LIMIT 1')
    top = cursor.fetchone()
    stats['top_direction'] = top if top else ('', 0)

    conn.close()

    return stats