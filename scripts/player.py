from ast import literal_eval
from builtins import print
from xml.etree.ElementTree import TreeBuilder
import bge
from mathutils import Vector
from .inventory  import *
from bge.logic import globalDict as gd
import aud


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
    own['speed'] = 0.0
    own['most_item'] = 0
    own['list_enemyes'] = []
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
            mostra_item(cont,o)
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


def mostra_item(cont,o):
    own = cont.owner
    listScene = bge.logic.getSceneList()
    listScene[0].suspend()
    #status['most_item'] = 1000
    if o:
        status['descri_item'] = o['descri_item_most']
        status['add_most_item'] = 'most_'+o['nome']
        bge.logic.sendMessage('add_most_item')
        status['most_item'] = 1000
        item_most = own.childrenRecursive.get('item_most')
 
def movement(cont):
    own = cont.owner
    char = bge.constraints.getCharacter(own)
    tc = bge.logic.keyboard.inputs
    ms = bge.logic.mouse.inputs
    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    open_bau = status['open_bau']
    open_invent = status['open_invent']
   
    if status['player']['saude'] >30:
        if not tc[bge.events.LEFTSHIFTKEY].active:
            own['speed'] =0.04
        else:
            own['speed'] =0.07
    else:
        own['speed'] = 0.03
    if status['regarregar'] ==0 and status['shotin_time'] ==0 and not status['agarrado'] and  status['player']['saude'] >0:
        if not status['agarrado']:
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
    tiro_metralha = cont.actuators['tiro_metralha']
    tiro_pistola = cont.actuators['tiro_pistola']
    tiro_shotgun = cont.actuators['tiro_shotgun']

    if status['agarrado'] == False and status['regarregar'] == 0:
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
                                if status['shotin_time'] == status['shotin_time_'+arma]:
                                    #bge.logic.sendMessage('shotin')
                                    cont.activate('tiro_'+arma)
                                    status['player']['bala_'+arma] -=1

                                if ray:
                                    o = ray.groupObject
                                    ob = ray
                                    o['life'] -= status['potencia_'+ arma] + o['resistencia']
                                    ob['dano'] = 50
                                    ob['ativo'] = True
                                    print(ob)
                                    

                            else:
                                if status['agarrado'] == False:
                                    bge.logic.sendMessage('reload') 
                                    
                                    no_bala(cont)

