"""ส่งแจ้งเตือนงานที่ถึงเวลา. รันทุก 1 นาที เช่น:  python manage.py send_reminders --loop"""
import json, time, urllib.request
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    req = urllib.request.Request(url, json.dumps({"chat_id": chat_id, "text": text}).encode(),
                                 {"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)

class Command(BaseCommand):
    help = "Send due task reminders via Telegram (prints to console if not configured)"
    def add_arguments(self, p): p.add_argument("--loop", action="store_true")
    def handle(self, *a, **o):
        while True:
            self.run_once()
            if not o["loop"]: break
            time.sleep(60)
    def run_once(self):
        due = Task.objects.filter(remind_at__lte=timezone.now(), reminded=False, is_done=False).select_related("user")
        for t in due:
            msg = f"⏰ {t.title}" + (f"\n{t.description}" if t.description else "")
            chat_id = getattr(getattr(t.user, "profile", None), "telegram_chat_id", "")
            try:
                if settings.TELEGRAM_BOT_TOKEN and chat_id: send_telegram(chat_id, msg)
                else: self.stdout.write(f"[console] to {t.user.username}: {msg}")
                t.reminded = True
                t.save(update_fields=["reminded"])
            except Exception as e:
                self.stderr.write(f"failed task {t.pk}: {e}")
