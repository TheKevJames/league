import collections
import operator


def get_wanted_order(wants, items):
    ratings = {item: sum(wants[tag] for tag in item.tags) for item in items}
    return [item for item, rating in sorted(ratings.items(),
                                            key=operator.itemgetter(1),
                                            reverse=True) if rating > 0]


def get_wants(tags_sets):
    wants = collections.Counter()
    for tags in tags_sets:
        wants.update(tags - set(['Active', 'Boots', 'Consumable', 'Jungle',
                                 'Lane', 'Trinket']))

    return wants
