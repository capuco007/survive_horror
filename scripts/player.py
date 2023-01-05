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
    scene = own.scene
    #gd['save_status_inRam']['last_scene'] = own.scene.name
    own['arm'] = [arm for arm in own.childrenRecursive if 'player_arm' in arm]
    own['can_pos'] = [o for o in own.childrenRecursive if 'pos_can' in o]
    own['can_track'] = [o for o in own.childrenRecursive if 'track_can' in o]
    own['point'] = [o for o in own.childrenRecursive if 'point' in o]
    own['Camera'] = [o for o in scene.objects if 'Camera_pl_pos' in o]
    own['Camera1'] = [o for o in scene.objects if 'Camera_pl' in o]

    own['isMove'] = 0
    own['scene_pass'] = False
    own['dor_open'] = False
    own['bauOpen'] = False
    own['invetOpen'] = False
    own['openBauTime'] = 0
    own['speed'] = 0.0
    own['most_item'] = 0
    own['list_enemyes'] = []
    own['oHited'] = None
    own['olhar'] = None
    own['arma_mao_pl'] = [o for o in own.childrenRecursive if 'arma_da_mao' in o]
    foco_mira_eix = own.childrenRecursive.get('foco_mira_eix')
    foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)
    status['trade_scene_time'] = 0
    if status['scene'] !='':
        status['scene'] = ''
        status['scene_pass'] = False

    
    if status['pos_spw']:
        own.worldPosition = status['pos_spw']
        dir = Vector(status['alaing']) - Vector(status['pos_spw'])
        foco_mira_eix.alignAxisToVect(dir, 1, 1.0) 
        status['pos_spw'] = []
        gd['save_ram']['player_position'] = ''
    else:
        if status['save_ram']['player_position'] !='':
            own.worldPosition = status['save_ram']['player_position']
    
def collDors(cont):
    own = cont.owner

