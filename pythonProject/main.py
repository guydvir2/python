import time
import datetime
import subprocess

import smtplib, ssl

port = 465
password = "GdSd13100301!"

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("guydvir.tech@gmail.com", password)
    # TODO: Send email here


def exec_sh_file(file):
    subprocess.run(file)


def return_datestamp():
    clk = datetime.datetime.now().ctime()
    return clk


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time.sleep(1)
    print(return_datestamp())
    # exec_sh_file("/home/guy/run_vmBox_raspbian.sh")
