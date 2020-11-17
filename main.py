import json
from multiprocessing import Process, Value, Lock, Manager

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

        print("Starting discord thread")
        discord_proc = Process(target=discord_bot.main)
        discord_proc.start()

        while True:  # Yes, while true
            start_time = time.time()
            v = Value('i', 0)  # success count
            l = manager.list()
            lock = Lock()

            best_buy_procs = [Process(target=bestbuy_detect, args=(url, v, l, lock, settings)) for url in
                              bestbuy_url_bank]
            amazon_procs = [Process(target=amazon_detect, args=(url, v, l, lock, settings)) for url in amazon_url_bank]
            newegg_procs = [Process(target=newegg_detect, args=(url, v, l, lock, settings)) for url in newegg_url_bank]

            for p in best_buy_procs: p.start()
            for p in amazon_procs: p.start()
            for p in newegg_procs: p.start()

            for p in best_buy_procs: p.join()
            for p in amazon_procs: p.join()
            for p in newegg_procs: p.join()

            if v.value == 0:
                print(
                 f'Detection of all the URL has failed. Sleeping for {settings["unknown_error_retry_delay"]} seconds!')
                print('Maybe check your Internet connection!')
                time.sleep(settings["unknown_error_retry_delay"])
            else:
                print(f'Went through all URLS in {time.time() - start_time} seconds, '
                      f'{v.value} Success, {total_url_count - v.value} Failed')
                print("Links:")
                print(l)
                notify.notify(l)

            print(f'Sleeping {settings["between_rounds_delay"]} seconds')
            time.sleep(settings["between_rounds_delay"])
