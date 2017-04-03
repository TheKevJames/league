import asyncio
import logging
import re

from ...monitor import SENTRY


HTML_TAG = re.compile('<[^<]+?>')
ON_HIT = re.compile(
    r'basic attacks deal(?: an additional)? (.*?)(?: (?:as|in))?(?: bonus)?'
    r'(?: (?:magic|physical))? damage(?: .*?)?(?: (?:on hit|vs\. monsters)).*')

ITEM_DESCRIPTION_STAT_KEYS = {
    'Ability Power per level': 'Scaling{}MagicDamageMod',
    'Ability Power': '{}MagicDamageMod',
    'Armor': '{}ArmorMod',
    'Attack Damage': '{}PhysicalDamageMod',
    'Attack Speed': '{}AttackSpeedMod',
    'Base Attack Damage': '{}PhysicalDamageMod',
    'Base Health Regen': '{}HPRegenMod',
    'Base Health Regeneration': '{}HPRegenMod',
    'Base Mana Regen while in Jungle': '{}MPRegenJungleMod',
    'Base Mana Regen': '{}MPRegenMod',
    'Bonus Health': '{}HPPoolMod',
    'Heal and Shield Power': '{}HealAndShieldMod',
    'increased cooldown': '{}CooldownMod',  # I would have assumed this should
                                            # be negative... but no. See i#3363
    'Cooldown Reduction': '{}CooldownMod',
    'Critical Strike Chance': '{}CritChanceMod',
    'Damage taken from Critical Strikes': '{}DamageReductionCritMod',
    'Gold per 10 seconds': '{}GoldPer10Mod',
    'Health': '{}HPPoolMod',
    'Increased Healing from Potions': '{}IncreasedPotionMod',
    'Lethality': '{}LethalityMod',
    'Life on Hit': '{}LifeOnHitMod',
    'Life Steal vs. Monsters': '{}LifeStealJungleMod',
    'Life Steal': '{}LifeStealMod',
    'Magic Penetration': '{}MagicPenetrationMod',
    'Magic Resist': '{}SpellBlockMod',
    'Mana per level': 'Scaling{}MPPoolMod',
    'Mana regen per 5 seconds': '{}MPRegenPer5Mod',
    'Mana': '{}MPPoolMod',
    'Movement Speed': '{}MovementSpeedMod',
    'Movement Speed out of Combat': '{}MovementSpeedOutOfCombatMod',
    'Bonus Armor Penetration': '{}ArmorPenetrationMod',
    'reduced ward vision radius': '{}WardVisionMod',
}

logger = logging.getLogger()


def parse_value(value):
    if '%' in value:
        return 'Percent', float(value[1:-1]) / 100

    return 'Flat', float(value[1:])


def parse_onhit(onhit):
    dvalue = ON_HIT.match(onhit).groups()[0]
    if 'of ability power' in onhit:
        flat, percent, _ = dvalue.split(' ', 2)
        value = int(percent[2:-1]) / 100
        value *= 100
        value += int(flat)
    elif "target's current health" in onhit:
        value = int(dvalue.split(' ', 1)[0][:-1]) / 100
        value *= 2000
    elif "target's maximum health" in onhit:
        value = int(dvalue.split(' ', 1)[0][:-1]) / 100
        value *= 1250
    elif 'total attack damage' in onhit:
        low, _, high, _ = dvalue.split(' ', 3)
        value = ((int(low[:-1]) + int(high[:-1])) / 2) / 100
        value *= 125
    elif 'your maximum health' in onhit:
        flat, _, percent, _ = dvalue.split(' ', 3)
        value = int(percent[:-1]) / 100
        value *= 2500
        value += int(flat)
    else:
        value = int(dvalue)

    if 'vs. monster' in onhit:
        return {'FlatOnHitJungleMod': value}
    else:
        return {'FlatOnHitMod': value}


async def parse_single_chunk(description):
    if '<' in description:
        description = HTML_TAG.sub('', description)
    description = description.strip(' .')

    dvalue, dkey = description.split(' ', 1)
    if dvalue in ('-', '+'):
        # bullets, see i#3363 "Farsight Alteration"
        # dvalue, dkey = (dvalue + dkey).split(' ', 1)
        return ({}, {description: ''})

    try:
        kind, value = parse_value(dvalue)
        key = ITEM_DESCRIPTION_STAT_KEYS[dkey].format(kind)
        return ({key: value}, {})
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(e)
        SENTRY.captureException()
        return ({}, {dkey: dvalue})


