import bge
from bge.types import *
from bge.logic import globalDict as gd

def start(cont: SCA_PythonController):
    own = cont.owner
    aplicar_props(own)
    

def aplicar_props(own):
    group = own.groupObject
    item_db = gd['database']['items'].get(own.get('nome'))
    if item_db:
        for key in item_db.keys():
            if not key in own:
                own[key] = item_db[key]
    mesh = group.get('mesh')
    if mesh:
        own.replaceMesh(mesh)