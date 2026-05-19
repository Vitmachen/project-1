from collections import deque
from typing import Deque, Iterable, Tuple

History = Deque[Tuple[int, bool]]


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def build_history_html(history: Iterable[Tuple[int, bool]]) -> str:
    items = []
    for year, is_leap in history:
        status = "високостный" if is_leap else "не високостный"
        color = "#27ae60" if is_leap else "#e74c3c"
        items.append(f"<li style='color: {color};'>{year} — {status}</li>")
    return "\n".join(items)


def build_page(result_message: str = "", result_color: str = "", history: Iterable[Tuple[int, bool]] = None) -> str:
    if history is None:
        history = deque()

    result_html = ""
    if result_message:
        result_html = (
            f"<p style='font-size:1.1em; color: {result_color}; margin: 16px 0;'>{result_message}</p>"
        )

    history_html = build_history_html(history)

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Проверка високосного года</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 24px; background: #f7f7f7; }}
    .card {{ max-width: 420px; margin: auto; padding: 24px; background: white; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); }}
    label {{ display: block; margin-bottom: 8px; font-weight: 600; }}
    input {{ width: 100%; padding: 10px 12px; margin-bottom: 0; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; }}
    .hint {{ color: #555; margin-top: 4px; margin-bottom: 16px; font-size: 0.95em; }}
    button {{ width: 100%; padding: 10px 12px; border: none; border-radius: 8px; background: #0078d4; color: white; font-size: 1em; cursor: pointer; margin-bottom: 0; margin-top: 12px; }}
    button:hover {{ background: #005fa3; }}
    .exit-button {{ background: #d83b01; }}
    .exit-button:hover {{ background: #a52700; }}
    .history-list {{ margin-top: 22px; padding-left: 20px; color: #333; line-height: 1.8; list-style: none; }}
    .history-list li {{ padding: 4px 0; font-weight: 500; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Проверка високосного года</h1>
    <form method="get" action="/">
      <label for="year">Введите год</label>
      <input id="year" name="year" type="text" value="" placeholder="" autocomplete="off" />
      <p class="hint">Введите год</p>
      <button type="submit">Проверить</button>
    </form>
    <form method="get" action="/shutdown">
      <button type="submit" class="exit-button">Выход</button>
    </form>
    {result_html}
    <ul class="history-list">
      {history_html}
    </ul>
  </div>
</body>
</html>"""