def abrir_portas(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    coll_dor = cont.sensors['Collision']
    scene = own.scene
    inventory = status['inventory']
    msg = status['exib_msg']
    if status['agarrado'] == False:
        if coll_dor.positive:
            o = coll_dor.hitObject.groupObject
            # porta fechada
            if o['open'] == False:
                if tc[bge.events.SPACEKEY].activated :
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
                    status['save_ram']['last_scene'] = o['local']
                    save_status_game(cont)
                    status['pos_spw'] = literal_eval(o['position'])
                    status['alaing'] = literal_eval(o['alaing'])
                    status['scene'] = o['local']
                    
            
        else:
            status['exib_msg'] = 'none'
       
def pegar_items(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    coll_itens = cont.sensors['coll_itens']            
    #Colidir com Itens pegaveis
    if coll_itens.positive:
        o = coll_itens.hitObject.groupObject
        
        if tc[bge.events.SPACEKEY].activated and status['agarrado'] == False:
            mostra_item(cont,o)
            inventory = status['inventory']
            print(len(inventory)+1)
            if len(inventory)< 9:
                item = {}
                
                # Pegar propriedades da instância de grupo do item
                for prop in o.getPropertyNames():
                    item[prop] = o[prop]
                itemAdd(item, inventory)
                o.endObject()
                    # alterar game-status
            if len(inventory) >8:
                
                status['exib_msg'] = 'Nao ha mais espaço no inventario '# mostra que o inventario esta cheio

def mostra_item(cont,o):
    own = cont.owner
    listScene = bge.logic.getSceneList()
    listScene[0].suspend()
    #status['most_item'] = 1000
    if o:
        status['descri_item'] = o['descri_item_most']
        status['add_most_item'] = o['mesh']
        bge.logic.sendMessage('add_most_item')
        status['most_item'] = 1000
        item_most = own.childrenRecursive.get('item_most')
 
def movement(cont):
    own = cont.owner
    scene = own.scene
    char = bge.constraints.getCharacter(own)
    tc = bge.logic.keyboard.inputs
    ms = bge.logic.mouse.inputs
    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    open_bau = status['open_bau']
    open_invent = status['open_invent']
   
    if status['player']['saude'] >30:
        if not tc[bge.events.LEFTSHIFTKEY].active:
            own['speed'] =0.06
        else:
            own['speed'] =0.10
    else:
        own['speed'] = 0.03
    if status['dano'] == 0:
        if status['regarregar'] ==0 and status['shotin_time'] ==0 and not status['agarrado'] and  status['player']['saude'] >0:
            if not status['agarrado']:
                if not open_bau and not open_invent :
                    if not ms[bge.events.RIGHTMOUSE].active:
                        track_can = scene.objects['track_can']
                        char.walkDirection = track_can.worldOrientation * Vector([x,y,0]).normalized()*own['speed']
                    
                    else:
                        if status['player']['arma_mao'] == '':
                            char.walkDirection = Vector([x,y,0]).normalized()*own['speed'] 
                        else:
                            char.walkDirection = Vector([0,0,0]).normalized()*own['speed'] 
                else:
                    char.walkDirection = Vector([0,0,0]).normalized()*own['speed'] 
        else:
            char.walkDirection = Vector([0,0,0]).normalized()*own['speed'] 
    else:
        if  own['oHited']:
            dir = own.worldPosition - own['oHited'].worldPosition
            char.walkDirection = Vector(dir).normalized()*own['speed']

   
   
   
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
                                    ob['hited'] = True
                                    ob['is_mov'] = True
                                    print(ob)
                                    

                            else:
                                if status['agarrado'] == False:
                                    bge.logic.sendMessage('reload') 
                                    
                                    no_bala(cont)
                        if arma == 'faca':
                            
                            status['shotin_time'] = status['shotin_time_'+arma]
                            if status['shotin_time'] == status['shotin_time_'+arma]:
                                pass
                                #bge.logic.sendMessage('shotin')
                                #cont.activate('tiro_'+arma)
                                    

                            if ray:
                                o = ray.groupObject
                                ob = ray
                                dis = own.getDistanceTo(ob)
                                if dis < 3:
                                    o['life'] -= status['potencia_'+ arma] + o['resistencia']
                                    ob['hited'] = True
                                    ob['is_mov'] = True
                                    print(ob)

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
    setScene = cont.actuators['setScene']
    if status['trade_scene_time'] == 1:
        pass
        #setScene.scene = status['scene']
        #cont.activate(setScene)
        scene.replace(status['scene'])
        
def mirar(cont):
    own = cont.owner
    ms = bge.logic.mouse.inputs
    foco_mira = cont.sensors['foco_mira']
    tc = bge.logic.keyboard.inputs
    scene = own.scene
    
    #Look = cont.actuators['Look']
    
    if ms[bge.events.RIGHTMOUSE].activated :
        if status['player']['arma_mao'] != '':
            if foco_mira.positive:
                distancia = 99999
                enemy = None
                for o in scene.objects:
                    if 'enemy' in o:
                        if o.getDistanceTo(own) <distancia:
                            distancia = o.getDistanceTo(own)
                            enemy = o
  
                if enemy:
                    en = enemy.groupObject
                    if en['life']>0:
                        dir = own.worldPosition - enemy.worldPosition
                        own.alignAxisToVect( dir ,1 ,1.0 )
                        own.alignAxisToVect([0,0,1], 2, 1.0)
                        scene.objects['track_can'].alignAxisToVect( -dir ,1 ,1.0 )
                        scene.objects['track_can'].alignAxisToVect([0,0,1], 2, 1.0)
        
            
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
    scene = own.scene
    char = bge.constraints.getCharacter(own)
    dir = char.walkDirection
    foco_mira_eix = own.childrenRecursive.get('foco_mira_eix')
    track_can = own.childrenRecursive.get('track_can')
    
    if dir.length != 0:
        if  own['oHited']:
            print(own['oHited'],track_can)
            dir = own.worldPosition - own['oHited'].worldPosition
            foco_mira_eix.alignAxisToVect(dir, 1, 0.5)
            foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)
            
        else:
            foco_mira_eix.alignAxisToVect(-dir, 1, 0.5)
            foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)
            track_can.alignAxisToVect(dir, 1, 0.04)
            track_can.alignAxisToVect([0,0,1], 2, 1.0)

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
        'atirar_faca': 20,
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
        if status['dano'] ==0:
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
                                    own['arm'][0].playAction('run_faca',1,23,play_mode = 1,blendin = 5,speed = 1)
                                    
                                else:
                                    own['arm'][0].playAction('walk',1,32,play_mode = 1,blendin = 5,speed = 1)
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
                                        own['arm'][0].playAction('run_'+arma,1,frameAnim['run_'+arma],play_mode = 1,blendin = 5,speed = 1)
                                        
                                    else:
                                        own['arm'][0].playAction('walk_'+arma,1,frameAnim['walk_'+arma],play_mode = 1,blendin = 5,speed = 1)
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

        if status['dano']>0:
            own['arm'][0].playAction('agarrao_z',82,120,play_mode = 1,blendin = 5)
    else:
        scene = own.scene
        
        frame  = own['arm'][0].getActionFrame(0) 
        if frame < 1.5:
            scene.addObject('bloco_player',own,0)
        if frame< 105:

            own['arm'][0].playAction('death_2',1,106,play_mode = 0,blendin = 5,speed = 2)   
        
        print(frame)
        if frame >105:

            listScene = bge.logic.getSceneList()
            listScene[0].suspend() 
            bge.logic.sendMessage('restart')     

