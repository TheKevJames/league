import os


TOKEN = os.environ['RIOT_TOKEN']

API_STATIC_DATA = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2'
API_ITEMS = API_STATIC_DATA + '/item?itemData=all&api_key=' + TOKEN
API_ITEM = API_STATIC_DATA + '/item/{}?itemData=all&api_key=' + TOKEN


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
}

IW1 = {
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
IW2 = {
    'FlatMovementSpeedOutOfCombatMod': (900 - IW1['FlatMovementSpeedMod'] * 25) / (115 - 25),  # mobis - MS
    'FlatOnHitMod': (1000 - IW1['PercentAttackSpeedMod'] * 0.25) / 15,  # recurve bow - AS
    'PercentArmorPenetrationMod': (1300 - IW1['FlatPhysicalDamageMod'] * 25) / 0.3,  # last whisper - AD
    'PercentCooldownMod': (800 - IW1['FlatHPPoolMod'] * 200) / 0.10,  # kindlegem - HP
    'PercentLifeStealMod': (900 - IW1['FlatPhysicalDamageMod'] * 15) / 0.10,  # vampiric sceptre - AD
    'PercentMagicPenetrationMod': (1100 - IW1['FlatMovementSpeedMod'] * 45) / 0.15,  # sorcerer's shoes - MS
    'PercentMovementSpeedMod': (850 - IW1['FlatMagicDamageMod'] * 30) / 0.05,  # aether wisp - AP
}
IW2F = {
    'FlatHPRegenMod': (450 - IW1['FlatHPPoolMod'] * 80) / 1.2,  # doran's shield - HP
    'FlatLifeOnHitMod': (450 - IW1['FlatPhysicalDamageMod'] * 7) / 3,  # cull - AD
    'PercentHPPoolMod': (2625 - IW1['FlatHPPoolMod'] * 400) / 0.15,  # cinderhulk - HP
}
IW3 = {
    'FlatLethalityMod': (1100 - IW1['FlatPhysicalDamageMod'] * 25 - IW2['FlatMovementSpeedOutOfCombatMod'] * 20) / 10,  # serrated dirk - AD - MSOOC
    'FlatMagicPenetrationMod': (1500 - IW1['FlatMagicDamageMod'] * 25 - IW1['FlatHPPoolMod'] * 200) / 15,  # haunting guise - AP - HP
}
IWARB = {
    'FlatMPRegenMod': 10,  # guardian's orb - HP - AP (too good!)
    'FlatMPRegenPer5Mod': 10 / 5,  # FlatMPRegenMod / 5
    'FlatOnHitJungleMod': 0.75 * IW2['FlatOnHitMod'],
    'PercentIncreasedPotionMod': 5 * 50,  # 5 potions, 50gp each
    'PercentLifeStealJungleMod': 0.75 * IW2['PercentLifeStealMod'],
    'PercentMPRegenJungleMod': 0.75 * IW1['PercentMPRegenMod'],
    'ScalingFlatMagicDamageMod': IW1['FlatMagicDamageMod'] / 8,  # from flat, lvl 8 x-over
    'ScalingFlatMPPoolMod': IW1['FlatMPPoolMod'] / 8,  # from flat, lvl 8 x-over
}
IWMISSING = {
    'FlatGoldPer10Mod': 0,
    'PercentDamageReductionCritMod': 0,
    'PercentHealAndShieldMod': 0,
}

ITEM_WORTH = {
    **IW1,
    **IW2,
    **IW2F,
    **IW3,
    **IWARB,
    **IWMISSING,
}
