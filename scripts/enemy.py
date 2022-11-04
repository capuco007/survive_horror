import bge
from bge.logic import globalDict as gd
status: dict = gd['game_status']
from mathutils import Vector
def start(cont):
    own = cont.owner
    scene = own.scene
    own['pl'] = [o for o in scene.objects if 'player' in o]
    own['m'] = [o for o in scene.objects if 'nav' in o]
    own['z_arm'] = [o for o in own.childrenRecursive if 'z_arm' in o]
    own['pl_arm'] = [o for o in scene.objects if 'foco_mira_eix' in o]
    own['atack'] = False
    own['ativo'] = False
    own['tempo_atack'] = 0
    own['afastar'] = 0
    own['vivo'] = True
    own['agarrou'] = False
    own['soltar'] = 0
    own['dano'] = 0
    if not 'enemies' in scene:
        scene['enemies'] = [] 
    scene['enemies'].append(own)

def update(cont):
    own = cont.owner
    player = own['pl'][0]
    nav_mesh = own['m'][0]
    seguir = cont.actuators['Steering']
    soltar_msg = cont.sensors['enemy_coll']
    radar =  cont.sensors['Radar']
    z_arm = own.childrenRecursive.get('z_arm')
    dis = own.getDistanceTo(own['pl'][0])
    tc = bge.logic.keyboard.inputs
    obGroup = own.groupObject
    scene = own.scene

    if status['atacando'] > 0:
        status['atacando'] -= 1
    if status['atacando'] == 1 and status['player']['saude'] >0:
        status['player']['saude'] -= 2
    # Player morreu ###########
    if status['player']['saude'] <=0:
        own['afastar'] = 80
        own['ativo'] = False
        if status['tempo_morte'] <500:
            status['tempo_morte'] +=1

    if soltar_msg.positive:
        own['afastar'] = 80
    if own['soltar'] == 100:
        bge.logic.sendMessage('soltar')
        own['agarrou'] = False
        status['agarrado'] = False
        own['soltar'] = 0 
    if own['dano']>0:
        own['dano'] -=1

    if tc[bge.events.SPACEKEY].activated and own['soltar']  <100 and status['agarrado']:
        own['soltar']  += 10
        
    if own['tempo_atack'] >0:
        own['tempo_atack'] -=1

    if own['afastar'] >0:
        own['afastar'] -=1
        #own.applyMovement([0,-0.02,0],True)
        own['agarrou'] = False
        status['agarrado'] = False
    

    if obGroup['life'] > 0:
        anim(cont)
        dis = own.getDistanceTo(player)
        # Ativando o inimigo
        if dis < 6 and own['ativo'] == False and status['player']['saude'] >0:
            own['ativo'] = True
        # seguindo o player
        if own['ativo']:
            seguir.navmesh = nav_mesh
            seguir.target = player
            cont.activate(seguir)
        # atacando o player
        if dis <2 and own['tempo_atack'] == 0 and not status['agarrado'] and own['afastar'] ==0 and not own['agarrou']and own['dano'] == 0:
            own['tempo_atack'] = 50

        if radar.positive:
            if own['tempo_atack'] >40 and own['afastar'] ==0:
                pl = radar.hitObject
                status['agarrado'] = True
                pos_play = own.childrenRecursive.get('pos_play')
                pl.worldPosition = pos_play.worldPosition
                own['agarrou'] = True
                

    # se morreu 
    else:

        if own['vivo']:
            cont.deactivate(seguir)
            own['z_arm'][0].playAction('death',1,94,play_mode = 0,blendin = 5)
            own['vivo'] = False
            own.suspendDynamics(True)
            own.suspendPhysics(True)

    
def anim(cont):
    own = cont.owner
    player = own['pl'][0]
    dis = own.getDistanceTo(player)
    if own['ativo']:
        if own['dano'] >0:
            own['z_arm'][0].playAction('agarrao_z',82,126,play_mode = 1,blendin = 5, speed = 2)
            own.applyMovement([0,-0.02,0],True)
        else:
            if own['agarrou']:
                own['z_arm'][0].playAction('agarrao_z',25,81,play_mode = 2,blendin = 5)
                if status['atacando'] == 0:
                    status['atacando'] = 100
                dir = player.worldPosition - own.worldPosition
                foco_mira_eix = player.childrenRecursive.get('foco_mira_eix')
                foco_mira_eix.alignAxisToVect(dir, 1, 0.5)
                foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)
            else:
                if own['tempo_atack'] == 0 and   own['afastar'] ==0 and own['dano'] == 0:
                    own['z_arm'][0].playAction('walk_z',1,41,play_mode = 1,blendin = 5)
                    if dis >2:
                        own.applyMovement([0,0.01,0],True)
                if own['tempo_atack'] >20:
                    own['z_arm'][0].playAction('agarrao_z',7,25,play_mode = 0,blendin = 5)
                    own.applyMovement([0,0.02,0],True)
                if own['afastar'] >0 and dis < 2:
                    own['z_arm'][0].playAction('agarrao_z',82,126,play_mode = 1,blendin = 5, speed = 2)
                    own.applyMovement([0,-0.02,0],True)
           
            
    else:
        own['z_arm'][0].playAction('idle_z',1,41,play_mode = 1,blendin = 5)
    #own['z_arm'][0].playAction('agarrao_z',82,126,play_mode = 1,blendin = 5, speed = 8)
        
    #own['z_arm'][0].playAction('death',1,94,play_mode = 0,blendin = 5)
   
    #own['z_arm'][0].playAction('walk_z',1,41,play_mode = 1,blendin = 5)
           
    #own['z_arm'][0].playAction('agarrao_z',7,25,play_mode = 0,blendin = 5)
        
    #own['z_arm'][0].playAction('agarrao_z',25,81,play_mode = 2,blendin = 5)
               