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
    own['speed'] = 0.06
    foco_mira_eix = own.childrenRecursive.get('foco_mira_eix')
    foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)
    if status['scene'] !='':
        status['scene'] = ''
    if status['pos_spw']:
        own.worldPosition = status['pos_spw']
        dir = Vector(status['alaing']) - Vector(status['pos_spw'])
        foco_mira_eix.alignAxisToVect(dir, 1, 1.0)
        
        status['pos_spw'] = []
def collDors(cont):
    own = cont.owner

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
                status['alaing'] = literal_eval(o['alaing'])
        
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
    ms = bge.logic.mouse.inputs
    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    open_bau = status['open_bau']
    open_invent = status['open_invent']
    if not status['agarrado'] and status['regarregar'] ==0:
        if not open_bau and not open_invent :
            if not ms[bge.events.RIGHTMOUSE].active:
                char.walkDirection = Vector([x,y,0]).normalized()*own['speed']
            
            else:
                if status['player']['arma_mao'] == '':
                    char.walkDirection = Vector([x,y,0]).normalized()*own['speed'] 
                else:
                    char.walkDirection = Vector([0,0,0]).normalized()*own['speed'] 
        else:
            char.walkDirection = Vector([0,0,0]).normalized()*own['speed'] 
    else:
        char.walkDirection = Vector([0,0,0]).normalized()*own['speed'] 
        
   
   
   
    own['isMove'] = char.walkDirection
        
def atirar(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    ms = cont.sensors['Mouse']
    msR = cont.sensors['MouseRight']
    point = own.childrenRecursive.get('point')

    if status['agarrado'] == False and status['regarregar'] ==0:
        if ms.positive and msR.positive:
            arma = status['player']['arma_mao']
            ray = own.rayCastTo(point,own.getDistanceTo(point),'enemy')
            
            if not status['open_invent'] and not status['open_bau']:
                arma = status['player']['arma_mao']
                if arma != '':
                    if status['shotin_time'] ==0:
                        #status['shotin_time'] = status['shotin_time_'+arma]
                        #arma = status['player']['arma_mao']
                        if arma != 'faca':
                            if status['player']['bala_'+arma] >0:
                                status['shotin_time'] = status['shotin_time_'+arma]
                                status['player']['bala_'+arma] -=1
                                bge.logic.sendMessage('shotin')

                                if ray:
                                    o = ray.groupObject
                                    o['life'] -= status['potencia_'+ arma] + o['resistencia']
                                

                            else:
                                if status['agarrado'] == False:
                                    bge.logic.sendMessage('reload') 
                                    #status['regarregar'] = 50

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
    tc = bge.logic.keyboard.inputs
    #MouseTrack = cont.actuators['MouseTrack']
    if ms[bge.events.RIGHTMOUSE].active and status['player']['arma_mao'] != '':
        if foco_mira.positive:

            enemy = foco_mira.hitObject
            dir = own.worldPosition - enemy.worldPosition
            own.alignAxisToVect( dir ,1 ,0.5 )
            own.alignAxisToVect([0,0,1], 2, 1.0)
            

            #cont.deactivate(MouseTrack)
        else:
            if tc[bge.events.AKEY].active:
                own.applyRotation([0,0,0.05],True)
            elif tc[bge.events.DKEY].active:
                own.applyRotation([0,0,-0.05],True)
            #cont.activate(MouseTrack)
def walkDir(cont):
    own = cont.owner
    char = bge.constraints.getCharacter(own)
    dir = char.walkDirection
    foco_mira_eix = own.childrenRecursive.get('foco_mira_eix')
    if dir.length != 0:
        
        foco_mira_eix.alignAxisToVect(-dir, 1, 0.5)
        foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)

def anim(cont):
    own = cont.owner
    char = bge.constraints.getCharacter(own)
    dir = char.walkDirection
    tc = bge.logic.keyboard.inputs
    ms = bge.logic.mouse.inputs
    arma = status['player']['arma_mao']
    frameAnim = {
        'idle_pistola': 41,
        'walk_pistola': 25,
        'mirar_pistola': 41,
        'run_pistola': 23,
        'atirar_pistola': 15,
        'idle_metralha': 124,
        'run_metralha': 21,
        'walk_metralha': 34,
        'atirar_metralha': 5,
        'mirar_metralha': 94,
        'dano': 10,
        'dano_max':10,
        'walk_shotgun':10,
        'run_shotgun': 10,
        'idle_shogun': 10,
        'mirar_shotgun': 10,
        'atirar_shotgun':10,
        'idle_faca': 181,
        'walk_faca': 32,
        'run_faca': 23,
        'atirar_faca': 46,
        'mirar_faca': 77,
        'recarregar_pistola':100,
        'recarregar_shotgun':20,
        'recarregar_metralha':100,

    }
    if status['regarregar'] >0:
        bge.logic.sendMessage('reload')
        own['arm'][0].playAction('recarregar_'+arma,1,frameAnim['run_'+arma],play_mode = 0,blendin = 5,speed = 2)

    if  status['agarrado'] and status['regarregar'] ==0:
        own['arm'][0].playAction('agarrado',1,24,play_mode = 2,blendin = 5)

    if not status['agarrado'] and status['regarregar'] ==0:
        if tc[bge.events.LEFTSHIFTKEY].active:
            own['speed'] = 0.09
        else:
            own['speed'] = 0.06

            # Mover Sem Armas
        if  status['shotin_time'] ==0:
            if status['player']['arma_mao'] == '':
                if dir.length != 0:
                    if tc[bge.events.LEFTSHIFTKEY].active:
                        own['arm'][0].playAction('run_faca',1,23,play_mode = 1,blendin = 5)
                        
                    else:
                        own['arm'][0].playAction('walk',1,32,play_mode = 1,blendin = 5)
                    
                else:
                    own['arm'][0].playAction('idle',1,181,play_mode = 1,blendin = 5)

            else:
            
                if not ms[bge.events.RIGHTMOUSE].active:
                    if dir.length != 0:
                        if tc[bge.events.LEFTSHIFTKEY].active:
                            own['arm'][0].playAction('run_'+arma,1,frameAnim['run_'+arma],play_mode = 1,blendin = 5)
                            
                        else:
                            own['arm'][0].playAction('walk_'+arma,1,frameAnim['walk_'+arma],play_mode = 1,blendin = 5)
                        
                    else:
                        own['arm'][0].playAction('idle_'+arma,1,frameAnim['idle_'+arma],play_mode = 1,blendin = 5)
                else:
                
                    if status['shotin_time'] == 0:
                        own['arm'][0].playAction('mirar_'+arma,1,frameAnim['idle_'+arma],play_mode = 1,blendin = 5)
        else:
            own['arm'][0].playAction('atirar_'+arma,1,frameAnim['atirar_'+arma],play_mode = 0,blendin = 2)
    
def update(cont):
    own = cont.owner
    up = cont.sensors['update']
   
    if up.positive:
        
        movement(cont)
        pegar_items(cont)
        abrir_portas(cont)
        abrir_bau(cont)
        transicao_scene(cont)
        anim(cont)
        walkDir(cont)
        print(status['shotin_time'])
        if status['shotin_time'] >0:
            status['shotin_time']-=1
        if status['regarregar'] >0:
            status['regarregar'] -=1

    