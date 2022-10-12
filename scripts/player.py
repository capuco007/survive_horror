from ast import literal_eval
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
    own['scene_pass'] = 0
    own['dor_open'] = False
    own['bauOpen'] = False
    own['invetOpen'] = False
    own['openBauTime'] = 0
    foco_mira_eix = own.childrenRecursive.get('foco_mira_eix')
    
    if status['scene'] !='':
        status['scene'] = ''
    if status['pos_spw']:
        own.worldPosition = status['pos_spw']
        status['pos_spw'] = []

def abrir_portas(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    coll_dor = cont.sensors['Collision']
    scene = own.scene
    inventory = status['inventory']
    msg = status['exib_msg']
    
    if coll_dor.positive:
        o = coll_dor.hitObject.groupObject
        # porta fechada
        if o['open'] == False:
            if tc[bge.events.SPACEKEY].activated:
                item = [it for it in inventory if 'key' in it]
                if item:
                    for i in inventory:
                        if 'key' in i:
                            if i['nome'] == o['keyPass']:
                                o['open']  = True
                                status['exib_msg'] = 'Voce destravou esta Porta'
                            else:
                                status['exib_msg'] = o['msg']
        
                    
                else:
                    status['exib_msg'] = o['msg']

        # porta aberta
        else:
            if tc[bge.events.SPACEKEY].activated:
                status['scene'] = o['local']
                status['pos_spw'] = literal_eval(o['position'])
        
    else:
        status['exib_msg'] = 'none'
       
def pegar_items(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    coll_itens = cont.sensors['coll_itens']            
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

    open_bau = status['open_bau']
    open_invent = status['open_invent']

    if not open_bau and not open_invent:
   
        char.walkDirection = Vector([x,y,0]).normalized()*0.08

    else:
        char.walkDirection = Vector([0,0,0]).normalized()*0.08
        
   
   
   
    own['isMove'] = char.walkDirection
        
def atirar(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    ms = cont.sensors['Mouse']
    point = own.childrenRecursive.get('point')
    if ms.positive:
        ray = own.rayCastTo(point,own.getDistanceTo(point),'enemy')
        print(ray)
        if not status['open_invent'] and not status['open_bau']:
            if status['shotin_time'] ==0:
                status['shotin_time'] = 30
                arma = status['player']['arma_mao']
                if arma !=  '':
                    if status['player']['bala_'+arma] >0:
                        status['player']['bala_'+arma] -=1
                        if ray:
                            o = ray.groupObject
                            o['life'] -= status['potencia_'+ arma] + o['resistencia']
                            

                    else:
                        bge.logic.sendMessage('reload')

def abrir_bau(cont):
    own = cont.owner
    coll = cont.sensors['coll_bau'] 
    tc = bge.logic.keyboard.inputs 
    invent_open = status['open_invent']

    if coll.positive:
        status['call_bau'] = True

    else:
        status['call_bau'] = False

def transicao_scene(cont):
    own = cont.owner
    scene = own.scene
    if status['scene_pass'] == True:
        scene.replace(status['scene'])

def mirar(cont):
    own = cont.owner
    ms = bge.logic.mouse.inputs
    foco_mira = cont.sensors['foco_mira']
    
    MouseTrack = cont.actuators['MouseTrack']
    if ms[bge.events.RIGHTMOUSE].active:
        if foco_mira.positive:

            enemy = foco_mira.hitObject
            dir = own.worldPosition - enemy.worldPosition
            own.alignAxisToVect( dir ,1 ,1.0 )
            cont.deactivate(MouseTrack)
        else:
            cont.activate(MouseTrack)

def update(cont):
    own = cont.owner
    up = cont.sensors['update']
    
    if up.positive:
        
        movement(cont)
        pegar_items(cont)
        abrir_portas(cont)
        abrir_bau(cont)
        transicao_scene(cont)
       
        if status['shotin_time'] >0:
            status['shotin_time']-=1

    