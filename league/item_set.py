def make_block(name, items):
    return {
        'type': name,
        'items': [{'count': 1, 'id': item.id} for item in items],
    }


def make_set(title, map_, champion, blocks):
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

    return {
        'title': 'SFT {}'.format(title),
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

        'blocks': blocks,
    }
