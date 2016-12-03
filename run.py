from bot.bot import run_bot_loop
from bot.updater import update
from web.server import app

import sys
import time

UPDATE_TIMEOUT = 5

if __name__ == '__main__':

    if '--bot' in sys.argv:
        run_bot_loop()

        while True:
            update()
            time.sleep(UPDATE_TIMEOUT)

    if '--server' in sys.argv:
        app.run()
