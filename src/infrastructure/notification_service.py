from google.oauth2 import service_account
import google.auth.transport.requests
import requests, os

SEND_NOTIFICATIONS_URL = os.environ.get("SEND_NOTIFICATIONS_URL")
if SEND_NOTIFICATIONS_URL is None:
    print("SEND_NOTIFICATIONS_URL not found in Environment")

PRIVATE_KEY_PATH = "fiufit-73a11.json"


class NotificationService:
    def _get_token(self):
        credentials = service_account.Credentials.from_service_account_file(
            PRIVATE_KEY_PATH,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"],
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials.token

    def send_notification(self, device_token: str, title: str, body: str):
        if SEND_NOTIFICATIONS_URL is None:
            return

        url = SEND_NOTIFICATIONS_URL

        headers = {
            "Authorization": "Bearer " + self._get_token(),
            "Content-Type": "application/json",
        }

        json = {
            "message": {
                "token": device_token,
                "notification": {"body": body, "title": title},
                # "data": {
                #     "id": "1"
                # }
                # },
                # "android": {
                # "notification": {
                #     "click_action":"OPEN_ACTIVITY_3"
                # }
            },
        }

        response = requests.post(url, headers=headers, json=json)
        return response.text