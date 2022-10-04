import bge
from bge.logic import globalDict as gd

gd['game_status'] = {
        'call_bau':False,
        'shotin_time':0,
        'reload_time':0,
        'reload': False,
        'open_bau':False,
        'open_invent': False,
        'max_bala_pistola': 30,
        'max_bala_shtogun': 20,
        'max_bala_metralha': 50,
        'fading':0,

        'exib_msg': 'none',

        'pos_spw':[],
            
        'player':{
            'pistola_capacity':10,
            'shotgun_capacity':8,
            'metralha_capacity':50,
            'scene':'',
            'saude': 90,
            'arma_mao': '',
            'bala_pistola': 0,
            'bala_shotgun': 0,
            'bala_metralha': 0,
           
           

        },
        'inventory':[
           

        ],
        'bau':[],
    }