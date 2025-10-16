# config.py
# Bot sozlamalari va konstantalar

BOT_TOKEN = "8136137840:AAF7_Wf9KU2epPkGKdsijfdx6zIwNzPVfc8"
ADMIN_IDS = [2015170305,1370651372]

DATABASE_NAME = 'education_system.db'

# Yo'nalishlar
DIRECTIONS = {
    'Islomshunoslik': 'islom',
    'Dinshunoslik': 'din',
    'KI': 'ki',
    'AXB': 'axb',
    'JIXM': 'jixm',
    'Yuristpensiya': 'yurist',
    'Jurnalistika': 'journal',
    'Turizim': 'turizm',
    'XM': 'xm'
}

# Kurslar
COURSES = {
    '1-kurs': '1',
    '2-kurs': '2',
    '3-kurs': '3',
    '4-kurs': '4',
    '1-magistr': 'mag1',
    '2-magistr': 'mag2'
}

# Murojaat turlari
COMPLAINT_TYPES = {
    "👨‍🏫 O'qituvchi haqida": 'teacher',
    "💻 Texnik-taminot": 'technical',
    "📖 Dars jarayoni": 'lesson'
}

# So'rovnoma havolalari
SURVEY_LINKS = {
    'teachers': "https://docs.google.com/forms/d/e/1FAIpQLScLaVr0ymp9MyuoLj-LAryP0IDyq_lQH98Wh6iXvMOKVJpmxA/viewform?usp=dialog",
    'education': "https://docs.google.com/forms/d/e/1FAIpQLSdEXAMPLE1/viewform?usp=dialog",
    'employers': "https://docs.google.com/forms/d/e/1FAIpQLSdEXAMPLE2/viewform?usp=dialog"
}

# PDF fayllar
PDF_FILES = {
    'grading': 'baholash_jarayoni.pdf',
    'exam': 'imtihon_jarayoni.pdf',
    'rules': 'tartib_qoidalari.pdf'
}