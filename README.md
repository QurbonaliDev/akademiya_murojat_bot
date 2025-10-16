# Talim Tizimi Monitoring Bot

Bu Telegram bot talim muassasalari uchun monitoring va murojaat tizimini taqdim etadi.

## 📁 Fayl tuzilmasi

```
bot/
├── main.py                    # Asosiy bot fayli
├── config.py                  # Konfiguratsiya va sozlamalar
├── database.py                # Ma'lumotlar bazasi funksiyalari
├── keyboards.py               # Klaviatura tugmalari
├── utils.py                   # Yordamchi funksiyalar
├── export.py                  # Excel/CSV export funksiyalari
├── handlers/
│   ├── __init__.py           # Handlers package
│   ├── complaint.py          # Murojaat handlerlari
│   ├── rules.py              # Tartib qoidalar handlerlari
│   ├── survey.py             # So'rovnoma handlerlari
│   └── admin.py              # Admin panel handlerlari
└── README.md                  # Bu fayl
```

## 🚀 O'rnatish

### 1. Kerakli kutubxonalarni o'rnatish

```bash
pip install python-telegram-bot
pip install pandas
pip install openpyxl
pip install sqlite3
```

### 2. Konfiguratsiya

`config.py` faylida quyidagi sozlamalarni o'zgartiring:

- `BOT_TOKEN` - Telegram bot tokeningizni kiriting
- `ADMIN_IDS` - Admin foydalanuvchilar ID raqamlarini kiriting

### 3. Botni ishga tushirish

```bash
python main.py
```

## 🎯 Asosiy funksiyalar

### 1. Murojaat tizimi (complaint.py)
- Yo'nalish tanlash
- Kurs tanlash
- Murojaat turi tanlash
- Fan va o'qituvchi haqida ma'lumot
- Anonim murojaat yuborish

### 2. Tartib qoidalar (rules.py)
- Baholash jarayoni
- Imtihon jarayoni
- Umumiy tartib qoidalar
- PDF fayllarni yuklab olish

### 3. So'rovnoma (survey.py)
- O'qituvchilar haqida so'rovnoma
- Talim sifati so'rovnomasi
- Ish beruvchilar so'rovnomasi
- So'rovnoma natijalarini ko'rish

### 4. Admin panel (admin.py)
- Statistikalar ko'rish
- Murojaatlarni ko'rish
- Excel formatda eksport qilish
- Dashboard

## 📊 Ma'lumotlar bazasi

Bot SQLite ma'lumotlar bazasidan foydalanadi. Baza avtomatik ravishda yaratiladi:

**Jadval**: `complaints`
- id - Unikal ID
- direction - Yo'nalish
- course - Kurs
- complaint_type - Murojaat turi
- subject_name - Fan nomi
- teacher_name - O'qituvchi ismi
- message - Murojaat matni
- created_at - Yaratilgan sana

## 🔒 Xavfsizlik

- Barcha murojaatlar anonim shaklda saqlanadi
- Foydalanuvchi ma'lumotlari saqlanmaydi
- Admin panelga faqat ruxsat berilgan foydalanuvchilar kirishi mumkin

## 📝 Qo'shimcha ma'lumotlar

### PDF fayllar

Quyidagi PDF fayllarni bot katalogiga joylashtiring:
- `baholash_jarayoni.pdf`
- `imtihon_jarayoni.pdf`
- `tartib_qoidalari.pdf`

### So'rovnoma havolalari

`config.py` faylida Google Forms havolalarini yangilang.

## 🛠️ Xatoliklarni tuzatish

Agar bot ishlamasa:

1. Bot tokenini tekshiring
2. Python kutubxonalari o'rnatilganligini tekshiring
3. Ma'lumotlar bazasi faylini tekshiring
4. Log fayllarni ko'rib chiqing

## 📞 Yordam

Muammolar yuzaga kelsa, bot loglarini tekshiring yoki botni qayta ishga tushiring.

## 🔄 Yangilanishlar

Bot doimiy ravishda yangilanadi. Eng so'nggi versiyani olish uchun repozitoriyani tekshiring.