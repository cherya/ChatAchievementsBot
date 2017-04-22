from bot import run_bot_loop
import updater
import time

UPDATE_TIMEOUT = 5


def run_forver():
    run_bot_loop()
    print('forver update...')
    while True:
        print('lol')
        updater.update()
        time.sleep(UPDATE_TIMEOUT)

run_forver()
