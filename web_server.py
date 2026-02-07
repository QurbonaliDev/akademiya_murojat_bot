# web_server.py
# Mini App uchun aiohttp web server

import os
import json
import logging
from aiohttp import web
from aiohttp.web import middleware
import sqlite3

from config.config import DATABASE_NAME

logger = logging.getLogger(__name__)

# ============================================
# MIDDLEWARE
# ============================================

@middleware
async def cors_middleware(request, handler):
    """CORS headers qo'shish"""
    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# ============================================
# DATABASE HELPERS
# ============================================

def get_db_connection():
    """Database ulanish"""
    return sqlite3.connect(DATABASE_NAME)


def get_translations(lang_code='uz'):
    """Tarjimalarni olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM translations WHERE language_code = ?', (lang_code,))
    translations = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return translations


def get_faculties_from_db():
    """Fakultetlarni olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT code, translation_key FROM faculties WHERE is_active = 1 ORDER BY sort_order')
    faculties = [{'code': row[0], 'translation_key': row[1]} for row in cursor.fetchall()]
    conn.close()
    return faculties


def get_directions_from_db(faculty_code=None):
    """Yo'nalishlarni olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    if faculty_code:
        cursor.execute('''
            SELECT code, faculty_code, translation_key FROM directions 
            WHERE faculty_code = ? AND is_active = 1 ORDER BY sort_order
        ''', (faculty_code,))
    else:
        cursor.execute('SELECT code, faculty_code, translation_key FROM directions WHERE is_active = 1 ORDER BY sort_order')
    directions = [{'code': row[0], 'faculty_code': row[1], 'translation_key': row[2]} for row in cursor.fetchall()]
    conn.close()
    return directions


def get_courses_from_db(course_type=None):
    """Kurslarni olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    if course_type:
        cursor.execute('''
            SELECT code, translation_key, course_type FROM courses 
            WHERE is_active = 1 AND course_type = ? ORDER BY sort_order
        ''', (course_type,))
    else:
        cursor.execute('SELECT code, translation_key, course_type FROM courses WHERE is_active = 1 ORDER BY sort_order')
    courses = [{'code': row[0], 'translation_key': row[1], 'course_type': row[2]} for row in cursor.fetchall()]
    conn.close()
    return courses


def get_education_types_from_db():
    """Ta'lim turlarini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT code, translation_key FROM education_types WHERE is_active = 1 ORDER BY sort_order')
    edu_types = [{'code': row[0], 'translation_key': row[1]} for row in cursor.fetchall()]
    conn.close()
    return edu_types


def get_education_languages_from_db():
    """Ta'lim tillarini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT code, translation_key FROM education_languages WHERE is_active = 1')
    edu_langs = [{'code': row[0], 'translation_key': row[1]} for row in cursor.fetchall()]
    conn.close()
    return edu_langs


def get_complaint_types_from_db():
    """Murojaat turlarini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT code, translation_key, requires_subject, requires_teacher 
        FROM complaint_types WHERE is_active = 1
    ''')
    complaint_types = [{
        'code': row[0], 
        'translation_key': row[1],
        'requires_subject': bool(row[2]),
        'requires_teacher': bool(row[3])
    } for row in cursor.fetchall()]
    conn.close()
    return complaint_types


def save_complaint_to_db(data):
    """Murojaatni saqlash"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints (
            faculty, direction, course, education_type, education_lang,
            complaint_type, subject_name, teacher_name, message, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('faculty', ''),
        data.get('direction', ''),
        data.get('course', ''),
        data.get('education_type', ''),
        data.get('education_language', ''),
        data.get('complaint_type', ''),
        data.get('subject_name', ''),
        data.get('teacher_name', ''),
        data.get('message', ''),
        'webapp'  # Mini App dan kelgan deb belgilaymiz
    ))
    conn.commit()
    complaint_id = cursor.lastrowid
    conn.close()
    return complaint_id


# ============================================
# API ROUTES
# ============================================

async def api_health(request):
    """Health check"""
    return web.json_response({'status': 'ok', 'service': 'akademiya-miniapp'})


