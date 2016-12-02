import json
import os
dir_name = os.path.dirname(os.path.abspath(__file__))

config = json.load(open(dir_name + '/config.json', encoding='utf-8'))

__all__ = ['config']
