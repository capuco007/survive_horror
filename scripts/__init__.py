import bge
from bge.logic import globalDict as gd

gd['game_status'] = {
        'shotin_time':0,
        'reload_time':0,
        'reload': False,
        'open_bau':True,
        'open_invent': True,

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
            {'nome':'metralha','tipo':'arma'},
            {'nome':'pistola','tipo':'arma'},
            {'nome':'key_0','tipo':'key'},
            {'nome':'med_kit','tipo':'cura'}

        ],
        'bau':[],
    }