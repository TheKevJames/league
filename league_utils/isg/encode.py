import json


def item_set(title, map_, champion, blocks):
    mode = 'any'
    if map_ == 'CS':
        mode = 'ODIN'
    elif map_ == 'HA':
        mode = 'ARAM'
    else:
        mode = 'CLASSIC'

    return json.dumps({
        'title': '{} (auto-generated)'.format(title),
        'map': map_,
        'mode': mode,

        'type': 'custom',
        'sortrank': 1,
        'priority': False,

        'isGlobalForChampions': False,
        'associatedChampions': list(),
        'associatedMaps': [],
        'isGlobalForMaps': True,
        'champion': champion,

        'blocks': [{
            'type': name,
            'items': [{'count': 1, 'id': str(item.id)} for item in items],
        } for name, items in blocks],
    })
