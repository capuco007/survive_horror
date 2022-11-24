from ast import literal_eval
from builtins import print
from xml.etree.ElementTree import TreeBuilder
import bge
from mathutils import Vector
from .inventory  import *
from bge.logic import globalDict as gd



def load(cont):
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

def save(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    from pprint import pformat


    #save

    
    gd['save_ram']['player_position'] = own.worldPosition
    gd['save_ram']['last_scene'] = own.scene.name
    with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
        openedFile.write(pformat(gd['save_ram']))
        print('> Savegame salvo em', openedFile.name)
    with open(bge.logic.expandPath('//save_pl.txt'), 'w') as openedFile:
        openedFile.write(pformat(gd['game_status']))
        print('> Savegame salvo em', openedFile.name)