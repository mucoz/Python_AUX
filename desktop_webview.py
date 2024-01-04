import webview
import sys
from app import app # app in app.py module
from killable_thread import KThread

if __name__ == '__main__':
    # run flask app in a different thread
    flask_app = KThread(target=app.run)
    flask_app.start()
    # run GUI
    webview.create_window(title='Application', url='http://127.0.0.1:5000', width=800, height=600, server=app)
    webview.start(http_server=True)
    # after GUI, terminate flask app
    flask_app.kill()
    sys.exit()
