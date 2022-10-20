import bge
from bge.logic import globalDict as gd
status: dict = gd['game_status']
def start(cont):
    own = cont.owner
    scene = own.scene
    own['pl'] = [o for o in scene.objects if 'player' in o]
    own['m'] = [o for o in scene.objects if 'nav' in o]
    own['is_mov'] = False
    own['ativo'] = False
    own['atacar'] = 0
    own['agarrao'] = False
    own['atackTime'] = 0
    own['pl_arm'] = [o for o in scene.objects if 'foco_mira_eix' in o]
def update(cont):
    own = cont.owner
    Steering = cont.actuators['Steering']
    colision = cont.sensors['Collision']
    radar =  cont.sensors['Radar']
    z_arm = own.childrenRecursive.get('z_arm')
    dis = own.getDistanceTo(own['pl'][0])
    alain(cont)

    if own['atackTime'] >0:
        own['atackTime']-=1
    if own['atackTime'] == 0:
        own['agarrao'] = False
        status['agarrado'] = False
    if own['ativo'] and   own['atackTime'] == 0:
        if dis < 3 and own['atacar'] == 0:
            own['atacar'] = 200


        else:
            cont.deactivate(Steering)
        if own['atacar'] < 170:
                z_arm.playAction('walk_z',1,42,play_mode = 1)

        if own['m']:
            if not own['agarrao']:
        
                Steering.navmesh = own['m'][0]
                if own['pl']:
                    Steering.target = own['pl'][0]

                    cont.activate(Steering)
                    own['is_mov'] = True
            else:
                 cont.deactivate(Steering)
    else:
        z_arm.playAction('agarrao_z',33,80,play_mode = 2,blendin = 6)
        if dis< 20:
            own['ativo'] = True

    if own['atacar'] >0:
        atacar(cont)
        own['atacar'] -=1
def atacar(cont):
    own = cont.owner
    radar =  cont.sensors['Radar']
    z_arm = own.childrenRecursive.get('z_arm')
    dis = own.getDistanceTo(own['pl'][0])
    Steering = cont.actuators['Steering']


    if own['atacar'] >170:
       
        
        own.applyMovement([0,0.03,0],True)
        z_arm.playAction('agarrao_z',15,30,play_mode = 0,blendin = 6)

    if own['atacar'] >170:
        cont.deactivate(Steering)
    else:
        cont.activate(Steering)
    if own['atacar'] < 3:
        if radar.positive:  
            o = radar.hitObject
           
            agarrar(cont,o)
def agarrar(cont,o):
    own = cont.owner
    pos_play = own.childrenRecursive.get('pos_play')

    if o :
        own['atackTime'] = 150
        own['agarrao'] = True
        status['agarrado'] = True
        o.worldPosition = pos_play.worldPosition
        
def alain(cont):
    own = cont.owner
    if own['atackTime'] >0:
        dir = own['pl_arm'][0].worldPosition - own.worldPosition
        own['pl_arm'][0].alignAxisToVect(dir, 1, 0.5)
        own['pl_arm'][0].alignAxisToVect([0,0,1], 2, 1.0)