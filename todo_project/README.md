# Django To-Do + Reminder

## รัน
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
เปิด http://127.0.0.1:8000  (บัญชีตัวอย่างใน db.sqlite3: demo / demo12345)

## แจ้งเตือน
    python manage.py send_reminders --loop
ถ้ายังไม่ตั้ง `TELEGRAM_BOT_TOKEN` จะพิมพ์ข้อความลงคอนโซลแทน

## โครงสร้าง
- config/ settings, urls
- tasks/  models, views, forms, urls, management/commands/send_reminders.py
- templates/ หน้าเว็บ (Bootstrap 5)
