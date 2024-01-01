import secrets
import string
import tempfile
import os
import re
from glob import glob
from datetime import datetime, timedelta


class SessionManager:

    @staticmethod
    def file():
        file = SessionManager._get_session_files()
        return file[0] if file else ""

    @staticmethod
    def _get_temp_folder():
        return tempfile.gettempdir()

    @staticmethod
    def _get_session_files():
        temp_folder = SessionManager._get_temp_folder()
        file_path = glob(os.path.join(temp_folder, r"TMPAPP*.session"))
        return file_path if file_path else ""

    @staticmethod
    def token():
        if not SessionManager.expired():
            pattern = re.compile(r'TMPAPP(.*?)\.session')
            token = pattern.search(SessionManager.file())
            if token:
                return token.group(1)
        return ""

    @staticmethod
    def remaining_time():
        if not SessionManager.expired():
            session_file = SessionManager.file()
            time = open(session_file, "r").read()
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
            return str(time-datetime.utcnow()).format("%H:%M:%s").split(".")[0]
        else:
            return "0"

    @staticmethod
    def _duration():
        return datetime.utcnow() + timedelta(minutes=30)

    @staticmethod
    def expired():
        session_file = SessionManager.file()
        # if file does not exist
        if not session_file:
            return True
        # if expiry time is not in valid format
        expiry_time = open(session_file, "r").read()
        try:
            expiry_time = datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return True
        # if time expired
        if datetime.utcnow() >= expiry_time:
            return True
        else:
            return False

    @staticmethod
    def create():
        """Creates the session file with token"""
        temp_folder = SessionManager._get_temp_folder()
        token = SessionManager._generate_token()
        duration = SessionManager._duration()
        file_name = "TMPAPP" + token + ".session"
        file_path = os.path.join(temp_folder, file_name)
        with open(file_path, mode="w") as file:
            try:
                file.write(str(duration))
            except IOError:
                return "", ""
            finally:
                file.close()
                return token, duration

    @staticmethod
    def remove():
        session_file = SessionManager._get_session_files()
        if session_file:
            for file in session_file:
                os.remove(file)

    @staticmethod
    def _generate_token(length=32):
        characters = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(characters) for _ in range(length))
        return token
