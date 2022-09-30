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

def abrir_portas(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    coll_dor = cont.sensors['Collision']
    scene = own.scene
    keys = status['inventory']
    
    if coll_dor.positive:

        o = coll_dor.hitObject.groupObject
       
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

   
    char.walkDirection = Vector([x,y,0]).normalized()*0.08
        
   
   
   
    own['isMove'] = char.walkDirection

def setMunision(cont):
    own = cont.owner

def abrir_inventario(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    
def abrir_bau(cont):
    own = cont.owner
    coll_bau  =cont.sensors['coll_bau']
    tc = bge.logic.keyboard.inputs
   
def msg(cont):
    own = cont.owner
    msg = status['exib_msg']
        
def atirar(cont):
    tc = bge.logic.keyboard.inputs
    ms = bge.logic.mouse.inputs
    if not status['open_invent']:
        if ms[bge.events.LEFTMOUSE].activated and status['shotinTime'] == 0 and status['player']['bala_pistola']>0:
            status['shotinTime'] = 30
            status['player']['bala_pistola'] -=1
            print(status['player']['bala_pistola'])

def update(cont):
    own = cont.owner
    movement(cont)
    pegar_items(cont)
    abrir_inventario(cont)
    abrir_bau(cont)
    atirar(cont)
    abrir_portas(cont)

    if own['time_scene_pass'] >1:
        own['time_scene_pass'] -= 1
