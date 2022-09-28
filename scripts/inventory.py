import bge
from bge.types import *
from collections import OrderedDict
from bge.logic import globalDict as gd
from mathutils import Vector

from symbol import argument

status: dict = gd['game_status']

def itemExists(item, collection):
    # type: (dict, list[dict]) -> bool
    """Verifica se o item passado no parâmetro existe na coleção."""
    for invItem in collection:
        if item.get('nome') == invItem.get('nome'):
            return True
    return False

def itemAdd(item, collection):
    # type: (dict, list[dict]) -> None
    """Adiciona item na coleção."""

    # Adiciona na coleção caso item não exista ou não seja agrupável
    if not itemExists(item,collection) or not item.get('quant'):
        collection.append(item)

    # Adiciona quantidade de item agrupável no item existente
    elif item.get('quant'):
        for invItem in collection:
            if item.get('nome') == invItem.get('nome'):
                invItem['quant'] += item['quant']

def itemRemove(idx, collection) -> dict:
    # type: (int, list[dict]) -> dict
    """Remove item da coleção a partir do índice e retorna este item."""
    if idx < len(collection):
        return collection.pop(idx)

def start(cont: SCA_PythonController):
    own = cont.owner
    own['select'] = False
    own['i'] = None
    own['openInvent'] = 0
    own['item'] = None
    own['reloadTime'] = 0
       
def item_slot(cont):
    own = cont.owner
    update(cont)
    
    posZero = Vector([10,10,1])
    scene = own.scene
    m_over = cont.sensors['m_over']
    group = own.groupObject
    lista = status[group['type']]
    ms = bge.logic.mouse.inputs
    tc = bge.logic.keyboard.inputs
    buttom = scene.objects['buttom']
    b_usar = cont.sensors['usar']
    b_mover = cont.sensors['mover']
    b_descart = cont.sensors['descart']
    usar =scene.objects['usar']
    mover  = scene.objects['mover']
    descart = scene.objects['descart']
    quant = own.childrenRecursive.get('quant')
    items  = lista[group['slot']] if group['slot'] < len(lista) else None
    
    if items:
        if 'quant' in items:
            print('ok')
            quant['quant'] = str(items['quant'])
            if items['quant'] <=0:
               
                itemRemove(group['slot'], status['inventory'])
                quant.visible =False
        else:
            quant['quant'] = ''

        if 'gun' in items:
                quant['quant'] = status['player']['bala_' +str(items['nome'])]
                
    else:
        quant['quant'] = ''

    if status['open_invent']:
        for o in scene.objects:
            o.visible = True
        if items:
            if m_over.positive:
                o = m_over.hitObject.groupObject
                oPosX = o.worldPosition.x
                oPosY = o.worldPosition.y
                totalPos = Vector([oPosX - 0.8,oPosY-1.5,1]) 
                if ms[bge.events.LEFTMOUSE].activated:
                    usar.worldPosition = totalPos
                    own['i'] = o
                
         # ultilizando items do inventario
        if own['i']:
            o = own['i']
            if b_usar.positive:
                if  ms[bge.events.LEFTMOUSE].activated:
                    if not status['openclosebau']:
                        if o['type'] == "inventory":
                            usar.worldPosition = [10,10,1]
                            own['i'] = None
                           

                            if 'gun' in status['inventory'][o['slot']]:
                                i = status['inventory'][o['slot']]     
                                status['player']['gun'] = i['nome']
                            
                                if status['player']['gun'] == i['nome'] and status['reloadTime'] == 0:
                                    status['reload'] = True
                                    for ob in scene.objects:
                                        if 'slot' in ob:
                                            if ob['slot'] < len(status['inventory']):
                                               if status['inventory'][ob['slot']]['nome'] == 'bala_'+str(i['nome']):
                                                   status['index'] = ob['slot']
                                                

                            if 'key' in status['inventory'] [o['slot']]:
                                
                                print('uma key')

                            if 'cura' in status['inventory'] [o['slot']]:
                                
                                print('curou')

                           
                            
                            #####################################################


                    if  status['openclosebau']:
                        if o['type'] == "inventory":
                            itemRem = itemRemove(own['i']['slot'], status['inventory'])
                            if itemRem['nome'] == status['player']['gun']:
                                status['player']['gun'] = ''
                                
                            itemAdd(itemRem, status['bau'])
                            usar.worldPosition = [10,10,1]
                        if o['type'] == "bau":
                            itemRem = itemRemove(own['i']['slot'], status['bau'])
                            itemAdd(itemRem, status['inventory'])
                            usar.worldPosition = [10,10,1]
                        

        # Mostrar item no slot##
        if items:
            
            own.replaceMesh(items['mesh'])
            
        
        else:
            pass
            own.replaceMesh('vazio') # Mostrar slot vazio #
    else:
        for o in scene.objects:
            o.visible = False
    
    if not status['openclosebau']:
        pass
        
def update(cont):
    
    if status['reloadTime'] >0:
        status['reloadTime'] -=1
    if status['clic'] >0:
        status['clic'] -= 1
    own = cont.owner
    scene = own.scene
    tc = bge.logic.keyboard.inputs
    if status['reload']:
        reload(cont)
   
def reload(cont):
    
    own = cont.owner
    capacity_pistola = 10
    capacity_shotgun = 8
    capacity_metralha = 50
    arma = status['player']['gun']
    scene = own.scene
    
    
    if arma != '':
        if status['player']['bala_'+str(arma)] < status['player'][str(arma)+ '_capacity']:
            balas_inv = status['inventory'][status['index']]['quant']
            if status['inventory'][status['index']]['quant'] >0:
                status['player']['bala_'+str(arma)] += 1
                status['inventory'][status['index']]['quant'] -= 1
