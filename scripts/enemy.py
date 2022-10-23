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
    own['is_mov'] = False
    own['ativo'] = False
    own['tempo_atacar'] = 0
    own['agarrao'] = False
    own['atack'] = False
    own['pl_arm'] = [o for o in scene.objects if 'foco_mira_eix' in o]
    own['dano_pl'] = 0
    own['soltar'] = 0
    own['recuo'] = 0
    own['dano_para_player'] = 0
    own['vivo'] = True

def update(cont):
    own = cont.owner
    seguir = cont.actuators['Steering']
    colision = cont.sensors['Collision']
    radar =  cont.sensors['Radar']
    z_arm = own.childrenRecursive.get('z_arm')
    dis = own.getDistanceTo(own['pl'][0])
    tc = bge.logic.keyboard.inputs
    
    obGroup = own.groupObject
    if obGroup['life'] > 0:
        anim(cont)
        if own['dano_para_player'] >0:
            own['dano_para_player'] -=1

        
        if own['tempo_atacar']>0:
            own['tempo_atacar']-=1
        # se o zumbi nao estiver ativo
        if not own['ativo'] and dis < 5:
            own['ativo'] = True
        if own['soltar'] < -0:
            own['soltar'] +=1

        # se o zumbi estiver ativo
        if own['ativo'] and own['atack'] == False:
            seguir.target = own['pl'][0]
            seguir.navmesh = own['m'][0]
            seguir.velocity = 0.6
            if dis >3 and  own['soltar'] == 0:
                cont.activate(seguir)
                own['is_mov'] = True
            else:
                atacar(cont)
                own['is_mov'] = False

        if own['soltar'] ==10:
            own['atack'] =False
            status['agarrado'] = False
            dir = own['pl_arm'][0].worldPosition - own.worldPosition
            own.alignAxisToVect(dir, 1, 0.5)
            own.alignAxisToVect([0,0,1], 2, 1.0)
            own.applyMovement([0,-0.5,0],True)
            own['soltar'] = -50

        if own['soltar'] < -20:
            own.applyMovement([0,-0.05,0],True)

    else:
        if own['vivo']:
            cont.deactivate(seguir)
            own['z_arm'][0].playAction('death',1,94,play_mode = 0,blendin = 5)
            own['vivo'] = False
            own.suspendDynamics(True)

def anim(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    if own['soltar'] == 49:
        own['z_arm'][0].playAction('agarrao_z',82,126,play_mode = 1,blendin = 5, speed = 4)
    
    if  own['ativo']:
        if own['atack'] == False:
            if own['tempo_atacar'] < 60:
                if own['soltar'] == 0:
                    own['z_arm'][0].playAction('walk_z',1,41,play_mode = 1,blendin = 5)
            if own['tempo_atacar'] >75:
                own['z_arm'][0].playAction('agarrao_z',7,25,play_mode = 0,blendin = 5)
        else:
            if status['agarrado']:
                own['z_arm'][0].playAction('agarrao_z',25,81,play_mode = 2,blendin = 5)
                if own['dano_para_player'] == 0:
                    own['dano_para_player'] = 80
                if own['dano_para_player'] == 79:
                    if status['player']['saude'] >0:
                        status['player']['saude'] -= 5
                if own['soltar'] == 0:
                    own['soltar'] = 100
                if tc[bge.events.SPACEKEY].activated and own['soltar']>0:
                    own['soltar'] -= 10

    else:
        if own['soltar'] == 0:
            own['z_arm'][0].playAction('idle_z',1,131,play_mode = 1,blendin = 5)
    
    


    
def atacar(cont):
    own = cont.owner
    radar =  cont.sensors['Radar']
    z_arm = own.childrenRecursive.get('z_arm')
    dis = own.getDistanceTo(own['pl'][0])
    Steering = cont.actuators['Steering']

    if own['tempo_atacar'] == 0:
        own['tempo_atacar'] = 90
        
    if  own['tempo_atacar'] > 75  and  own['soltar'] == 0:
        dir = own['pl_arm'][0].worldPosition - own.worldPosition
        own.alignAxisToVect(dir, 1, 0.5)
        own.alignAxisToVect([0,0,1], 2, 1.0)
        own.applyMovement([0,0.05,0],True)

    if radar.positive and  own['soltar'] == 0 and status['agarrado'] == False:
        own['atack'] = True
        own['tempo_atacar'] = 0
        o = radar.hitObject 
        agarrar(cont,o)
    else:
        if own['tempo_atacar'] == 0:
            own['atack'] = False

def agarrar(cont,o):
    own = cont.owner
    pos_play = own.childrenRecursive.get('pos_play')

    if o :
        status['regarregar'] = 0
        status['agarrado'] = True
        o.worldPosition = pos_play.worldPosition
        alain(cont)
def alain(cont):
    own = cont.owner
    if own['atack'] :
        dir = own['pl_arm'][0].worldPosition - own.worldPosition
        own['pl_arm'][0].alignAxisToVect(dir, 1, 0.5)
        own['pl_arm'][0].alignAxisToVect([0,0,1], 2, 1.0)