from bot.bot import run_bot_loop
from bot.updater import update
import time

UPDATE_TIMEOUT = 1

if __name__ == '__main__':
    run_bot_loop()

    while True:
        update()
        time.sleep(UPDATE_TIMEOUT)
