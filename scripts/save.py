def save(self):
        savegame = {
            'player': {
                'GunList': self.object['GunList'],
                'life': self.life,
                'cash': self.cash,
                'recargEstam': self.recargEstam,
                'position': list(self.object.worldPosition),
                'activeDash': self.activeDash,
                'keys': self.key
            },
            'objects': [],
        }

        for o in self.object.scene.objects:
            if 'save' in o:
                savegame['objects'].append(o.name)
            if 'dor' in o:
                
                for prop in o.getPropertyNames():
                    savegame[o.name] = o[prop]

            if 'openDor' in o:
                for prop in o.getPropertyNames():
                    savegame[o.name] = o[prop]

        
            

        with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            openedFile.write(str(savegame))
            print('> Savegame salvo em', openedFile.name)

def load(self):
    from ast import literal_eval

    savegame = {}

    try:
        with open(bge.logic.expandPath('//save.txt'), 'r') as openedFile:
            savegame = literal_eval(openedFile.read())
            print('> Savegame carregado de', openedFile.name)
    except Exception as e:
        print('X Savegame não existe', e)
