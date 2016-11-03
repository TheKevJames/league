import math

import league_utils.models as models


FIRST_POKE = 120
PASSIVE_ENABLED = 75


def maximum_minion_kill(lane, time_current, kill_interval=0, kill_rate=1,
                        time_purchase=0):
    caster = models.Minion('caster')
    melee = models.Minion('melee')
    siege = models.Minion('siege')

    kill_gold = 0
    last_kill = time_purchase - kill_interval
    for time in range(time_purchase, time_current):
        if time < last_kill + kill_interval:
            continue

        minion = None
        for minion in (siege, melee, caster):
            available = minion.in_lane(lane, time) - \
                        minion.in_lane(lane, time - 1)
            if available:
                break
        else:
            continue

        kill_gold += minion.value(time)
        last_kill = time

    return kill_gold * kill_rate


def maximum_passively_generated_from_farm(lane, gold_per_farm, time_current,
                                          farm_rate=1, time_purchase=0):
    caster = models.Minion('caster').in_lane
    melee = models.Minion('melee').in_lane
    siege = models.Minion('siege').in_lane

    casters = caster(lane, time_current) - caster(lane, time_purchase)
    melees = melee(lane, time_current) - melee(lane, time_purchase)
    sieges = siege(lane, time_current) - siege(lane, time_purchase)
    farm = casters + melees + sieges

    return farm * gold_per_farm * farm_rate


def passively_generated(gold_per_ten, time_current, time_purchase=0):
    time_active = time_current - max(time_purchase, PASSIVE_ENABLED)
    return (max(0, time_active) // 10) * gold_per_ten


def passively_generated_bandit(lane, ranged, time_current, farm_rate=1,
                               poke_rate=1):
    farm = maximum_passively_generated_from_farm(lane, 1, time_current,
                                                 farm_rate=farm_rate)
    poke = poking(3 if ranged else 10, 1, 5, time_current, poke_rate=poke_rate)
    return farm + poke


def poking(gold_per_poke, charges, regen, time_current, poke_rate=1,
           time_purchase=0):
    time_active = time_current - max(time_purchase, FIRST_POKE)
    rate = regen / charges
    return max(0, math.ceil(time_active / rate)) * poke_rate * gold_per_poke
