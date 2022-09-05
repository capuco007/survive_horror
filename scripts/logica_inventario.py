import bge
from bge.types import  *
from bge.logic import globalDict


####################################
### Estado inicial do globalDict ###
####################################

globalDict['game_status'] = {
    'level': 5,
    'chest': [],
    'inventory': [
        {
            'nome': 'pistola',
            'muni': 15,
        },
        {
            'nome': 'balas_pistola',
            'quant': 20,
        },
    ]
}

# Inventário
inventory = globalDict['game_status']['inventory']  # type: list[dict]

# Baú
chest = globalDict['game_status']['chest']  # type: list[dict]


#########################
### Funções genéricas ###
#########################

def itemExists(item, collection):
    # type: (dict, list[dict]) -> bool
    """Verifica se o item passado no parâmetro existe na coleção."""
    for invItem in collection:
        if item.get('nome') == invItem.get('nome'):
            return True
    return False


def itemAdd(item, collection):
    # type: (dict, list[dict]) -> None
    """Adiciona item na coleção."""

    # Adiciona na coleção caso item não exista ou não seja agrupável
    if not itemExists(item) or not item.get('quant'):
        collection.append(item)

    # Adiciona quantidade de item agrupável no item existente
    elif item.get('quant'):
        for invItem in collection:
            if item.get('nome') == invItem.get('nome'):
                invItem['quant'] += item['quant']


def itemRemove(idx, collection) -> dict:
    # type: (int, list[dict]) -> dict
    """Remove item da coleção a partir do índice e retorna este item."""
    if idx < len(collection):
        return collection.pop(idx)


#############################
### Pegar item no cenário ###
#############################

hitObject = None  # type: KX_GameObject
item = {}

# Pegar propriedades da instância de grupo do item
for prop in hitObject.groupObject.getPropertyNames():
    item[prop] = hitObject[prop]

# Item vira isso:
# item = {
#     'nome': 'balas_pistola',
#     'quant': 10,
# }

# Adicionar item no inventário
itemAdd(item, inventory)


###########################
### Remover item do baú ###
###########################

# Remover item no slot 3 na lista do baú e guardar este item na variável
item = itemRemove(3, chest)

# Adicionar item removido do baú no inventário
itemAdd(item, inventory)