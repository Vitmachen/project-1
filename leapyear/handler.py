import http.server
import urllib.parse
from collections import deque

from .utils import build_page, is_leap_year


class LeapYearHandler(http.server.BaseHTTPRequestHandler):
    history = deque(maxlen=20)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        year_text = query.get("year", [""])[0]

        if parsed.path == "/shutdown":
            body = (
                """<!doctype html><html lang=\"ru\"><head><meta charset=\"utf-8\"><title>Выход</title></head>"
                "<body><div style='font-family:Arial,sans-serif;padding:24px;max-width:420px;margin:auto;'>"
                "<h1>Сервер остановлен</h1><p>Можно закрыть эту вкладку.</p></div></body></html>"""
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            self.server.shutdown()
            return

        result_message = ""
        result_color = ""

        if year_text:
            if year_text.lstrip("-").isdigit() and year_text != "-":
                year = int(year_text)
                if year <= 0:
                    result_message = "Ошибка: год должен быть положительным числом"
                    result_color = "#e74c3c"
                else:
                    is_leap = is_leap_year(year)
                    result_message = (
                        f"Год {year} {'является' if is_leap else 'не является'} високостным"
                    )
                    result_color = "#27ae60" if is_leap else "#e74c3c"
                    LeapYearHandler.history.appendleft((year, is_leap))
            else:
                result_message = "Ошибка: год должен быть числом"
                result_color = "#e74c3c"

        body = build_page(result_message, result_color, LeapYearHandler.history)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        return
