import json
import multiprocessing
from multiprocessing import Process, Value, Lock, Manager, Semaphore

import discord_bot
from detect import *
from notify import *

if __name__ == "__main__":
    with Manager() as manager:

        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                settings = json.load(f)
        else:
            raise Exception('MISSING config.json')

        notify = Notify(settings)

        bestbuy_url_bank = []
        amazon_url_bank = []
        newegg_url_bank = []

        if os.path.exists('bestbuy_url.json'):
            with open('bestbuy_url.json', 'r') as f:
                bestbuy_url_bank = json.load(f)
        if os.path.exists('amazon_url.json'):
            with open('amazon_url.json', 'r') as f:
                amazon_url_bank = json.load(f)
        if os.path.exists('newegg_url.json'):
            with open('newegg_url.json', 'r') as f:
                newegg_url_bank = json.load(f)

        total_url_count = len(bestbuy_url_bank) + len(amazon_url_bank) + len(newegg_url_bank)
        if not total_url_count:
            raise Exception('MISSING ALL URLS, PLEASE ADD AT LEAST ONE JSON FILE')

        if settings['discord']:
            print("Starting discord thread")
            discord_proc = Process(target=discord_bot.main)
            discord_proc.start()

        newegg_last = datetime.datetime.now() - datetime.timedelta(days=1)
        amazon_last = datetime.datetime.now() - datetime.timedelta(days=1)

        sema = Semaphore(int(multiprocessing.cpu_count()*1.5))
        lock = Lock()
        while True:  # Yes, while true
            start_time = time.time()
            v = Value('i', 0)  # success count
            l = manager.list()

            best_buy_procs = [Process(target=bestbuy_detect, args=(v, l, lock, settings, sema, notify,  url)) for url in
                              bestbuy_url_bank]
            newegg_procs = []
            wait = datetime.datetime.now() - newegg_last
            if wait.total_seconds() > settings['newegg_cooldown_delay'] or \
                    (not settings['newegg_cooldown']):
                newegg_procs = [Process(target=newegg_detect, args=(v, l, lock, settings, sema, notify, url)) for url in
                                newegg_url_bank]
                newegg_last = datetime.datetime.now()
            else:
                print('Skipping newegg for cooldown')

            wait = datetime.datetime.now() - amazon_last
            amazon_procs = []
            if wait.total_seconds() > settings['amazon_cooldown_delay'] or \
                    (not settings['amazon_cooldown']):
                amazon_procs = [Process(target=amazon_detect, args=(v, l, lock, settings, sema, notify, url)) for url in
                                amazon_url_bank]
                amazon_last = datetime.datetime.now()
            else:
                print('Skipping amazon for cooldown')

            all_procs = best_buy_procs + amazon_procs + newegg_procs
            total_count = len(all_procs)

            for proc in all_procs:
                sema.acquire()
                proc.start()

            for proc in all_procs:
                proc.join()

            if v.value == 0:
                print(
                    f'Detection of all the URL has failed. Sleeping for {settings["unknown_error_retry_delay"]} seconds!')
                print('Maybe check your Internet connection!')
                time.sleep(settings["unknown_error_retry_delay"])
            else:
                print(f'Went through all URLS in {time.time() - start_time} seconds, '
                      f'{v.value} Success, {total_count - v.value} Failed')
                print("Links:")
                print(l)


            print(f'Sleeping {settings["between_rounds_delay"]} seconds')
            time.sleep(settings["between_rounds_delay"])