# Adicionar os sons dos tiros          #status['regarregar'] = 50
def no_bala(cont):
    own = cont.owner
    arma = status['player']['arma_mao']
    shot_time = 1 * status['shotin_time_'+arma]
    
    print(shot_time)

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
    scene = own.scene
    #MouseTrack = cont.actuators['MouseTrack']
    if ms[bge.events.RIGHTMOUSE].active :
        if status['player']['arma_mao'] != '':
            if foco_mira.positive:
                distancia = 99999
                enemy = None
                for o in scene['enemies']:
                    if o.getDistanceTo(own) <distancia:
                        distancia = o.getDistanceTo(own)
                        enemy = o
  
                if enemy:
                    dir = own.worldPosition - enemy.worldPosition
                    own.alignAxisToVect( dir ,1 ,1.0 )
                    own.alignAxisToVect([0,0,1], 2, 1.0)
        
            
    else:
        status['list_enemyes'] =[]
                #cont.activate(MouseTrack)
                #cont.deactivate(MouseTrack)
    if foco_mira.positive:
        pass
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
        # pistola
        'idle_pistola': 41,
        'walk_pistola': 25,
        'mirar_pistola': 41,
        'run_pistola': 23,
        'atirar_pistola': 15,
        'recarregar_pistola':28,
        # metralha
        'idle_metralha': 124,
        'run_metralha': 21,
        'walk_metralha': 34,
        'atirar_metralha': 5,
        'mirar_metralha': 94,
        'recarregar_metralha':82,
        # shotgun
        'walk_shotgun':34,
        'run_shotgun': 21,
        'idle_shotgun': 124,
        'mirar_shotgun': 94,
        'atirar_shotgun':30,
        'recarregar_shotgun':35,
        # faca
        'idle_faca': 181,
        'walk_faca': 32,
        'run_faca': 23,
        'atirar_faca': 46,
        'mirar_faca': 77,
        
        #danos
        'dano': 10,
        'dano_max':10,
        #morte
        'morreu': 10,
        # machucado
        'idle_machucado': 10,
        'walk_machucado': 10,

    }
    if status['player']['saude'] >0:
        if status['regarregar'] > 60:
            bge.logic.sendMessage('reload')
            own['arm'][0].playAction('recarregar_'+arma,1,frameAnim['run_'+arma],play_mode = 0,blendin = 2,speed = 2,priority = 0)
    
        if  status['agarrado'] and status['regarregar'] ==0:
            own['arm'][0].playAction('agarrado',1,24,play_mode = 2,blendin = 5)

        if not status['agarrado'] and status['regarregar'] ==0:
            if tc[bge.events.LEFTSHIFTKEY].active:
                own['speed'] = 0.07
            else:
                own['speed'] = 0.04

                # Mover Sem Armas
            if  status['shotin_time'] ==0:
                if status['player']['arma_mao'] == '':
                    if dir.length != 0:
                        if status['player']['saude'] >30:
                            if tc[bge.events.LEFTSHIFTKEY].active:
                                own['arm'][0].playAction('run_faca',1,23,play_mode = 1,blendin = 5)
                                
                            else:
                                own['arm'][0].playAction('walk',1,32,play_mode = 1,blendin = 5)
                        else:
                            own['arm'][0].playAction('machucado',1,31,play_mode = 1,blendin = 5)
                        
                    else:
                        if status['player']['saude'] >30:
                            own['arm'][0].playAction('idle',1,181,play_mode = 1,blendin = 5)
                        else:
                            own['arm'][0].playAction('idle',1,181,play_mode = 1,blendin = 5)

                else:
                    
                    if not ms[bge.events.RIGHTMOUSE].active:
                        if dir.length != 0:
                            if status['player']['saude'] >30:
                                if tc[bge.events.LEFTSHIFTKEY].active:
                                    own['arm'][0].playAction('run_'+arma,1,frameAnim['run_'+arma],play_mode = 1,blendin = 5)
                                    
                                else:
                                    own['arm'][0].playAction('walk_'+arma,1,frameAnim['walk_'+arma],play_mode = 1,blendin = 5)
                            else:
                                own['arm'][0].playAction('machucado',1,31,play_mode = 1,blendin = 5,speed = 0.9)
                        else:
                            if status['player']['saude'] >30:
                                own['arm'][0].playAction('idle_'+arma,1,frameAnim['idle_'+arma],play_mode = 1,blendin = 5)
                            else:
                                own['arm'][0].playAction('idle_mach',1,32,play_mode = 2,blendin = 5)
                    else:
                    
                        if status['shotin_time'] == 0:
                            own['arm'][0].playAction('mirar_'+arma,1,frameAnim['idle_'+arma],play_mode = 1,blendin = 5)
            else:
                if status['shotin_time'] >  status['shotin_time_'+arma]/ 1.2:
                    own['arm'][0].playAction('atirar_'+arma,1,frameAnim['atirar_'+arma],play_mode = 0,blendin = 1,speed = 2)

    else:
        own['arm'][0].playAction('death',1,94,play_mode = 0,blendin = 5)             
def update(cont):
    own = cont.owner
    up = cont.sensors['update']
    scenList = bge.logic.getSceneList()
   
    if up.positive:

        movement(cont)
        pegar_items(cont)
        abrir_portas(cont)
        abrir_bau(cont)
        transicao_scene(cont)
        anim(cont)
        walkDir(cont)
        
        
        if status['shotin_time'] >0:
            status['shotin_time']-=1
        if status['shotin_time'] <-0:
            status['shotin_time']=1
        if status['regarregar'] >0:
            status['regarregar'] -=2
        if status['tempo_morte'] ==500:
            scenList[0].suspend()
    