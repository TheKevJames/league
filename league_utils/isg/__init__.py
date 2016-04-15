import league_utils.common as common
# TODO: aliasing breaks these lines. WTF?
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

    return (role.name, 'SR', champ.key,
            [('Consumables', league_utils.isg.groups.consumables()),
             ('Early & Boots', common.dedup(early)),
             ('Build', common.dedup(build))])
