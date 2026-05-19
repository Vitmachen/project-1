import socketserver
import sys
import webbrowser

from leapyear.handler import LeapYearHandler


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    url = f"http://{host}:{port}/"
    print(f"Сервер запущен: {url}")
    print("Откройте этот адрес в браузере.")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with socketserver.TCPServer((host, port), LeapYearHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nВыход.")
        finally:
            httpd.server_close()
            print("Сервер остановлен.")
            sys.exit(0)


if __name__ == "__main__":
    run_server()
