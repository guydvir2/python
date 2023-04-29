import datetime
import requests
TOKEN = "497268459:AAESYm27tJfNXwnnnn0slbmWnkqvbWgQEyw"
chat_id = "596123373"
message = str(datetime.datetime.now())
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # this sends the message