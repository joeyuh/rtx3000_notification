import time
import requests
import faker
from multiprocessing import Process, Value, Lock, Manager

from settings import *
from notify import *
from detect import *

if __name__ == "__main__":
    with Manager() as manager:
        while True:  # Yes, while true
            total_url_count = Settings.bestbuty_url_bank + Settings.amazon_url_bank
            start_time = time.time()
            v = Value('i', 0)  # success count
            l = manager.list()
            lock = Lock()
            best_buy_procs = [Process(target=bestbuy_detect, args=(url, v, l, lock)) for url in
                              Settings.bestbuty_url_bank]
            amazon_procs = [Process(target=amazon_detect, args=(url, v, l, lock)) for url in Settings.amazon_url_bank]
            for p in best_buy_procs: p.start()
            for p in amazon_procs: p.start()
            for p in best_buy_procs: p.join()
            for p in amazon_procs: p.join()
            if v.value == 0:
                print(f'Detection of all the URL has failed. Sleeping for {Settings.UNKNOWN_ERROR_RETRY} seconds!')
                print('Maybe check your Internet connection!')
                time.sleep(Settings.UNKNOWN_ERROR_RETRY)
            else:
                print(f'Went through all URLS in {time.time() - start_time} seconds, '
                      f'{v.value} Success, {len(total_url_count) - v.value} Failed')
                print("Links:")
                print(l)
                notify(l)
            print(f'Sleeping {Settings.BETWEEN_ROUNDS} seconds')
            time.sleep(Settings.BETWEEN_ROUNDS)
