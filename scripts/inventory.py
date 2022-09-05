import bge
from bge.types import *
from collections import OrderedDict
from bge.logic import globalDict as gd

status: dict = gd['game_status']


def start(cont: SCA_PythonController):
    own = cont.owner
    own['slots'] = [obj for obj in own.childrenRecursive if 'slot' in obj]
    own['slot_bau'] = [obj for obj in own.childrenRecursive if 'slot_bau' in obj]
    
    own['i'] = None
    own['invent_open'] = 0
    own['empt'] = own.childrenRecursive.get('Empty')
    own['opne_inv'] = False
    own['reload'] = 0
    own['bauOpen'] = False
    own['pos_slot'] = 0
    
    scene = own.scene
    botom_bau = scene.objects['botom_bau']
    botom: KX_GameObject = scene.objects['botom']
    botom.worldPosition = [10,10,1]
    botom_bau.worldPosition = [10,10,1]

def update(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    mesage(cont)
    menu_inset(cont)
    openCloseBau(cont)
    revive(cont)
    if status['player']['life'] > 100:
        status['player']['life'] = 100
    
    own['bauOpen'] = status['openclosebau']

    if status:
        m_over(cont)   

    if own['reload'] >0:
        own['reload'] -= 1
        reloadGun(cont)
    if tc[bge.events.RKEY].activated:
        own['reload'] = 20

def openCloseBau(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    if status['openclosebau']:
        bge.logic.sendMessage('open')
        own['bauOpen'] = True
        get_bau(cont)
    
def menu_inset(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    scene = own.scene
    botom: KX_GameObject = scene.objects['botom']

    if own['opne_inv'] == False:
            
        botom.worldPosition = [10,10,1]
    
    if own['invent_open'] > 0:
        own['invent_open'] -= 1

    if own['invent_open'] < -0:
        own['invent_open'] += 1

    if tc[bge.events.EKEY].activated and own['invent_open'] == 0:
        if own['opne_inv'] == False:
            own['invent_open'] = 10
            botom.worldPosition = [10,10,1]
        else:
            own['invent_open'] = -10

    if own['invent_open'] == 10:
        get_itens(cont)

    if own['invent_open'] == 9 and own['opne_inv'] == False:
        own['opne_inv'] = True
        status['open_invent'] = True

    if own['invent_open'] == -9 and own['opne_inv'] == True:
        own['opne_inv'] = False
        status['open_invent'] = False

    if own['invent_open'] != 0:
        if own['opne_inv']:
            own['empt'].playAction('inventory',0,5)
            
        else:
            own['empt'].playAction('inventory',5,10)
                
def get_itens(cont):
    own = cont.owner
    
    if status:
        itens = list(status['inventory'])
        for slot in own['slots']:
            quant =[o for o in slot.childrenRecursive if 'quant' in o] 
            if  len(itens) > slot['number']:
                if itens[slot['number']] in itens:
                    slot['mesh'] = itens[slot['number']] 
                    
                    
                    if  status['inventory'][slot['mesh']] == 'gun_tipe':
                        quant[0]['quant'] = str(status['player'][str('M_')+slot['mesh']])
                        
                        #print('municao da arma',slot['mesh'])
                    else:
                        quant[0]['quant'] =  str(status['inventory'][slot['mesh']])
                        #print('municao reload')
                    
                    slot.replaceMesh(slot['mesh'])
                    slot.visible = True
                    quant[0].visible = True

                else:
                    slot.replaceMesh('none')
                    slot['mesh'] = ''
                    

            else:
                slot.visible = False
                quant[0]['quant'] = str(0)
                quant[0].visible = False
                slot['mesh'] = ''

def get_bau(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    itens = list(status['bau'])

    
    for slot in own['slot_bau']:
        quant =[o for o in slot.childrenRecursive if 'quant' in o] 
       

        if  len(itens) > slot['number']:

            if itens[slot['number']] in itens:
                slot['mesh'] = itens[slot['number']] 

                if  status['bau'][slot['mesh']] == 'gun_tipe':
                       
                    quant[0]['quant'] = str(status['player'][str('M_')+slot['mesh']])
                            
                else:
                    quant[0]['quant'] =  str(status['bau'][slot['mesh']])

                slot.replaceMesh(slot['mesh'])
                slot.visible = True
                quant[0].visible = True
        else:
            slot.visible = False
            quant[0].visible = False
            slot.replaceMesh('none')
            slot['mesh'] = ''
            
def m_over(cont):
    own = cont.owner
    scene = own.scene
    m_Over = cont.sensors['MouseOver']  
    ms = bge.logic.mouse.inputs
    botom = scene.objects['botom']
    botom_bau = scene.objects['botom_bau']
    player_user = status['player']
    itens = list(status['inventory'])
    if m_Over.positive:
        ob = m_Over.hitObject
        
        if 'slot' in m_Over.hitObject:
            if ms[bge.events.LEFTMOUSE].activated:
                o = m_Over.hitObject
                own['i'] = o
                if o['mesh']!= '':
                    
                    botom.worldPosition.x = o.worldPosition.x
                    botom.worldPosition.y = o.worldPosition.y
                    
        
        ###### Usar do Inventario ########################
        if own['bauOpen'] == False:
            if 'usar' in ob and own['i']:
                if ms[bge.events.LEFTMOUSE].activated:
                    botom.worldPosition = [10,10,1]
                    name = str(own['i']['mesh'])
                    if name in status['inventory']:
                        i = status['inventory'][name]
                        if i == 'gun_tipe':
                            if not name in player_user['gun']:
                                player_user['gun'] = name
                                
                            else:
                                if player_user['gun'] != 'none':
                                    own['reload'] = 20


                        
                        
                        if name == 'vida': 
                            
                            if status['player']['life'] < 100:
                                status['inventory'][name]-=1
                                get_itens(cont)
                                status['player']['life'] += 50
                                print(status['player']['life'])
                            
                            
                            

                        if i == 'key':
                            pass

                        if i != 'key' and not 'gun_tipe':
                            if player_user['gun']:
                                
                                del status['inventory'][name]
                                own['i']['mesh'] = ''
                                own['i'].replaceMesh('none')
                                botom.worldPosition = [10,10,1]
############### Colocar no Bau ################

        else:
            
            if 'usar' in ob and own['i']:
                if ms[bge.events.LEFTMOUSE].activated:
                    name = str(own['i']['mesh'])
                    if name in status['inventory']:
                        i = status['inventory'][name]
                        if not name in status['bau']:
                            status['bau'][name] = i
                        else:
                            status['bau'][name] += i
                        del(status['inventory'][name])
                        get_itens(cont)
                        get_bau(cont)
                        botom.worldPosition = [10,10,1]
                        

####################### Pegar do Bau #######################
            
            
            if 'slot_bau' in m_Over.hitObject:
                
                ob_bau = m_Over.hitObject
                own['i'] = ob_bau
                if ms[bge.events.LEFTMOUSE].activated:  
                    if own['i']['mesh'] != '':
                        botom_bau.worldPosition.x = ob_bau.worldPosition.x
                        botom_bau.worldPosition.y = ob_bau.worldPosition.y  

            if 'pegar' in m_Over.hitObject and  own['i']:
                if ms[bge.events.LEFTMOUSE].activated:
                    quant =[o for o in own['i'].childrenRecursive if 'quant' in o] 
                    name = str(own['i']['mesh'])
                    if name in status['bau']:
                        i = status['bau'][name]
                        
                        if name in status['bau']:
                            if name == 'vida':
                                status['bau'][name] -= 1
                                if 'vida' in status['inventory']:
                                    status['inventory'][name] +=1
                                    get_itens(cont)
                                    get_bau(cont)
                                else:
                                    status['inventory']['vida'] =1
                                    get_itens(cont)
                                    get_bau(cont)
                            else:
                                status['inventory'][name] = i
                                own['i']['mesh'] = ''
                                own['i'].replaceMesh('none')
                                quant[0]['quant'] = str('')
                                del(status['bau'][name])
                    
                            get_itens(cont)
                            get_bau(cont)
                            botom_bau.worldPosition = [10,10,1]
                                                                     
def reloadGun(cont):
    own = cont.owner
    scene = own.scene
    player_user = status['player']
    inventory = status['inventory']
    botom= scene.objects['botom']

    get_itens(cont)
# reload pistola ###################
    if player_user['gun'] == 'pistola':
        if 'M_pistola' in inventory:
            if player_user['M_pistola'] < 10 and int(inventory['M_pistola']) >0:
                player_user['M_pistola'] += 1
                inventory['M_pistola'] -= 1
            
                

    if 'M_pistola' in inventory:
        if inventory['M_pistola'] == 0:
            del(inventory['M_pistola'])
            botom.worldPosition = [10,10,1]
        
################# Reload Shotgun ##############
    if player_user['gun'] == 'shotgun':
        if 'M_shotgun' in inventory:
            if player_user['M_shotgun'] < 10 and int(inventory['M_shotgun']) >0:
                player_user['M_shotgun'] += 1
                inventory['M_shotgun'] -= 1
            

    if 'M_shotgun' in inventory:
        if inventory['M_shotgun'] == 0:
            del(inventory['M_shotgun'])
            botom.worldPosition = [10,10,1]
    #print(player_user,inventory)                                    
def load_config(cont):
    own = cont.owner
    from ast import literal_eval

    savegame = {}

    try:
        with open(bge.logic.expandPath('//save.txt'), 'r') as openedFile:
            savegame = literal_eval(openedFile.read())
            #print('> Savegame carregado de', openedFile.name)
            status = savegame

    except Exception as e:
            print('X Savegame não existe', e)

def save_config(cont):
    own = cont.owner
    savegame = status
    with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            openedFile.write(str(savegame))

def mesage(cont):
    own = cont.owner
    scene = own.scene
    MSG_exib = scene.objects['MSG']

    if 'exib_msg' in status:
        if status['exib_msg'] != 'none':
            MSG_exib['MSG'] = status['exib_msg']
        else:
            MSG_exib['MSG'] = ""

def revive(cont):
    own = cont.owner
    inventory = status['inventory']
    bau = status['bau']

    if status['player']['life'] > 100:
        status['player']['life'] = 100

    if 'vida' in inventory:
        if inventory['vida'] ==0:
            del(inventory['vida'])
            get_itens(cont)
            print(inventory,'acabou')

    if 'vida' in bau:
        if bau['vida'] ==0:
            del(bau['vida'])
            get_itens(cont)
            print(bau,'acabou')