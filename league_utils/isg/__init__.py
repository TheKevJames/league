import league_utils.common as common
# TODO: aliasing breaks these lines. WTF?
import league_utils.isg.groups
import league_utils.isg.wants


def item_set(champ, role):
    biscuits = league_utils.isg.groups.biscuits()

    consumables = league_utils.isg.groups.consumables()
    early = common.without(champ.starts[role], consumables, biscuits) + \
            league_utils.isg.wants.order(
                league_utils.isg.wants.tags(champ, role),
                league_utils.isg.groups.boots())
    build = common.without(champ.builds[role], consumables, biscuits, early)

    return (role.name, 'SR', champ.key,
            [('Early & Boots', common.dedup(early)),
             ('Build', common.dedup(build)),
             ('Consumables', consumables)])
