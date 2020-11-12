import threading  # threading is required as alert will halt execution of other notification
import beepy
import webbrowser
import os
import json
import datetime

from settings import *
from sendemail import *


def alert(times=Settings.beep_time):
    for i in range(times):
        beepy.beep(sound=3)


class Notify:

    def __init__(self):
        self.history = {}
        if os.path.exists('history.json'):
            with open('history.json') as f:
                self.history = json.load(f)

    def notify(self, url_list: list):
        now = datetime.datetime.now()
        if Settings.MINIMAL_REALERT_INTERVAL !=-1:
            for url in url_list:
                if url in self.history:
                    last_alerted = datetime.datetime.fromisoformat(self.history[url])
                    time_delta = now - last_alerted
                    if time_delta.total_seconds() / 60 < Settings.MINIMAL_REALERT_INTERVAL:  # already alerted recently
                        print(f'Last alerted {self.history[url]}. Not going to alert again about {url}')
                        url_list.remove(url)
                self.history[url] = datetime.datetime.isoformat(now)
            with open('history.json', 'w') as f:
                json.dump(self.history, f)

        if len(url_list) == 0:  # empty list do nothing
            return

        alert_thread = threading.Thread(target=alert)
        email_thread = []

        if Settings.AUDIO_ALERT:
            alert_thread.start()  # Start audio thread, and while the alarm plays, continue to apply other alerts

        if Settings.OPEN_IN_BROWSER:
            for url in url_list:
                webbrowser.open_new(url)  # open the url in the default browser

        if Settings.EMAIL_ALERT:
            for url in url_list:
                for address in Settings.recipients:
                    email_thread.append(threading.Thread(target=send_an_email, args=(Settings.subject + url,
                                                                                     address,
                                                                                     url,
                                                                                     Settings.html_template.format(
                                                                                         url))))
                    # Send multiple email by calling send email function with multithreading
            for t in email_thread: t.start()  # start all email threads
        if Settings.AUDIO_ALERT:
            alert_thread.join()  # Finally join audio

        for t in email_thread: t.join()  # Join all email threads
