import bge
def start(cont):
    own = cont.owner
    scene = own.scene
    own['pl'] = [o for o in scene.objects if 'player' in o]
    own['m'] = [o for o in scene.objects if 'mesh' in o]
    own['is_mov'] = False
def update(cont):
    own = cont.owner
    Steering = cont.actuators['Steering']
    colision = cont.sensors['Collision']
    z_arm = own.childrenRecursive.get('z_arm')
    if own['m']:
        Steering.navmesh = own['m'][0]
        if own['pl']:
            Steering.target = own['pl'][0]

            cont.activate(Steering)
            own['is_mov'] = True
    


