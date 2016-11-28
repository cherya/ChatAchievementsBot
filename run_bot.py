from bot.bot import run_bot
import json

config = json.load(open('config.json', encoding='utf-8'))

if __name__ == '__main__':
    run_bot(config['token'])
