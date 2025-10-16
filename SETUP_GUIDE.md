# 🚀 Telegram Bot - Batafsil O'rnatish Qo'llanmasi

## 📋 1-Qadam: Kerakli dasturlarni o'rnatish

### Python o'rnatish
1. [Python.org](https://www.python.org/downloads/) dan Python 3.8+ versiyasini yuklab oling
2. O'rnatish vaqtida "Add Python to PATH" variantini belgilang

### Python o'rnatilganligini tekshirish
```bash
python --version
```

## 📁 2-Qadam: Loyiha strukturasini yaratish

### Papkalarni yaratish
```bash
mkdir education_bot
cd education_bot
mkdir handlers
```

### Fayllarni joylashtirish
Quyidagi fayllarni yarating:

```
education_bot/
├── main.py
├── config.py
├── database.py
├── keyboards.py
├── utils.py
├── export.py
├── requirements.txt
├── .gitignore
├── README.md
└── handlers/
    ├── __init__.py
    ├── complaint.py
    ├── rules.py
    ├── survey.py
    └── admin.py
```

## 🔑 3-Qadam: Telegram Bot yaratish

### BotFather bilan bot yaratish
1. Telegram'da [@BotFather](https://t.me/BotFather) ni oching
2. `/newbot` komandasini yuboring
3. Bot nomini kiriting (masalan: "Education Monitoring Bot")
4. Bot username kiriting (masalan: "education_monitoring_bot")
5. BotFather sizga **BOT TOKEN** beradi (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Bot tokenini saqlash
Token shunday ko'rinishda bo'ladi:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

## 🔧 4-Qadam: Konfiguratsiya

### config.py faylini tahrirlash
```python
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"  # BotFather'dan olgan tokenni qo'ying
ADMIN_IDS = [123456789]  # Sizning Telegram ID raqamingiz
```

### Telegram ID ni aniqlash
1. [@userinfobot](https://t.me/userinfobot) botiga o'ting
2. `/start` ni bosing
3. Bot sizga ID raqamingizni ko'rsatadi

### So'rovnoma havolalarini yangilash
`config.py` da `SURVEY_LINKS` bo'limini o'zgartiring:
```python
SURVEY_LINKS = {
    'teachers': "SIZNING_GOOGLE_FORMS_HAVOLANGIZ",
    'education': "SIZNING_GOOGLE_FORMS_HAVOLANGIZ",
    'employers': "SIZNING_GOOGLE_FORMS_HAVOLANGIZ"
}
```

## 📦 5-Qadam: Kutubxonalarni o'rnatish

### Virtual muhit yaratish (ixtiyoriy, lekin tavsiya etiladi)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

Yoki alohida-alohida:
```bash
pip install python-telegram-bot==20.7
pip install pandas==2.1.4
pip install openpyxl==3.1.2
```

## 📄 6-Qadam: PDF fayllarni tayyorlash (ixtiyoriy)

Agar tartib qoidalar bo'limi uchun PDF fayllar kerak bo'lsa:

1. Quyidagi nomlar bilan PDF fayllar yarating:
   - `baholash_jarayoni.pdf`
   - `imtihon_jarayoni.pdf`
   - `tartib_qoidalari.pdf`

2. Fayllarni bot katalogiga joylashtiring

## ▶️ 7-Qadam: Botni ishga tushirish

### Birinchi marta ishga tushirish
```bash
python main.py
```

### Kutilayotgan chiqish
```
2024-01-15 10:00:00 - __main__ - INFO - Ma'lumotlar bazasi ishga tushirildi
2024-01-15 10:00:00 - __main__ - INFO - Bot ishga tushmoqda...
```

### Botni tekshirish
1. Telegram'da botingizni oching
2. `/start` komandasini yuboring
3. Klaviatura tugmalari ko'rinishi kerak

## ✅ 8-Qadam: Botni test qilish

### Asosiy funksiyalarni tekshirish
1. **Murojaat**: "📝 Murojaat" tugmasini bosing va jarayonni oxirigacha bajaring
2. **Tartib qoidalar**: "📋 Tartib qoidalar" ni oching va bo'limlarni ko'ring
3. **So'rovnoma**: "📊 So'rovnoma" ni ochib havolalarni tekshiring
4. **Admin panel**: "👨‍💼 Admin" tugmasini bosing (faqat admin uchun)

### Admin panel test qilish
1. Admin panel ochilishini tekshiring
2. Statistikalarni ko'ring
3. Excel export qiling
4. Dashboard ni ko'ring

## 🔄 9-Qadam: Doimiy ishlatish

### Windows uchun
Botni avtomatik ishga tushirish uchun `.bat` fayl yarating:

**run_bot.bat:**
```batch
@echo off
cd /d "C:\path\to\your\education_bot"
python main.py
pause
```

### Linux/Mac uchun
Botni fonda ishlatish:
```bash
nohup python main.py &
```

Yoki systemd service yarating:
```bash
sudo nano /etc/systemd/system/education_bot.service
```

**education_bot.service:**
```ini
[Unit]
Description=Education Monitoring Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/education_bot
ExecStart=/usr/bin/python3 /path/to/education_bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Service'ni ishga tushirish:
```bash
sudo systemctl daemon-reload
sudo systemctl enable education_bot
sudo systemctl start education_bot
```

## 🐛 10-Qadam: Xatoliklarni tuzatish

### Umumiy muammolar

#### Bot tokenida xato
**Xato:** `telegram.error.InvalidToken`
**Yechim:** `config.py` da to'g'ri tokenni kiriting

#### Kutubxona topilmadi
**Xato:** `ModuleNotFoundError: No module named 'telegram'`
**Yechim:** 
```bash
pip install python-telegram-bot
```

#### Ma'lumotlar bazasi xatosi
**Xato:** `sqlite3.OperationalError`
**Yechim:** 
```bash
# Bazani qayta yaratish
rm education_system.db
python main.py
```

#### Admin panelga kirish mumkin emas
**Yechim:** 
1. `config.py` da `ADMIN_IDS` ro'yxatini tekshiring
2. To'g'ri Telegram ID kiritilganligini tekshiring

### Loglarni ko'rish
Bot o'z faoliyatini konsolga chiqaradi. Xatolarni ko'rish uchun konsol chiqishini kuzating.

## 📊 11-Qadam: Ma'lumotlarni boshqarish

### Bazani zaxiralash
```bash
cp education_system.db education_system_backup.db
```

### Excel export
Admin panel orqali "📤 Excel export" tugmasini bosing

### Bazani tozalash (ehtiyotkorlik bilan!)
```python
import sqlite3
conn = sqlite3.connect('education_system.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM complaints')
conn.commit()
conn.close()
```

## 🔐 12-Qadam: Xavfsizlik

### Bot tokenini himoya qilish
1. Token'ni hech qachon Git'ga yuklamang
2. `.gitignore` faylida `config.py` ni qo'shing
3. Maxfiy ma'lumotlarni environment variablelar'da saqlang

### Environment variables ishlatish (ixtiyoriy)
```python
# config.py
import os
BOT_TOKEN = os.getenv('BOT_TOKEN', 'default_token')
```

Terminal'da:
```bash
export BOT_TOKEN="sizning_tokeningiz"
python main.py
```

## 📈 13-Qadam: Monitoring

### Bot ishlayotganini tekshirish
```bash
# Linux/Mac
ps aux | grep main.py

# Windows
tasklist | findstr python
```

### Xotira ishlatilishini ko'rish
```bash
# Linux
top -p $(pgrep -f main.py)
```

## 🆘 Yordam

### Tez-tez so'raladigan savollar

**S: Bot javob bermayapti?**
J: 
1. Bot ishlab turganligini tekshiring
2. Internetga ulanishni tekshiring
3. Loglarni ko'rib chiqing

**S: Klaviatura ko'rinmayapti?**
J: Bot kodida `ReplyKeyboardMarkup` ishlatilganligini tekshiring

**S: Excel export ishlamayapti?**
J: `pandas` va `openpyxl` o'rnatilganligini tekshiring

**S: Admin panel ochilmayapti?**
J: `ADMIN_IDS` da ID to'g'ri kiritilganligini tekshiring

## 🎉 Tayyor!

Botingiz ishga tushdi! Endi foydalanishingiz mumkin.

Qo'shimcha savol va muammolar uchun GitHub Issues'da murojaat qiling.