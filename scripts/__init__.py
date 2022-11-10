from importlib.resources import path
import json
import bge
from bge.logic import globalDict as gd

gd['database'] = {}

gd['game_status'] = {
        'afast':False,
        'index_enemy':0,
        'list_enemyes':[],
        'descri_item':'',
        'add_most_item':'',
        'most_item':0,
        'tempo_morte':0,
        'soltar':0,
        'atacando':0,
        'regarregar':0,
        'agarrado': False,
        'scene_pass': False,
        'scene':'',
        'call_bau':False,
        'shotin_time':0,
        'shotin_time_pistola':40,
        'shotin_time_shotgun':70,
        'shotin_time_metralha':15,
        'shotin_time_faca':50,
        'reload_time':0,
        'reload': False,
        'open_bau':False,
        'open_invent': False,
        'max_bala_pistola': 30,
        'max_bala_shtogun': 20,
        'max_bala_metralha': 50,
        'fading':0,
        'potencia_pistola': 10,
        'potencia_metralha': 15,
        'potencia_shotgun': 30,
        'potencia_faca': 5,

        'exib_msg': 'none',

        'pos_spw':[],
        'alaing': None,
            
        'player':{
            'pistola_capacity':10,
            'shotgun_capacity':12,
            'metralha_capacity':50,
            'scene':'',
            'saude': 100,
            'arma_mao': 'faca',
            'bala_pistola': 10,
            'bala_shotgun': 12,
            'bala_metralha': 50,
           
           

        },
        'inventory':[
           

        ],
        'bau':[],
    }

def carregar_database():
    from pathlib import Path
    from bge.logic import expandPath
    from json import loads
    path = Path(expandPath('//database')).resolve()
    for f in path.iterdir():
        if f.suffix == '.json':
            data = loads(f.open(mode='r',encoding='utf-8').read())
            gd['database'][f.stem] = data
            print('carregou o arquivo',f)

carregar_database()