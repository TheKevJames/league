import json

import league_utils.common as common
# TODO: aliasing breaks these lines. WTF?
import league_utils.isg.encode
import league_utils.isg.groups
import league_utils.isg.wants


def item_set(champ, role):
    early = common.without(champ.starts[role],
                           league_utils.isg.groups.consumables(1)) + \
            league_utils.isg.wants.order(
                league_utils.isg.wants.tags(champ, role),
                league_utils.isg.groups.boots())
    build = common.without(champ.builds[role],
                           league_utils.isg.groups.consumables(1), early)

    data = league_utils.isg.encode.item_set(
        role.name, 'SR', champ.key,
        [league_utils.isg.encode.block('Consumables',
                                       league_utils.isg.groups.consumables()),
         league_utils.isg.encode.block('Early & Boots', early),
         league_utils.isg.encode.block('Build', build)])

    return json.dumps(data)
