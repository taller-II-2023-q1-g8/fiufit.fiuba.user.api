import pyrebase


firebaseConfig = {
  "apiKey": "AIzaSyD6XrGbtwpNBOybOGjNY6eNci26qDGuz6I",
  "authDomain": "fiufit-73a11.firebaseapp.com",
  "projectId": "fiufit-73a11",
  "storageBucket": "fiufit-73a11.appspot.com",
  "messagingSenderId": "587864716594",
  "appId": "1:587864716594:web:30d86e78e5c21d366f132b",
  "measurementId": "G-TCBPRSHX8M",
  "databaseURL": "https://fiufit-18294.firebaseio.com/" 
};

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def sign_up(email: str, password: str):
    auth.create_user_with_email_and_password(email, password)
