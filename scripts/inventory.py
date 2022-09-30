import bge
from bge.types import *
from collections import OrderedDict
from bge.logic import globalDict as gd
from mathutils import Vector


status: dict = gd['game_status']

def start(cont: SCA_PythonController):
    own = cont.owner
    own['obHit'] = None
    own.setParent(own.groupObject)

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
     
def slots(cont):
    own = cont.owner 
    group = own.groupObject
    lista = status[group['type']]
    items  = lista[group['slot']] if group['slot'] < len(lista) else None
    
    if items:
       own.replaceMesh(status[group['type']][group['slot']]['nome'])

    else:
        own.replaceMesh('vazio')

def recarregar(cont):
    own = cont.owner
    print('Recarregando_Armas')

def usar_item_mover_item(cont):
    own = cont.owner
    scene = own.scene
    Mouse_Over = cont.sensors['Mouse_Over']
    Mouse_Left = cont.sensors['Mouse']
    botao = scene.objects['botao']
    Mouse_Use = cont.sensors['Mouse_Use']

    if status['open_invent']:
        
        if Mouse_Over.positive and Mouse_Left.positive:
            own['obHit'] = Mouse_Over.hitObject.groupObject
            
            if own['obHit']['slot']< len(status[own['obHit']['type']]):

                botao.worldPosition.x = own['obHit'].worldPosition.x
                botao.worldPosition.y = own['obHit'].worldPosition.y - 0.5
           

       
        if own['obHit'] and Mouse_Use.positive and Mouse_Left.positive:
            if own['obHit']['slot']< len(status[own['obHit']['type']]):
                botao.worldPosition = [10,10,1]

                # se o Bau estiver aberto
                if status['open_bau']:
            
                    itemRemovido = itemRemove(own['obHit']['slot'], status[own['obHit']['type']])
                    if own['obHit']['type'] == 'bau':
                        itemAdd(itemRemovido, status['inventory'])
                        own['obHit'] = None
                    else:
                        itemAdd(itemRemovido, status['bau'])
                        own['obHit'] = None
            
                
                # se o Bau estiver fechado
                else:
                    if status['inventory'][own['obHit']['slot']]['tipo'] == 'arma':
                        if status['player']['arma_mao'] != status['inventory'][own['obHit']['slot']]['nome']:
                            status['player']['arma_mao'] = status['inventory'][own['obHit']['slot']]['nome']
                            print(status['player']['arma_mao'],'sim e uma arma')
                        else:
                            recarregar(cont)
                    else:
                        if status['inventory'][own['obHit']['slot']]['tipo'] == 'cura':
                            if status['player']['saude'] < 100:
                                status['player']['saude'] = 100
                                print('Curando')
                                itemRemove(own['obHit']['slot'], status['inventory'])
                            else:
                                print('saude esta no maximo')
                    own['obHit'] = None
            
def update(cont):
    slots(cont)
    usar_item_mover_item(cont)

