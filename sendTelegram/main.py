import requests
import datetime
import pywhatkit

chatID = '596123373'
BOT_TOKEN_1 = "812406965:AAEaV-ONCIru8ePuisuMfm0ECygsm5adZHs"  # botbot
BOT_TOKEN_2 = "497268459:AAESYm27tJfNXwnnnn0slbmWnkqvbWgQEyw"  # homepi_bot
BOT_TOKEN_3 = "1238925698:AAGWARuQ2eyx2i0ui2sCp_mM7xInTsKgUuM"  # guyd_test2bot

tokens = [BOT_TOKEN_1, BOT_TOKEN_2, BOT_TOKEN_3]


def send_to_telegram(message):
    apiURL = f'https://api.telegram.org/bot{tokens[2]}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


send_to_telegram(datetime.datetime.now().ctime())
pywhatkit.sendwhatmsg("+972-524291167", "hi", 21, 36)
