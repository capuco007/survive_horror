import bge
from bge.logic import globalDict as gd

gd['game_status'] = {
        'reloadTime':0,
        'index':0,
        'reload': False,
        'clic':0,
        'select_item': None,
        'openclosebau':False,
        'open_invent': False,

        'exib_msg': 'none',

        'pos_spw':[],
            
        'player':{
            'pistola_capacity':10,
            'shotgun_capacity':8,
            'metralha_capacity':50,
            'scene':'',
            'life': 90,
            'gun': '',
            'bala_pistola': 0,
            'bala_shotgun': 0,
            'bala_metralha': 0,
            'Global_Municao': 0

        },
        'inventory':[

        ],
        'bau':[],
        'slot_conf':[]
    }