import bge
from bge.logic import globalDict as gd

gd['game_status'] = {
        'openclosebau':False,
        'open_invent': False,

        'exib_msg': 'none',

        'pos_spw':[],
            
        'player':{
            'scene':'',
            'life': 90,
            'gun': '',
            'M_pistola': 10,
            'M_shotgun': 0,
            'M_bazuka': 0,
            'Global_Municao': 0
        },
        'inventory':{

        },
        'bau':{
            
        },

    }