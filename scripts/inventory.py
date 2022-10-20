from asyncio import events
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
                valorTotal = invItem['quant'] + item['quant']
                resto = valorTotal - status['max_'+str(invItem['nome'])]
                print(valorTotal,resto)
                if  invItem['quant'] <status['max_'+str(invItem['nome'])]:
                    invItem['quant'] = valorTotal - resto
                if resto >0:
                    item['quant'] = resto
                    collection.append(item)
                    resto = 0
                break
                    
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
    slot_quant = own.childrenRecursive.get('slot_quant')
    if items:
        slot_quant.visible = True
        own.replaceMesh(status[group['type']][group['slot']]['nome'])

        

        if items['tipo'] == 'arma':
            slot_quant['quant'] = status['player']['bala_' + items['nome']]

        else:
            if 'quant' in items:
                slot_quant['quant'] = items['quant']
            else:
                slot_quant['quant'] = 0
                slot_quant.visible = False

    



    else:
        slot_quant.visible = False
        slot_quant['quant'] = 0
        own.replaceMesh('vazio')

def recarregar(cont):
    own = cont.owner
    arma = status['player']['arma_mao']
    list_Balas = []
    for item in status['inventory']:
        if item['nome'] == 'bala_'+arma:
            list_Balas.append(item)
    import functools
    list_Balas = sorted(list_Balas,key=functools.cmp_to_key(lambda item1,item2:item1['quant']-item2['quant']))
    
    
    for balas in list_Balas:
        bala_recarga = status['player'][arma+'_capacity'] - status['player']['bala_'+arma]
        if bala_recarga == 0:
            break

        if balas['quant'] < bala_recarga:
            status['player']['bala_'+arma] += balas['quant']
            balas['quant'] = 0
        elif balas['quant']>= bala_recarga:
            balas['quant'] -= bala_recarga
            status['player']['bala_'+arma] += bala_recarga
        if balas['quant'] == 0:
            itemRemove(status['inventory'].index(balas), status['inventory'])

def usar_item_mover_item(cont):
    own = cont.owner
    scene = own.scene
    Mouse_Over = cont.sensors['Mouse_Over']
    Mouse_Left = cont.sensors['Mouse']
    botao = scene.objects['botao']
    Mouse_Use = cont.sensors['Mouse_Use']

    if status['open_invent'] or status['open_bau']:
        
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
                        print(itemRemovido)
                        own['obHit'] = None
                        if itemRemovido['nome'] == status['player']['arma_mao']:
                            status['player']['arma_mao'] = ''
                        

                    
            
                
                # se o Bau estiver fechado
                else:
                    if status['inventory'][own['obHit']['slot']]['tipo'] == 'arma':
                        if status['player']['arma_mao'] != status['inventory'][own['obHit']['slot']]['nome']:
                            status['player']['arma_mao'] = status['inventory'][own['obHit']['slot']]['nome']
                            print(status['player']['arma_mao'],'sim e uma arma')
                        else:
                            recarregar(cont)

                                    

                    elif status['inventory'][own['obHit']['slot']]['tipo'] == 'cura':
                        if status['player']['saude'] < 100:
                            status['player']['saude'] = 100
                            print('Curando',status['player']['saude'])
                            itemRemove(own['obHit']['slot'], status['inventory'])
                        else:
                            print('saude esta no maximo')
                    own['obHit'] = None

def abrir_inventario_bau(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    scene = own.scene
    bau = scene.objects['bau']
    inventory = scene.objects['inventory']
    fading = scene.objects['fading']
    actF = fading.getActionFrame()
    bau_open = status['open_bau']
    open_invent = status['open_invent']
    coll_bau = status['call_bau']
    listScene = bge.logic.getSceneList()
   
   

    

    if coll_bau:
        if bau_open == False and tc[bge.events.SPACEKEY].activated:
            if actF == 0:
                status['open_bau'] = True
                fading.playAction('fadingAction',0,12,play_mode = 0)
                if '_game_test' in listScene:
                    print(listScene)
                    listScene['_game_test'].suspend()
        if bau_open == True and tc[bge.events.SPACEKEY].activated:
            if actF == 12:
                status['open_bau'] = False
                fading.playAction('fadingAction',12,0,play_mode = 0)
                if '_game_test' in listScene:
                    listScene['_game_test'].resume()
        if actF >= 7:
            bau.worldPosition.x = 0
        if actF <= 7:
            bau.worldPosition.x = -17

    else:
        if open_invent == False and tc[bge.events.QKEY].activated:
            if actF == 0:
                status['open_invent']= True
                fading.playAction('fadingAction',0,12,play_mode = 0)
                if '_game_test' in listScene:
                    print(listScene)
                    listScene['_game_test'].suspend()

        if open_invent == True and tc[bge.events.QKEY].activated:
            if actF == 12:
                status['open_invent'] = False
                fading.playAction('fadingAction',12,0,play_mode = 0)
                if '_game_test' in listScene:
                    listScene['_game_test'].resume()

        if actF >= 7:
            inventory.worldPosition.x = 1.4
        if actF <= 7:
            inventory.worldPosition.x = 8.5
    if status['fading'] >0:
        status['fading'] -=1
            

    if status['fading'] <-0:
        status['fading'] +=1

def update(cont):
    slots(cont)
    own = cont.owner
    usar_item_mover_item(cont)
    abrir_inventario_bau(cont)
    scene = own.scene
    tc = bge.logic.keyboard.inputs
    if tc[bge.events.RKEY].activated:
        recarregar(cont)
    