def damage(cont):
    own = cont.owner
    dano = cont.sensors['dano']
    if dano.positive and status['dano'] == 0:
        if status['player']['saude']>0:
            status['player']['saude'] -= 5
        status['dano'] = 20
        own['oHited'] = dano.hitObject
        
def hited(cont):
    own = cont.owner

def save_status_game(cont):
    from pprint import pformat
    
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    
    save_game_ram = status['save_ram']
    scene = own.scene
    save_game_ram[scene.name] = {}

    for o in scene.objects:
        if 'save' in o:
            obj_data = {}
            for prop in o.getPropertyNames():
                obj_data[prop] = o[prop]
                status['save_ram'][scene.name][o.name] = obj_data
                #gd['save_ram'][scene.name][o.name] = obj_data
                

def load_in_disc(cont):
    own = cont.owner
    scene = own.scene
    global status
    tc = bge.logic.keyboard.inputs
    from pprint import pformat
    ms = cont.sensors['Mouse']
    msKey = bge.logic.mouse.inputs
    print(status['trade_scene_time'])
    if status['trade_scene_time'] >0:
        status['trade_scene_time'] -=1
    if ms.positive and msKey[bge.events.LEFTMOUSE].activated:
        try:

            with open(bge.logic.expandPath('//save.txt'), 'r') as openedFile:
                status = eval(openedFile.read())
                print('> Savegame carregado de', openedFile.name)
                bge.logic.sendMessage('load')
                if status['trade_scene_time'] == 0:
                    status['trade_scene_time'] = 60
        except Exception as e:
            print('nao achou o save .txt')

    if status['trade_scene_time'] ==1:
        print(status['save_ram']['last_scene'])
        scene.replace(status['save_ram']['last_scene'])


       

