import datetime
import os
import json
import threading  # threading is required as alert will halt execution of other notification
import webbrowser

import beepy

from sendemail import *


def alert(times):
    for i in range(times):
        beepy.beep(sound=3)


class Notify:

    def __init__(self, settings: dict):
        self.history = {}
        self.settings = settings
        self.json_error = False
        self.recipients = []
        self.html_template = '{0}'

        if os.path.exists('recipient_emails.json'):
            with open('recipient_emails.json', 'r') as f:
                self.recipients = json.load(f)
        elif self.settings['email_alert']:
            raise Exception('EMAIL ALERTS ARE ENABLED YET MISSING recipient_emails.json')

        if os.path.exists('email_template.html'):
            with open('email_template.html', 'r') as f:
                self.html_template = f.read().replace("\n", "")
        else:
            print('MISSING HTML TEMPLATE, CONTINUING WITH NO HTML BODY')

        try:
            if os.path.exists('history.json'):
                with open('history.json') as f:
                    self.history = json.load(f)
        except Exception as e:
            self.json_error = True
            print(f'Failed to load JSON. Likely IO/Permission errors. History and re-alert interval features will be '
                  f'disabled. Error: {e}. If you want to re-enable such features, resolve the error and relaunch')

    def notify(self, url_list: list):
        now = datetime.datetime.now()
        if self.settings['minimal_re_alert_interval'] != -1 and not self.json_error:
            for url in url_list:
                if url in self.history:
                    last_alerted = datetime.datetime.fromisoformat(self.history[url])
                    time_delta = now - last_alerted
                    if time_delta.total_seconds() / 60 < self.settings['minimal_re_alert_interval']:
                        # already alerted recently
                        print(f'Last alerted {self.history[url]}. Not going to alert again about {url}')
                        url_list.remove(url)
                    else:
                        # if we haven't alert recently, alert
                        # and update time
                        self.history[url] = datetime.datetime.isoformat(now)
                else:
                    # First time alerting, store in history
                    self.history[url] = datetime.datetime.isoformat(now)
            try:
                with open('history.json', 'w') as f:
                    json.dump(self.history, f, indent=4)
            except Exception as e:
                self.json_error = True
                print(
                    f'Failed to dump JSON. Likely IO/Permission errors. History and re-alert interval features will be '
                    f'disabled. Error: {e}. If you want to re-enable such features, resolve the error and relaunch')

        if len(url_list) == 0:  # empty list do nothing
            return

        alert_thread = threading.Thread(target=alert, args=(self.settings['audio_beeps'],))
        email_thread = []

        if self.settings['audio_alert']:
            alert_thread.start()  # Start audio thread, and while the alarm plays, continue to apply other alerts

        if self.settings['open_in_browser']:
            for url in url_list:
                webbrowser.open_new(url)  # open the url in the default browser

        if self.settings['email_alert']:
            for url in url_list:
                for address in self.recipients:
                    email_thread.append(
                        threading.Thread(target=send_an_email,
                                         args=(self.settings, self.settings['email_subject'] + url,
                                               address,
                                               url,
                                               self.html_template.format(
                                                   url))))
                    # Send multiple email by calling send email function with multithreading
            for t in email_thread: t.start()  # start all email threads

        if self.settings['audio_alert']:
            alert_thread.join()  # Finally join audio

        for t in email_thread: t.join()  # Join all email threads

# Debug
# if __name__ == '__main__':
#     with open('config.json', 'r') as f:
#         settings = json.load(f)
#     notify = Notify(settings)
#     notify.notify(['google.com'])
