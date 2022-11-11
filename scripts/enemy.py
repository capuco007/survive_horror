import bge
from bge.logic import globalDict as gd
status: dict = gd['game_status']
from mathutils import Vector

kb = bge.logic.keyboard.inputs
alive = True
active = False
scene = bge.logic.getCurrentScene()
player = [o for o in scene.objects if 'player' in o]
soltar = 0


def start(cont):
    own = cont.owner
    scene = own.scene
    own['pl'] = [o for o in scene.objects if 'player' in o]
    own['m'] = [o for o in scene.objects if 'nav' in o]
    own['z_arm'] = [o for o in own.childrenRecursive if 'z_arm' in o]
    own['pl_arm'] = [o for o in scene.objects if 'foco_mira_eix' in o]
    own['state'] = 'idle'
    own['is_mov'] = False
    own['hited'] = False
    own['atacar'] = 0
    own['soltar'] = 0
    own['vivo'] = True
    status['afast'] = False
    own['dano_pl'] = 0
    own['pos_play'] = [o for o in own.childrenRecursive if 'pos_play' in o]
    
    

    if not 'enemies' in scene:
        scene['enemies'] = [] 
    scene['enemies'].append(own)

def state_machine(cont):
    own = cont.owner
    group = own.groupObject
    pl =player[0]
    distancia= own.getDistanceTo(pl)
    Steering = cont.actuators['seguir']
    radar = cont.sensors['Radar']

    if own['vivo']:
        if status['afast'] and distancia < 3:
            own['state'] = 'hited'
            status['afast'] = False
        if group['life'] <= 0:
            own.suspendPhysics(True)
            cont.deactivate(Steering)
            own['state'] = 'death'
        if status['atacando']  >0:
            status['atacando'] -= 1

        if distancia < 5 and distancia >1:
                own['is_mov'] = True
        
        if own['state']  == 'idle':
            idle(cont)
                
        if own['state'] == 'walk':
            walk(cont,distancia,Steering)
            
        if own['state'] == 'atack':
            atack(cont,radar)

        if own['state'] == 'hited':
            hited(cont)

        if own['state'] == 'grab_atack':
            grab_atack(cont)
        if own['state'] == 'death':
            death(cont)
    if not own['vivo']:
        
        #own.suspendDynamics(True)
        own.suspendPhysics(True)


def death(cont):
    own = cont.owner
    frame  = own['z_arm'][0].getActionFrame(0)
    own['z_arm'][0].playAction('death',1,94,play_mode = 0,blendin = 5)
    if frame > 93 and frame < 94:
        own['vivo'] = False

def idle(cont):
    own = cont.owner
    own['z_arm'][0].playAction('idle_z',1,41,play_mode = 1,blendin = 5)
    if own['is_mov'] and  status['atacando'] == 0:
        own['state'] = 'walk'
    if own['hited']:
        own['state'] = 'hited'

def walk(cont,distancia,Steering):
    own = cont.owner
    own['soltar'] = 0
    own.applyMovement([0,0.01,0], True)
    Steering.target = player[0]
    Steering.navmesh = own['m'][0]
    cont.activate(Steering)
    if status['atacando'] == 0:
        own['z_arm'][0].playAction('walk_z_2',1,122,play_mode = 1,blendin = 5)
    if own['hited']:
        own['state'] = 'hited'
    if distancia < 2 and status['agarrado'] == False:
        own['state'] = 'atack'
        status['atacando'] = 150
    
def atack(cont,radar):
    own = cont.owner
    if  status['atacando'] > 50:
        if radar.positive and status['soltar'] == 0:
            own['state'] = 'grab_atack'
        own.applyMovement([0,0.01,0], True)
        own['z_arm'][0].playAction('agarrao_z',7,25,play_mode = 0,blendin = 5)

    if status['atacando'] < 50:
        own['state'] = 'idle'

def grab_atack(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    status['agarrado'] = True
    if own['dano_pl'] == 0:
        own['dano_pl'] = 50
    if own['dano_pl'] >0:
        own['dano_pl']-=1
    if own['soltar'] == 0:
        own['soltar']   = 50
    if own['dano_pl'] == 49 and status['player']['saude']>0:
        status['player']['saude'] -= 5

    if own['soltar'] > 0 and tc[bge.events.SPACEKEY].activated and status['player']['saude']>0:
        own['soltar'] -=5
    if own['soltar'] == 5:
        own['state'] = 'hited'
        status['afast'] = True
        status['agarrado'] = False
    if status['player']['saude']>0:
        own['z_arm'][0].playAction('agarrao_z',25,81,play_mode = 2,blendin = 5)
        player[0].worldPosition = own['pos_play'][0].worldPosition
        
        foco_mira_eix = player[0].childrenRecursive.get('foco_mira_eix')
        dir = own.worldPosition - foco_mira_eix.worldPosition
        foco_mira_eix.alignAxisToVect(-dir, 1, 0.5)
        foco_mira_eix.alignAxisToVect([0,0,1], 2, 1.0)

    if status['player']['saude']<=0:
        own['z_arm'][0].playAction('devora_z',1,209,play_mode = 2,blendin = 5)
    
def hited(cont):
    own = cont.owner
    frame  = own['z_arm'][0].getActionFrame(0)
    if frame >= 110:
        own['hited'] = False
        own['state'] = 'idle'
    elif frame < 110:
        own['z_arm'][0].playAction('agarrao_z',82,120,play_mode = 1,blendin = 5,speed = 2)
        dir = own.worldPosition - player[0].worldPosition
        own.alignAxisToVect( -dir , 1 , 1.0 )
        own.alignAxisToVect( [0,0,1] , 2 , 1.0 )
        own.applyMovement([0,-0.03,0], True)
        
   
    #own['z_arm'][0].playAction('idle_z',1,41,play_mode = 1,blendin = 5)
    #own['z_arm'][0].playAction('agarrao_z',82,126,play_mode = 1,blendin = 5, speed = 8)
        
    #own['z_arm'][0].playAction('death',1,94,play_mode = 0,blendin = 5)
   
    #own['z_arm'][0].playAction('walk_z',1,41,play_mode = 1,blendin = 5)
           
    #own['z_arm'][0].playAction('agarrao_z',7,25,play_mode = 0,blendin = 5)
        
    #own['z_arm'][0].playAction('agarrao_z',25,81,play_mode = 2,blendin = 5)
               