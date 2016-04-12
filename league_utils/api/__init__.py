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
        raise Exception('could not find champion {}', champ_filter)

    return champs
