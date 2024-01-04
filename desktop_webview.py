import webview
import threading
import sys
from app import app # app in app.py module


if __name__ == '__main__':
    # run flask app in a different thread
    flask_app = threading.Thread(target=app.run)
    flask_app.start()
    # run GUI
    webview.create_window(title='Application', url='http://127.0.0.1:5000', width=800, height=600)
    webview.start(http_server=True)
    # after GUI, terminate flask app
    sys.exit()
  
