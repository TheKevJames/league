import collections
import operator


UNWANTED_TAGS = ['Active', 'Boots', 'Consumable', 'Jungle', 'Lane', 'Trinket']


def order(wants, items):
    ratings = {item: sum(wants[tag] for tag in item.tags) for item in items}
    return [item for item, rating in sorted(ratings.items(),
                                            key=operator.itemgetter(1),
                                            reverse=True) if rating > 0]


def tags(champ, role):
    wanted_tags = collections.Counter()
    for build_tags in [build.tags for build in champ.builds[role]]:
        wanted_tags.update(build_tags - set(UNWANTED_TAGS))

    return wanted_tags
