"""Firebase configuration for FIUFIT"""
import firebase_admin
from firebase_admin import credentials, auth

# import pyrebase
from src.usecase.authentication_service import IAuthenticationService

firebaseConfig = {
    "apiKey": "AIzaSyD6XrGbtwpNBOybOGjNY6eNci26qDGuz6I",
    "authDomain": "fiufit-73a11.firebaseapp.com",
    "projectId": "fiufit-73a11",
    "storageBucket": "fiufit-73a11.appspot.com",
    "messagingSenderId": "587864716594",
    "appId": "1:587864716594:web:30d86e78e5c21d366f132b",
    "measurementId": "G-TCBPRSHX8M",
    "databaseURL": "https://fiufit-18294.firebaseio.com/"
}


PRIVATE_KEY_PATH = "/etc/secrets/fiufit-73a11.json"


class FirebaseAuthService(IAuthenticationService):

    def __init__(self):
        # self.auth = pyrebase.initialize_app(firebaseConfig).auth()
        creds = credentials.Certificate(PRIVATE_KEY_PATH)
        self.app = firebase_admin.initialize_app(creds, firebaseConfig)

    def sign_up(self, email: str, password: str):
        """Sign up a new user in firebase"""
        return auth.create_user(email=email, password=password)
