import os

import riotwatcher


try:
    token = os.environ['LEAGUE_TOKEN']
except KeyError:
    raise Exception('No LEAGUE_TOKEN found. See developer.riotgames.com')
riot = riotwatcher.RiotWatcher(token)


def get_champ(champ_filter=None):
    champs = []
    for champ in riot.static_get_champion_list()['data'].values():
        champs.append(dict(id=champ['id'], key=champ['key'],
                           name=champ['name']))
        if not champ_filter:
            continue

        if champ_filter == champ['name'].lower():
            return champs[-1:]

    if champ_filter:
        raise Exception('Could not find champion {}', champ_filter)

    return champs


def get_item(item_filter=None):
    items = []
    for item in riot.static_get_item_list()['data'].values():
        if 'name' not in item:
            # Weird API response is weird.
            # {'group': 'RelicBase', 'id': 3462}
            continue

        items.append(dict(id=item['id'], name=item['name']))
        if not item_filter:
            continue

        if item_filter == item['name'].lower():
            return items[-1:]

    if item_filter:
        raise Exception('Could not find item {}', item_filter)

    return items
