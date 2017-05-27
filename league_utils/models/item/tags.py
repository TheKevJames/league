import logging


logger = logging.getLogger()


def get_missing_tags(iid, name):
    # pylint: disable=too-many-return-statements
    if 'Biscuit of Rejuvenation' in name:
        return {'Consumable', 'HealthRegen', 'ManaRegen'}

    if "Death's Daughter" in name:
        return {'Damage', 'Slow'}
    if 'Fire at Will' in name:
        return {'AttackSpeed', 'Damage'}
    if 'Raise Morale' in name:
        return {'NonbootsMovement'}

    if 'Hex Core' in name:
        return {'Mana', 'SpellDamage'}

    if 'Enchantment' in name:
        if 'Bloodrazor' in name:
            return {'AttackSpeed', 'Jungle', 'OnHit'}
        elif 'Cinderhulk' in name:
            return {'Aura', 'Health', 'Jungle', 'SpellDamage'}
        elif 'Runic Echoes' in name:
            return {'Jungle', 'NonbootsMovement', 'SpellDamage'}
        elif 'Warrior' in name:
            return {'CooldownReduction', 'Damage', 'Jungle'}

    if name in ('Dark Matter Scythe', 'Dark Star Sigil', 'Cloak of Stars',
                'Cosmic Shackle', 'Entropy Field', 'Flash Zone',
                'Gravity Boots', 'Nexus Siege: Siege Weapon Slot', 'Port Pad',
                'Shield Totem', 'Siege Ballista', 'Siege Refund',
                'Siege Sight Warder', 'Siege Teleport',
                'Siege Teleport (Inactive)', 'Siege Warp',
                'Siege Warp (Inactive)', 'Singularity Lantern',
                'Tower: Beam of Ruination', 'Tower: Storm Bulwark',
                'Tower Surge: Beam of Ruination',
                'Tower Surge: Firestorm Bulwark', 'Vanguard Banner',
                'Diet Poro-Snax', 'Poro-Snax', 'unknown-item'):
        return {}

    logger.error('item %s has no tags', iid)
    return {}


async def build_tags(payload):
    name = payload.get('name', 'unknown-item')

    try:
        tags = set(payload['tags']) - {'Bilgewater'}
        if name in ('Boots of Mobility', 'Boots of Swiftness'):
            # Champions that really want movement speed should consider these
            # boots.
            tags.add('NonbootsMovement')
        return tags
    except KeyError:
        iid = payload.get('id', '')
        return get_missing_tags(iid, name)