async def api_translations(request):
    """Tarjimalarni olish"""
    lang = request.match_info.get('lang', 'uz')
    translations = get_translations(lang)
    return web.json_response(translations)


async def api_faculties(request):
    """Fakultetlarni olish"""
    faculties = get_faculties_from_db()
    return web.json_response({'faculties': faculties})


async def api_directions(request):
    """Yo'nalishlarni olish"""
    faculty_code = request.match_info.get('faculty', None)
    directions = get_directions_from_db(faculty_code)
    return web.json_response({'directions': directions})


async def api_courses(request):
    """Kurslarni olish"""
    course_type = request.query.get('type', None)
    courses = get_courses_from_db(course_type)
    return web.json_response({'courses': courses})


async def api_education_types(request):
    """Ta'lim turlarini olish"""
    edu_types = get_education_types_from_db()
    return web.json_response({'education_types': edu_types})


async def api_education_languages(request):
    """Ta'lim tillarini olish"""
    edu_langs = get_education_languages_from_db()
    return web.json_response({'education_languages': edu_langs})


async def api_complaint_types(request):
    """Murojaat turlarini olish"""
    complaint_types = get_complaint_types_from_db()
    return web.json_response({'complaint_types': complaint_types})


async def api_submit_complaint(request):
    """Murojaat yuborish"""
    try:
        data = await request.json()
        
        # Validatsiya
        required_fields = ['faculty', 'direction', 'course', 'complaint_type', 'message']
        for field in required_fields:
            if not data.get(field):
                return web.json_response(
                    {'success': False, 'error': f'Missing field: {field}'}, 
                    status=400
                )
        
        complaint_id = save_complaint_to_db(data)
        
        return web.json_response({
            'success': True, 
            'complaint_id': complaint_id,
            'message': 'Murojaat muvaffaqiyatli qabul qilindi!'
        })
    except Exception as e:
        logger.error(f"Error submitting complaint: {e}")
        return web.json_response(
            {'success': False, 'error': str(e)}, 
            status=500
        )


async def api_config(request):
    """Barcha konfiguratsiyani birdan olish (optimizatsiya)"""
    lang = request.query.get('lang', 'uz')
    
    return web.json_response({
        'translations': get_translations(lang),
        'faculties': get_faculties_from_db(),
        'education_types': get_education_types_from_db(),
        'education_languages': get_education_languages_from_db(),
        'complaint_types': get_complaint_types_from_db(),
        'courses': {
            'regular': get_courses_from_db('regular'),
            'magistr': get_courses_from_db('magistr')
        }
    })


async def index_handler(request):
    """Asosiy index.html ni yuborish"""
    index_path = os.path.join(os.path.dirname(__file__), 'webapp', 'index.html')
    if os.path.exists(index_path):
        return web.FileResponse(index_path)
    return web.Response(text="index.html topilmadi", status=404)


# ============================================
# WEBAPP SERVER
# ============================================

def create_webapp_server():
    """Web server yaratish"""
    app = web.Application(middlewares=[cors_middleware])
    
    # API routes
    app.router.add_get('/api/health', api_health)
    app.router.add_get('/api/translations/{lang}', api_translations)
    app.router.add_get('/api/faculties', api_faculties)
    app.router.add_get('/api/directions', api_directions)
    app.router.add_get('/api/directions/{faculty}', api_directions)
    app.router.add_get('/api/courses', api_courses)
    app.router.add_get('/api/education-types', api_education_types)
    app.router.add_get('/api/education-languages', api_education_languages)
    app.router.add_get('/api/complaint-types', api_complaint_types)
    app.router.add_post('/api/complaint', api_submit_complaint)
    app.router.add_get('/api/config', api_config)
    
    # Root route for index.html
    app.router.add_get('/', index_handler)

    # Static files (CSS, JS)
    webapp_path = os.path.join(os.path.dirname(__file__), 'webapp')
    if os.path.exists(webapp_path):
        # append_version=True browser keshlash problemalarini oldini oladi
        app.router.add_static('/', webapp_path, name='static')
    
    return app


async def start_web_server(host='0.0.0.0', port=8080):
    """Web serverni ishga tushirish"""
    app = create_webapp_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f"Mini App web server ishga tushdi: http://{host}:{port}")
    return runner
