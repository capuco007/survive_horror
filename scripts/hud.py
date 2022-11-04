import bge
gd = bge.logic.globalDict
status: dict = gd['game_status']
def msg(cont):
    own = cont.owner
    conta_balas(cont)
    life_bar(cont)
    msg = status['exib_msg']

    if msg != 'none':
        own['msg'] = msg

    else:
        own['msg'] = ''

    if status['scene'] !='':
        transicao_scene(cont)

def transicao_scene(cont):
    own = cont.owner
    scene = own.scene
    fading_hud = scene.objects['fading_hud']
    fading_hud.playAction('fadingAction_scene',0,20,play_mode = 0)
    frame = fading_hud.getActionFrame(0)
    print(frame,status['scene'])
    if frame > 10 and frame < 12:
        status['scene_pass'] = True

def conta_balas(cont):
    own = cont.owner
    
    arma = status['player']['arma_mao']
    if arma:
        if arma != 'faca':
            own['balas'] = status['player']['bala_'+arma]
        else:
            own['balas'] = '%'
            
def life_bar(cont):
    own = cont.owner
    scene = own.scene
    life_pl = status['player']['saude']
    life = scene.objects['life']
    life['life'] = life_pl
    life.playAction('life',life_pl,life_pl)
    
