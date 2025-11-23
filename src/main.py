import os
import sys
import threading
import webbrowser
import time
from app import app

def open_browser():
    time.sleep(3)  # Ожидание запуска сервера
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    

    app.run(host='0.0.0.0', port=5000, debug=False)
