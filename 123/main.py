import os
import datetime
import requests
from sys import platform
import paho.mqtt.publish as mqtt_pub
import paho.mqtt.client as mqtt_client

# MQTT Server
mqtt_port = 1883
mqtt_connected: bool = False
mqtt_broker = "192.168.2.100"
mqtt_client_name = "MQTT_Supervisor"
mqtt_credits = {"username": "guy", "password": "kupelu9e"}
client: mqtt_client
# ~~~~~~~~~~~~~~

# Topics Subscribe:
subsTopics = ["myHome/Lights/#", "myHome/Windows/#", "myHome/Conts/#",
              "myHome/alarmMonitor/#", "myHome/WaterBoiler/#", "myHome/Messages", "myHome/log"]
# ~~~~~~~~~~~~~~

# Telegram
CHAT_ID = "596123373"
BOT_TOKEN = "812406965:AAEaV-ONCIru8ePuisuMfm0ECygsm5adZHs"
# define BOT_TOKEN_2 "497268459:AAESYm27tJfNXwnnnn0slbmWnkqvbWgQEyw" //homepi_bot
# define BOT_TOKEN_3 "1238925698:AAGWARuQ2eyx2i0ui2sCp_mM7xInTsKgUuM" //guyd_test2bot
# ~~~~~~~~~~~~~~


# log file
FILE_EXT = 'log'
MAX_FILE_SIZE = 10 ** 6
PATH = '/mqttlogs/'
LOG_FILENAME_PREFIX = ['lights', 'win', 'conts', 'alarm', "boiler", "msg", "log"]
filename: str = "filename"
filename_suffix_counter = [0, 0, 0, 0, 0, 0, 0]


# ~~~~~~~~~~~~~~
def set_log_save_directory():
    global PATH
    username = os.getlogin()

    if platform == "linux" or platform == "linux2":
        PATH = '/home/' + username + PATH
    elif platform == "darwin":
        PATH = '/Users/' + username + PATH
    # elif platform == "win32":
    #     yield
    # Windows...
    else:
        print("Fail to set path - unidentified OS")
        quit()


def send_msg_telegram(message):
    apiURL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': CHAT_ID, 'text': message})
        print(str(response.json()["ok"]) == "True")
    except Exception as e:
        print(e)


def construct_filename(file_index):
    global filename
    filename = PATH + str(LOG_FILENAME_PREFIX[file_index]) + "_" + str(
        filename_suffix_counter[file_index]) + '.' + FILE_EXT


def update_filename(file_index):
    global filename
    global filename_suffix_counter

    construct_filename(file_index)
    while os.path.exists(filename) and get_filesize(filename) > MAX_FILE_SIZE:
        filename_suffix_counter[file_index] += 1
        construct_filename(file_index)


def get_filesize(file=filename):
    if os.path.exists(file):
        file_stats = os.stat(file)
        return file_stats.st_size
    else:
        return 0


def write2file(line, use_timestamp=False, newLine=True, file_index=0):
    if newLine:
        line = line + "\n"
        update_filename(file_index)
    with open(filename, 'a') as f:
        if not use_timestamp:
            f.write(line)
        else:
            f.write(msg_w_timestamp(line))


def on_connect(client, userdata, flags, rc):
    _str = f"Connection to MQTT server {mqtt_broker}"
    if rc == 0:
        print(_str + " succeeded")
    else:
        print(_str + f" failed. Result code {rc}")

    for _topic in subsTopics:
        client.subscribe(_topic)
        print(f"\tsubscribed: {_topic}")


def on_message(client, userdata, msg):
    _str = "[" + str(msg.topic) + "] -->" + str(msg.payload, "UTF-8")

    # This part is for going on/offline
    if check_avail_change(msg.topic):
        if "offline" in str(msg.payload):
            device_goes_offline_cb(msg.topic)
        else:
            device_goes_online_cb(msg.topic)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    i = 0
    for topic in subsTopics:
        if topic[-1] == "#":
            if topic[:-2] in msg.topic:
                break
        else:
            if topic in msg.topic:
                break
        i += 1

    if i < len(subsTopics):
        write2file(_str, True, True, i)


def connect_mqtt_server():
    global client
    global mqtt_connected
    client = mqtt_client.Client(mqtt_client_name)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(mqtt_credits["username"], mqtt_credits["password"])
    client.connect(mqtt_broker, mqtt_port)
    mqtt_connected = client.is_connected()


def loop_mqtt():
    client.loop()


def check_avail_change(msg):
    if "Avail" in str(msg):
        return True
    else:
        return False


def device_goes_offline_cb(topic):
    minimsg = msg_w_timestamp(f"{topic} is offline")
    print(minimsg)
    send_msg_telegram(minimsg)


def device_goes_online_cb(topic):
    # print(msg_w_timestamp(f"{topic} is online"))
    yield


def msg_w_timestamp(msg):
    _msg = "[" + get_clk() + "]" + msg
    return _msg


def get_clk():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def all_loop():
    while True:
        try:
            loop_mqtt()
        except KeyboardInterrupt:
            print("Forced exit")
            quit()


def wakeup_msg():
    for i, log in enumerate(LOG_FILENAME_PREFIX, start=0):
        timestamp_len = 21
        update_filename(i)
        _str0 = msg_w_timestamp(
            f" ~~ Subscribe: {subsTopics[i]} ~~ file size "
            f"{get_filesize(filename) / 1000}[kb] / {MAX_FILE_SIZE / 1000}[kb]")
        _str = "\n" + _str0 + "\n" + " " * timestamp_len + "~" * (len(_str0) - timestamp_len)
        write2file(_str, False, True, i)

    mqtt_pub.single("myHome/log", msg_w_timestamp(f" [{mqtt_client_name}][Boot]"), hostname=mqtt_broker,
                    auth=mqtt_credits, client_id=mqtt_client_name)

    send_msg_telegram(msg_w_timestamp(f" [{mqtt_client_name}][Boot]"))


if __name__ == "__main__":
    set_log_save_directory()
    wakeup_msg()
    connect_mqtt_server()
    all_loop()