async def parse_chunk(title, description):
    if '<' in description:
        description = HTML_TAG.sub('', description)
    description = description.strip(' .')

    if description.startswith('+'):
        stats = {}
        dvalue, dkey = description.split(' ', 1)
        try:
            # TODO: parse this properly
            dkey, dextra = dkey.split('. ', 1)
            # dextra = 'Increases to +115 Movement Speed when out of combat '
            #          'for 5 seconds.'
            if dextra.startswith('Increases to +115 Movement'):
                stats = {'FlatMovementSpeedOutOfCombatMod': 90}  # 115 - 25
        except ValueError:
            pass

        try:
            kind, value = parse_value(dvalue)
            key = ITEM_DESCRIPTION_STAT_KEYS[dkey].format(kind)
            stats[key] = value
            return (stats, {})
        except Exception as e:  # pylint: disable=broad-except
            logger.exception(e)
            SENTRY.captureException()
            return (stats, {dkey: dvalue})

    if description.startswith('Basic attacks deal'):
        dvalue = ON_HIT.match(description.lower()).groups()[0]
        try:
            return (parse_onhit(description.lower()), {})
        except Exception as e:  # pylint: disable=broad-except
            logger.exception(e)
            SENTRY.captureException()
            return ({}, {'OnHit': dvalue})

    if description.startswith('Restores'):
        try:
            _, dvalue, dkey = description.split(' ', 2)
            if dkey == 'Health every 5 seconds':
                return ({'FlatHPRegenMod': float(dvalue) / 5}, {})
        except Exception as e:  # pylint: disable=broad-except
            logger.exception(e)
            SENTRY.captureException()

    title = title.strip(':')
    logger.info('Could not parse description chunk %s:%s', title, description)
    return ({}, {title: description})


async def build_stats_block(chunk, start='<stats>', end='</stats>', br='<br>'):
    if '<stats>' not in chunk:
        return {}, {}

    idx = chunk.find(start) + len(start)
    idx_end = chunk.find(end, idx)
    if idx_end == -1:
        idx_end = None

    stats = chunk[idx:idx_end]

    futures = [asyncio.ensure_future(parse_single_chunk(x))
               for x in stats.split(br)
               if x and 'Limit>' not in x]
    if not futures:
        return {}, {}

    done, _ = await asyncio.wait(futures)

    parsed_stats, unparseable_stats = {}, {}
    for stats in done:
        success, fail = await stats
        parsed_stats = {**parsed_stats, **success}
        unparseable_stats = {**unparseable_stats, **fail}

    return parsed_stats, unparseable_stats

async def build_stats_from_chunk(chunk, start, end, br='<br>'):
    # pylint: disable=too-many-locals
    futures = []
    idx = -1
    while True:
        idx = chunk.find(start, idx + 1)
        if idx == -1:
            break

        idx_mid = chunk.find(end, idx)
        idx_end = chunk.find(br, idx_mid)
        if idx_end == -1:
            idx_end = None

        title = chunk[idx + len(start):idx_mid]
        description = chunk[idx_mid + len(end):idx_end]
        futures.append(asyncio.ensure_future(parse_chunk(title, description)))

    if not futures:
        return {}, {}

    done, _ = await asyncio.wait(futures)

    parsed_stats, unparseable_stats = {}, {}
    for stats in done:
        success, fail = await stats
        parsed_stats = {**parsed_stats, **success}
        unparseable_stats = {**unparseable_stats, **fail}

    return parsed_stats, unparseable_stats


async def build_stats(description):
    done, _ = await asyncio.wait([
        asyncio.ensure_future(build_stats_from_chunk(
            description, '<active>', '</active>')),
        asyncio.ensure_future(build_stats_from_chunk(
            description, '<aura>', '</aura>')),
        asyncio.ensure_future(build_stats_from_chunk(
            description, '<consumable>', '</consumable>')),
        asyncio.ensure_future(build_stats_from_chunk(
            description, '<passive>', '</passive>')),
        asyncio.ensure_future(build_stats_from_chunk(
            description, '<br><unlockedPassive>', '</unlockedPassive>')),
        asyncio.ensure_future(build_stats_from_chunk(
            description, '<unique>', '</unique>')),
        asyncio.ensure_future(build_stats_block(description)),
    ])

    parsed_stats, unparseable_stats = {}, {}
    for stats in done:
        success, fail = await stats
        parsed_stats = {**parsed_stats, **success}
        unparseable_stats = {**unparseable_stats, **fail}

    return parsed_stats, unparseable_stats
