import threading  # threading is required as alert will halt execution of other notification
import beepy
import webbrowser

from settings import *
from sendemail import *


def alert(times=Settings.beep_time):
    for i in range(times):
        beepy.beep(sound=3)


def notify(url_list):
    alert_thread = threading.Thread(target=alert)
    email_thread = []

    if Settings.AUDIO_ALERT:
        alert_thread.start()

    if Settings.OPEN_IN_BROWSER:
        for url in url_list:
            webbrowser.open_new(url)

    if Settings.EMAIL_ALERT:
        for url in url_list:
            for address in Settings.recipients:
                email_thread.append(threading.Thread(target=send_an_email, args=(Settings.subject,
                                                                                 address,
                                                                                 url,
                                                                                 Settings.html_template.format(url))))
        for t in email_thread: t.start()

    alert_thread.join()  # Finally join
    for t in email_thread: t.join()


if __name__ == "__main__":
    notify(["google.com"])
