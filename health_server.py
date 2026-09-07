# -*- coding: utf-8 -*-
"""
health_server.py
سيرفر HTTP بسيط جدًا (بدون Flask، بمكتبة http.server المدمجة في بايثون) يعمل في
Thread منفصل بجانب البوت. سبب وجوده: Render كـ Web Service يرسل طلبات HTTP دورية
للتأكد أن الخدمة "حية"؛ بوت تيليجرام العادي (polling فقط) لا يستمع على أي منفذ،
فيعتبره Render غير سليم ويعيد نشره بلا توقف. هذا السيرفر فقط يرد "OK" على أي طلب،
وهذا كافٍ لإرضاء فحص الصحة، دون أي تأثير على منطق البوت نفسه.

لا يُستخدم هذا الملف إطلاقًا إن كانت الاستضافة تدعم Background Worker مباشرة.
"""

import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)


class _HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Noor Bot is running.".encode("utf-8"))

    def log_message(self, format, *args):
        pass  # يمنع طباعة كل طلب health-check في اللوج (يحدث كل بضع ثوانٍ)


def start_health_server(port: int):
    """يشغّل سيرفر الصحة في Thread خلفي منفصل، بحيث لا يوقف أو يبطئ البوت الرئيسي."""
    server = HTTPServer(("0.0.0.0", port), _HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"سيرفر فحص الصحة يعمل على المنفذ {port} (لتوافق Render Web Service).")
    return server
