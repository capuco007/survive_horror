from importlib.resources import path
import bge
from mathutils import Vector
from pathlib import Path



def start(cont):
    own = cont.owner
    gd = bge.logic.globalDict
    
    bge.logic.loadGlobalDict()
    gd.clear()
    #bge.logic.saveGlobalDict()
    own['arm'] = [arm for arm in own.childrenRecursive if 'player_arm' in arm]
    own['isMove'] = 0
    own['timeScene'] = 0
    own['fade'] = 0
    own['inventory'] = {
        'keys':['0'],
        'guns':[],
    }
    spwPos(cont)
    gd['pos'] = ''
    if 'itens' in gd:
        own['itens'] = gd['itens']
    else:
        own['itens'] = {}
    saveStatuts(cont)

def update(cont):
    own = cont.owner
    colisionDor(cont)
    movement(cont)
    inventory(cont)
    
    if own['fade'] >0:
        own['fade'] -= 1
    if own['timeScene'] >0:
        own['timeScene'] -= 1
    if own['timeScene'] == 1:
        bge.logic.sendMessage('clear_msg')

def movement(cont):
    own = cont.owner
    char = bge.constraints.getCharacter(own)
    tc = bge.logic.keyboard.inputs
    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    if own['fade'] == 0:
        char.walkDirection = Vector([x,y,0]).normalized()*0.08
    else:
        char.walkDirection = Vector([0,0,0])
    own['isMove'] = char.walkDirection
    
def moveDirection(cont):
    own = cont.owner

    if own['isMove']!= 0:
        pass

def colisionDor(cont):
    own = cont.owner
    Collision = cont.sensors['Collision']
    scn = own.scene
    tc = bge.logic.keyboard.inputs
    if Collision.positive:
        hit = Collision.hitObject
        DorHit = hit.groupObject['Name']
        objHit = hit.groupObject
        gd = bge.logic.globalDict
        if tc[bge.events.SPACEKEY].activated:
            hit = Collision.hitObject
            objHit = hit.groupObject
            if 'Name' in hit.groupObject and hit.groupObject['key'] in own['inventory']['keys']:
                DorHit = hit.groupObject['Name']
                objHit = hit.groupObject
                if objHit['active'] == False:
                    objHit['active'] = True
                    own['timeScene'] = 20
                    gd['msg'] = objHit['dor_msg']
                    
            else:
                if 'format_key' in objHit:
                    gd['msg'] = objHit['format_key']
                    
                else:
                    gd['msg'] = 'nokey'
                bge.logic.sendMessage('clear_msg')
            
            if objHit['active'] and own['timeScene'] == 0:
                #own['posSpw']['DorName'] = DorHit
                #own['gd']['posSpw'] = own['posSpw']
                #bge.logic.saveGlobalDict()
                if own['fade'] == 0:
                    own['fade'] = 50
        if own['fade'] == 1:
            gd['pos'] = objHit['location']
            
            bge.logic.saveGlobalDict()
            scn.replace(DorHit)
             
def camActive(cont):
    own = cont.owner

def loadStaus(cont):
    own = cont.owner
    from ast import literal_eval

    savegame = {}

    try:
        with open(bge.logic.expandPath('//save.txt'), 'r') as openedFile:
            savegame = literal_eval(openedFile.read())
            print('> Savegame carregado de', openedFile.name)
            own['inventory'] = savegame

    except Exception as e:
            print('X Savegame não existe', e)

def saveStatuts(cont):
    own = cont.owner
    own['inventory']['itens'] = own['itens']
    savegame = own['inventory']
    with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            openedFile.write(str(savegame))
            print('> Savegame salvo em', openedFile.name)

        

def spwPos(cont):
    own = cont.owner
    scene = own.scene.name
    gd = bge.logic.globalDict
    position = {
        'salao_1': [5,0,0],
        'salao_2': [-5,0,0],
        '_game_test': [0,-8,0]
    }
    if 'pos' in gd:
    
        own.worldPosition = position[gd['pos']]
    gd.clear()
    bge.logic.saveGlobalDict()
    
def dialogs(cont):
    own = cont.owner
    msg = cont.sensors['Message']
    gd = bge.logic.globalDict
    

    
    if own['time'] >0:
        own['time'] -= 1
    if own['time'] == 1:
        own['msg'] = None
        own.visible = False
    
    if msg.positive and own['time'] == 0:
        own['time'] = 100

    dor_msg = {
        'destravou': 'Você destravou esta porta',
        'nokey': 'Voce nao tem a chave !!',
        'format_key': 'Parece ter um formato de cruz na porta'
    }

    if 'msg' in gd:
        own.visible = True
        own['msg'] = dor_msg[gd['msg']]
        gd.clear()
    
def inventory(cont):
    own = cont.owner
    gd = bge.logic.globalDict
    Coll_Iten = cont.sensors['Coll_Iten']
    tc = bge.logic.keyboard.inputs
    if Coll_Iten.positive:
        obj = Coll_Iten.hitObject.groupObject
        objTipo = Coll_Iten.hitObject.groupObject['tipo']
        objquant = Coll_Iten.hitObject.groupObject['quant']
        
        if tc[bge.events.SPACEKEY].activated:
            if len(own['itens']) < 8:
                if objTipo in own['itens']:
                    if own['itens'][objTipo] < 99:
                        own['itens'][objTipo] += objquant
                        
                else:
                    own['itens'][objTipo] = objquant
                obj.endObject()
                gd['itens'] = own['itens']
                bge.logic.saveGlobalDict()
                #gd.clear()
    if 'itens' in gd:
        pass
        #print(gd['itens'])
   
  
    
    