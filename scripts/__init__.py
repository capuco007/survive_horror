import bge
from bge.logic import globalDict as gd

gd['game_status'] = {
        'regarregar':0,
        'agarrado': False,
        'scene_pass': False,
        'scene':'',
        'call_bau':False,
        'shotin_time':0,
        'shotin_time_pistola':40,
        'shotin_time_shotgun':70,
        'shotin_time_metralha':15,
        'shotin_time_faca':5,
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

        'exib_msg': 'none',

        'pos_spw':[],
        'alaing': None,
            
        'player':{
            'pistola_capacity':10,
            'shotgun_capacity':8,
            'metralha_capacity':50,
            'scene':'',
            'saude': 50,
            'arma_mao': 'pistola',
            'bala_pistola': 10,
            'bala_shotgun': 12,
            'bala_metralha': 50,
           
           

        },
        'inventory':[
           

        ],
        'bau':[],
    }