import json


TAG = 'SFT'


def item_set(title, map_, champion, blocks):
    map_ = 'any'
    mode = 'any'
    # TODO: specify mode/map
    # if map_ == 'CS':
    #     mode = 'ODIN'
    # elif map_ == 'HA':
    #     mode = 'ARAM'
    # else:  # 'any', 'SR', or 'TA'
    #     mode = 'CLASSIC'
    #     # TODO: mode = 'any' ?

    return json.dumps({
        'title': '{} {}'.format(TAG, title),
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
            'items': [{'count': 1, 'id': item.id} for item in items],
        } for name, items in blocks],
    })
