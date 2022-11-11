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
            #status['regarregar'] = 200
            status['player']['bala_'+arma] += balas['quant']
            balas['quant'] = 0
            status['regarregar'] = 130
        elif balas['quant']>= bala_recarga:
            status['regarregar'] = 130
            balas['quant'] -= bala_recarga
            status['player']['bala_'+arma] += bala_recarga
        elif balas['quant']<= bala_recarga:
            print('no_bala')
        if balas['quant'] == 0:
            bge.logic.sendMessage('no_bala')
            
            itemRemove(status['inventory'].index(balas), status['inventory'])

def usar_item_mover_item(cont):
    own = cont.owner
    scene = own.scene
    Mouse_Over = cont.sensors['Mouse_Over']
    #Mouse_Over_Equip = cont.sensors['Mouse_Over_equip']
    Mouse_Left = cont.sensors['Mouse']
    botao = scene.objects['botao']
    botao_equip = scene.objects['botao_equip']
    botao_Reload = scene.objects['botao_Reload']
    Mouse_Use = cont.sensors['Mouse_Use']
    Mouse_Use_Equip = cont.sensors['Mouse_Use_Equip']
    Mouse_Realod = cont.sensors['Mouse_Realod']
    if Mouse_Left.positive:
        if Mouse_Realod.positive:
            recarregar(cont)
            status['regarregar'] = 20
            botao_Reload.worldPosition = [10,10,1]
            botao_equip.worldPosition = [10,10,1]
            botao.worldPosition = [10,10,1]

        if Mouse_Use_Equip.positive:
            status['player']['arma_mao'] = ''
            botao_equip.worldPosition = [10,10,1]
            botao_Reload.worldPosition = [10,10,1]
            botao.worldPosition = [10,10,1]


    if not status['open_invent'] and not status['open_bau']:
        botao.worldPosition = [10,10,1]
        botao_equip.worldPosition = [10,10,1]
        botao_Reload.worldPosition = [10,10,1]

    if status['open_invent'] or status['open_bau']:
        
        if Mouse_Over.positive and Mouse_Left.positive:
            own['obHit'] = Mouse_Over.hitObject.groupObject

            arma_nome = status['inventory'][own['obHit']['slot']]['nome']
            arm_mao = status['player']['arma_mao']

            if status['player']['arma_mao'] == arma_nome:
                botao_equip.worldPosition.x = own['obHit'].worldPosition.x
                botao_equip.worldPosition.y = own['obHit'].worldPosition.y - 0.5
                botao.worldPosition = [10,10,1]
                if arm_mao != 'faca':
                    botao_Reload.worldPosition.x = own['obHit'].worldPosition.x
                    botao_Reload.worldPosition.y = own['obHit'].worldPosition.y - 1.0
            else:
                item = status['inventory'][own['obHit']['slot']]['tipo']
                if item !='municao':
                    if own['obHit']['slot']< len(status[own['obHit']['type']]):

                        botao.worldPosition.x = own['obHit'].worldPosition.x
                        botao.worldPosition.y = own['obHit'].worldPosition.y - 0.5
                        botao_equip.worldPosition = [10,10,1]
                else:
                    botao.worldPosition = [10,10,1]
                    botao_equip.worldPosition = [10,10,1]

                
           

       
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
                        if itemRemovido['nome'] == status['player']['arma_mao']:
                            status['player']['arma_mao'] = ''
                        

                    
            
                
                # se o Bau estiver fechado
                else:
                    arma = status['inventory'][own['obHit']['slot']]['tipo']
                    arma_nome = status['inventory'][own['obHit']['slot']]['nome']
                    if arma == 'arma' and arma_nome !=  'faca':
                        if status['player']['arma_mao'] != status['inventory'][own['obHit']['slot']]['nome']:
                            status['player']['arma_mao'] = status['inventory'][own['obHit']['slot']]['nome']
                            print(status['player']['arma_mao'],'sim e uma arma')
                        else:
                            arm_mao = status['player']['arma_mao']
                            if status['player']['bala_'+ arm_mao] < status['player'][arm_mao+'_capacity']:
                                pass
                                #recarregar(cont)
                                #status['regarregar'] = 20
                            else:
                                print('FULL')
                                #status['player']['arma_mao'] = ''

                                    

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
   
   

    if status['player']['saude'] >0:
        if status['add_most_item'] == '':

            if coll_bau:
                if bau_open == False and tc[bge.events.QKEY].activated:
                    if actF == 0:
                        status['open_bau'] = True
                        fading.playAction('fadingAction',0,12,play_mode = 0)
                        if '_game_test' in listScene:
                            listScene['_game_test'].suspend()
                if bau_open == True and tc[bge.events.QKEY].activated:
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
                            listScene[0].suspend()

                if open_invent == True and tc[bge.events.QKEY].activated:
                    if actF == 12:
                        status['open_invent'] = False
                        fading.playAction('fadingAction',12,0,play_mode = 0)
                        if '_game_test' in listScene:
                            listScene[0].resume()

                if actF >= 7:
                    inventory.worldPosition.x = 1.4
                if actF <= 7:
                    inventory.worldPosition.x = 8.5
            if status['fading'] >0:
                status['fading'] -=1
                    

            if status['fading'] <-0:
                status['fading'] +=1

def most_item(cont):
    own = cont.owner
    inventory = status['inventory']
    if len(inventory) <8:
        if status['add_most_item'] != '':
            if status['descri_item'] != '':
                descri_item = own.childrenRecursive.get('descri_item')
                descri_item['texto'] = status['descri_item']
            
            item_most = own.childrenRecursive.get('item_most')
            item_most.replaceMesh(status['add_most_item'])
            item_most.visible = True
            if status['most_item'] ==0 and not status['open_invent']:
                tc = bge.logic.keyboard.inputs
                if tc[bge.events.SPACEKEY].activated:
                    status['most_item'] = 0
                    status['add_most_item'] = ''
                    listScene = bge.logic.getSceneList()
                    listScene[0].resume()
                    status['descri_item'] = ''
                    descri_item['texto'] = None
                    bge.logic.sendMessage('remove_most_item')
    else:
        status['add_most_item'] = ''
        descri_item = own.childrenRecursive.get('descri_item')
        item_most = own.childrenRecursive.get('item_most')
        descri_item['texto'] = 'O inventário esta cheio !'
        item_most.visible = False
        if status['most_item'] ==0:
            tc = bge.logic.keyboard.inputs
            if tc[bge.events.SPACEKEY].activated and not status['open_invent']:
                descri_item['texto'] = None
                bge.logic.sendMessage('remove_most_item')

def update(cont):
    slots(cont)
    own = cont.owner
    usar_item_mover_item(cont)
    if status['shotin_time'] == 0 :
        abrir_inventario_bau(cont)
    scene = own.scene
    listScene = bge.logic.getSceneList()

    tc = bge.logic.keyboard.inputs
    if tc[bge.events.RKEY].activated and status['shotin_time'] == 0:
        arma = status['player']['arma_mao']
        if arma!='' and  arma!='faca' and status['agarrado'] == False:
            recarregar(cont)
            
    if status['most_item'] >0:
        status['most_item'] -=1
        print(status['most_item'])
    
    
    tc = bge.logic.keyboard.inputs
    if tc[bge.events.SPACEKEY].activated and status['most_item'] == 0 and not status['open_invent']:
        listScene[0].resume()
    

