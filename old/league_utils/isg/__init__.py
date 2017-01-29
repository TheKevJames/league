import league_utils.common as common
# TODO: aliasing breaks these lines. WTF?
import league_utils.isg.groups
import league_utils.isg.wants


def item_set(champ, role, items):
    biscuits = league_utils.isg.groups.biscuits()
    boots = league_utils.isg.groups.boots()
    wants = league_utils.isg.wants.tags(champ, role)

    consumables = league_utils.isg.groups.consumables()
    early = common.without(champ.starts[role], consumables, biscuits) + \
        league_utils.isg.wants.order(wants, boots)
    build = common.without(champ.builds[role], consumables, biscuits, early)
    options = common.without(league_utils.isg.wants.order(wants, items),
                             build, early, consumables)

    return (role.name, 'SR', champ.key,
            [('Early & Boots', common.dedup(early)),
             ('Build', common.dedup(build)),
             ('Options', common.dedup(options)[:10]),
             ('Consumables', consumables)])
