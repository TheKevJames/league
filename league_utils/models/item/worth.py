BASE_VALUES = {
    'FlatArmorMod': 300 / 15,  # cloth armor
    'FlatHPPoolMod': 400 / 150,  # ruby crystal
    'FlatMagicDamageMod': 435 / 20,  # amplifying tome
    'FlatMovementSpeedMod': 300 / 25,  # boots of speed
    'FlatMPPoolMod': 350 / 250,  # sapphire crystal
    'FlatPhysicalDamageMod': 350 / 10,  # long sword
    'FlatSpellBlockMod': 450 / 25,  # null-magic mantle
    'PercentAttackSpeedMod': 300 / 0.12,  # dagger
    'PercentCritChanceMod': 400 / 0.10,  # brawler's gloves
    'PercentHPRegenMod': 150 / 0.5,  # rejuvenation bead
    'PercentMPRegenMod': 125 / 0.25,  # faerie charm
}
DERIVED_TIER2 = {
    'FlatMovementSpeedOutOfCombatMod':
        # mobis - MS
        (900 - BASE_VALUES['FlatMovementSpeedMod'] * 25) / (115 - 25),
    'FlatOnHitMod':
        # recurve bow - AS
        (1000 - BASE_VALUES['PercentAttackSpeedMod'] * 0.25) / 15,
    'PercentArmorPenetrationMod':
        # last whisper - AD
        (1300 - BASE_VALUES['FlatPhysicalDamageMod'] * 25) / 0.3,
    'PercentCooldownMod':
        # kindlegem - HP
        (800 - BASE_VALUES['FlatHPPoolMod'] * 200) / 0.10,
    'PercentLifeStealMod':
        # vampiric sceptre - AD
        (900 - BASE_VALUES['FlatPhysicalDamageMod'] * 15) / 0.10,
    'PercentMagicPenetrationMod':
        # sorcerer's shoes - MS
        (1100 - BASE_VALUES['FlatMovementSpeedMod'] * 45) / 0.15,
    'PercentMovementSpeedMod':
        # aether wisp - AP
        (850 - BASE_VALUES['FlatMagicDamageMod'] * 30) / 0.05,
}
DERIVED_TIER2_FUZZY = {
    'FlatHPRegenMod':
        # doran's shield - HP
        (450 - BASE_VALUES['FlatHPPoolMod'] * 80) / 1.2,
    'FlatLifeOnHitMod':
        # cull - AD
        (450 - BASE_VALUES['FlatPhysicalDamageMod'] * 7) / 3,
    'PercentHPPoolMod':
        # cinderhulk - HP
        (2625 - BASE_VALUES['FlatHPPoolMod'] * 400) / 0.15,
}
DERIVED_TIER3 = {
    'FlatLethalityMod':
        # serrated dirk - AD - MSOOC
        (1100 - BASE_VALUES['FlatPhysicalDamageMod'] * 25
         - DERIVED_TIER2['FlatMovementSpeedOutOfCombatMod'] * 20) / 10,
    'FlatMagicPenetrationMod':
        # haunting guise - AP - HP
        (1500 - BASE_VALUES['FlatMagicDamageMod'] * 25
         - BASE_VALUES['FlatHPPoolMod'] * 200) / 15,
    'PercentHealAndShieldMod':
        # forbidden idol - MPR% - CDR
        (800 - BASE_VALUES['PercentMPRegenMod'] * 0.5
         - DERIVED_TIER2['PercentCooldownMod'] * 0.1) / 0.08,
}
ARBITRARY = {
    'FlatMPRegenMod': 10,  # guardian's orb - HP - AP (too good!)
    'FlatMPRegenPer5Mod': 10 / 5,  # FlatMPRegenMod / 5
    'FlatOnHitJungleMod': 0.75 * DERIVED_TIER2['FlatOnHitMod'],
    'PercentIncreasedPotionMod': 5 * 50,  # 5 potions, 50gp each
    'PercentLifeStealJungleMod': 0.75 * DERIVED_TIER2['PercentLifeStealMod'],
    'PercentMPRegenJungleMod': 0.75 * BASE_VALUES['PercentMPRegenMod'],
    'ScalingFlatMagicDamageMod':
        BASE_VALUES['FlatMagicDamageMod'] / 8,  # from flat, lvl 8 x-over
    'ScalingFlatMPPoolMod':
        BASE_VALUES['FlatMPPoolMod'] / 8,  # from flat, lvl 8 x-over
}
VOID = {
    'FlatGoldPer10Mod': 0,
    'PercentDamageReductionCritMod': 0,
    'PercentPhysicalDamageMod': 0,
    'PercentWardVisionMod': 0,
}

ITEM_WORTH = {
    **BASE_VALUES,
    **DERIVED_TIER2,
    **DERIVED_TIER2_FUZZY,
    **DERIVED_TIER3,
    **ARBITRARY,
    **VOID,
}


def calculate_worth(stats):
    return sum(ITEM_WORTH[k] * v for k, v in stats.items())


def split_stats(stats):
    ignored, included = {}, {}
    for stat, value in stats.items():
        if ITEM_WORTH[stat] == 0:
            ignored[stat] = value
        else:
            included[stat] = value

    return ignored, included
