from builtins import print
from xml.etree.ElementTree import TreeBuilder
import bge
from mathutils import Vector
from .inventory  import *
from bge.logic import globalDict as gd


from scripts import inventory

status: dict = gd['game_status']




def start(cont):
    own = cont.owner
    
    own['arm'] = [arm for arm in own.childrenRecursive if 'player_arm' in arm]
    own['isMove'] = 0
    own['time_scene_pass'] = 0
    own['dor_open'] = False
    own['bauOpen'] = False
    own['invetOpen'] = False
    own['openBauTime'] = 0
    if status['pos_spw']:
        own.worldPosition = status['pos_spw']
        status['pos_spw'] = []
    
def update(cont):
    own = cont.owner
    movement(cont)
    colision(cont)
    openInventory(cont)
    bauOpen(cont)

    if own['time_scene_pass'] >1:
        own['time_scene_pass'] -= 1

def colision(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    coll_dor = cont.sensors['Collision']
    coll_itens = cont.sensors['coll_itens']
    scene = own.scene
    #print(own['time_scene_pass'])
    #Colidir com Portas 
    keys = status['inventory']
    
    if coll_dor.positive:

        o = coll_dor.hitObject.groupObject
        if tc[bge.events.SPACEKEY].activated:
            
            if o['keyPass'] in keys:
                if not o['open']:
                    o['open'] = True
                    status['exib_msg'] = 'Destrancou!!'
                    

            else:
                status['exib_msg'] = o['msg']
                
        if o['open'] and own['time_scene_pass'] == 0:
             if tc[bge.events.SPACEKEY].activated:
                own['time_scene_pass'] = 30

        if own['time_scene_pass'] == 1 and  tc[bge.events.SPACEKEY].activated:
            status['pos_spw'] = eval(o['position'])
            status['player']['scene'] = scene.name
            # alterar game-status
            scene.replace(o['Name'])
    else:
        own['time_scene_pass'] = 0 
        status['exib_msg'] = 'none'
                  
    #Colidir com Itens pegaveis
    if coll_itens.positive:
        o = coll_itens.hitObject.groupObject
        if tc[bge.events.SPACEKEY].activated:
            inventory = status['inventory']
            if len(inventory)< 8:
                item = {}
                
                # Pegar propriedades da instância de grupo do item
                for prop in o.getPropertyNames():
                    item[prop] = o[prop]
                itemAdd(item, inventory)
                o.endObject()
                    # alterar game-status
            else:
                
                status['exib_msg'] = 'nao ha mais espaço no inventario '# mostra que o inventario esta cheio
      
def movement(cont):
    own = cont.owner
    char = bge.constraints.getCharacter(own)
    tc = bge.logic.keyboard.inputs
    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    if status['openclosebau'] == False and status['open_invent'] == False:
        char.walkDirection = Vector([x,y,0]).normalized()*0.08
        
    else:
        char.walkDirection = Vector([0,0,0])
   
    own['isMove'] = char.walkDirection

def setMunision(cont):
    own = cont.owner
    ms = bge.logic.mouse.inputs
    player_user = status['player']
    invent = status['inventory']

    if status['open_invent'] == False:
        if ms[bge.events.LEFTMOUSE].activated:
            if 'pistola' in player_user['gun']:
                if player_user['M_pistola'] >0:
                    player_user['M_pistola'] -= 1
                    print(player_user['M_pistola'])

            if 'shotgun' in player_user['gun']:
                if player_user['M_shotgun'] >0:
                    player_user['M_shotgun'] -= 1
                    print(player_user['M_shotgun'])
    else:
        if 'pistola' in invent:
            pass

def openInventory(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    listScene = bge.logic.getSceneList()
    if tc[bge.events.QKEY].activated and own['openBauTime'] == 0:
        if status['open_invent'] == False:
            status['open_invent'] = True
            own['openBauTime'] = 20
            bge.logic.addScene('inventory',1)
    
    if tc[bge.events.QKEY].activated and own['openBauTime'] == 0:
        if status['open_invent'] == True:   
            status['open_invent'] = False
            status['openclosebau'] = False
            own['openBauTime'] = 20
            bge.logic.sendMessage('endScene')
    
    if own['openBauTime'] >0:
        own['openBauTime'] -= 1

def bauOpen(cont):
    own = cont.owner
    coll_bau  =cont.sensors['coll_bau']
    tc = bge.logic.keyboard.inputs

    if coll_bau.positive:
        if tc[bge.events.SPACEKEY].activated:
             status['open_invent'] = True
             status['openclosebau'] = True
             bge.logic.addScene('inventory',1)
                    
def msg(cont):
    own = cont.owner
    msg = status['exib_msg']
    

    
    if msg != 'none' and own['exib'] == 0:
        own.visible = True
        own['MSG'] = msg
        own['exib'] = 30

    if own['exib'] < 2:
        status['exib_msg'] = 'none'
        own.visible = False
        own['MSG'] = msg
    if own['exib'] >0:
        own['exib']-=1