def save_in_dis(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    from pprint import pformat

    save_game = cont.sensors['save_game']
    if save_game.positive and tc[bge.events.SPACEKEY].activated:
        gd['save_ram']['player_position'] = own.worldPosition
        gd['save_ram']['last_scene'] = own.scene.name
       
        # open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            #openedFile.write(pformat(gd['save_ram']))
            #print('> Savegame salvo em', openedFile.name)
        with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            openedFile.write(pformat(gd['game_status']))
            print('> Savegame salvo em', openedFile.name)
        
def load_game(cont):
    from pprint import pformat
    print('carregou static game')
    scene = cont.owner.scene
    save_game_ram = status['save_ram']
    scene_data = save_game_ram.get(scene.name)
    scene_last = save_game_ram['last_scene']
    
    if scene_last !='' and scene.name != scene_last:
        status['scene'] = scene_last
        status['scene_pass'] = False

    if scene_last == scene.name:
        status['scene'] = ''

    if scene_data:
        for obj in scene.objects:
            if 'save' in obj:
                if obj.name in scene_data.keys():
                    props = scene_data[obj.name]
                    for prop in props.keys():
                        obj[prop] = props[prop]
                
                else :
                    obj.endObject()
                if 'life' in obj:
                    if obj['life']<=0:
                        obj.endObject()
       
def save_load(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    from pprint import pformat

    #load
    if tc[bge.events.LKEY].activated:
        try:
            with open(bge.logic.expandPath('//save.txt'), 'r') as openedFile:
                gd['save_ram'] = eval(openedFile.read())
                print('> Savegame carregado de', openedFile.name)
        except Exception as e:
            print('nao achou o save .txt')

        try:
            with open(bge.logic.expandPath('//save_pl.txt'), 'r') as openedFile:
                gd['game_status'] = eval(openedFile.read())
                print('> Savegame carregado de', openedFile.name)
        except Exception as e:
            print('nao achou o save .txt')

   
      
    #save

    if tc[bge.events.HKEY].activated:
        gd['save_ram']['player_position'] = own.worldPosition
        gd['save_ram']['last_scene'] = own.scene.name
        with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            openedFile.write(pformat(gd['save_ram']))
            print('> Savegame salvo em', openedFile.name)
        with open(bge.logic.expandPath('//.save_pltxt'), 'w') as openedFile:
            openedFile.write(pformat(gd['game_status']))
            print('> Savegame salvo em', openedFile.name)

def new_game(cont):
    from pathlib import Path
    own = cont.owner
    scene = own.scene
    print(status['trade_scene_time'])
    if status['trade_scene_time'] >0:
        status['trade_scene_time'] -=1
  
    ms = bge.logic.mouse.inputs
    path = Path(bge.logic.expandPath('//save.txt'))
   
    if ms[bge.events.LEFTMOUSE].activated:
        bge.logic.sendMessage('new')
        if path.exists():
            path.unlink()
        status['trade_scene_time'] = 20
       
    if status['trade_scene_time'] ==1:
        scene.replace('salao_principal')
def can_collision(cont):
    own = cont.owner
    scene = own.scene
    ray = own.rayCast( own['can_track'][0],own['can_pos'][0], own['can_track'][0].getDistanceTo(own['can_pos'][0]),'wall')
    if ray[0] != None:
        print(ray)
        own['Camera'][0].worldPosition = ray[1]
        own['Camera'][0].worldPosition.y = ray[1][1] +0.6
        #own['Camera'][0].worldPosition.z = ray[1][2] +1.5

        
        
        
        
        #own['Camera'][0].sensor_width = 100.0
    else:
        own['Camera'][0].worldPosition = own['can_pos'][0].worldPosition

   
def update(cont):
    own = cont.owner
    up = cont.sensors['update']
    scenList = bge.logic.getSceneList()
    scene = own.scene
    can_collision(cont)
    tc = bge.logic.keyboard.inputs
    if tc[bge.events.DELKEY].activated:
        new_game(cont)
    save_in_dis(cont)
    if own['arma_mao_pl']:
        if status['player']['arma_mao']:
            own['arma_mao_pl'][0].replaceMesh('mesh_' + status['player']['arma_mao'])
            own['arma_mao_pl'][0].visible = True
        else:
            own['arma_mao_pl'][0].visible = False
   
    if up.positive:

        movement(cont)
        pegar_items(cont)
        abrir_portas(cont)
        abrir_bau(cont)
        transicao_scene(cont)
        anim(cont)
        walkDir(cont)
        #can_collision(cont)
        
        if status['dano'] >0:
            status['dano'] -=1
        if status['dano'] == 0:
            own['oHited'] = None
        
        if status['shotin_time'] >0:
            status['shotin_time']-=1
        if status['shotin_time'] <-0:
            status['shotin_time']=1
        if status['regarregar'] >0:
            status['regarregar'] -=2
        if status['tempo_morte'] ==500:
            #scene.suspend()
            scenList[status['scene']].suspend()
    