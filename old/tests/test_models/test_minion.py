import league_utils.models as models


def test_equality():
    caster = models.Minion('Caster')
    assert caster == caster

    melee = models.Minion('Melee')
    assert caster != melee

    melee_copy = models.Minion('Melee')
    assert melee == melee_copy


def test_repr():
    assert str(models.Minion('Caster')) == '[caster]'


def test_first_spawn_order():
    caster = models.Minion('Caster')
    melee = models.Minion('Melee')
    siege = models.Minion('Siege')

    assert melee.first_spawn < caster.first_spawn < siege.first_spawn


def test_group_size():
    caster = models.Minion('Caster')
    melee = models.Minion('Melee')
    assert caster.group_size == melee.group_size == 3

    siege = models.Minion('Siege')
    assert siege.group_size == 1


def test_interval():
    times = [0, 15 * 60, 30 * 60, 45 * 60]

    caster = models.Minion('Caster')
    melee = models.Minion('Melee')
    for time in times:
        assert caster.interval(time) == 30
        assert melee.interval(time) == 30

    siege = models.Minion('Siege')
    assert siege.interval(times[0]) == 90
    assert siege.interval(times[1]) == 90
    assert siege.interval(times[2]) == 60
    assert siege.interval(times[3]) == 30


def test_speed():
    melee = models.Minion('Melee')
    assert melee.speed == 325

    bot = models.Lane('Bot')
    assert bot.nexus_to_center_time(melee.speed) == 33

    mid = models.Lane('Mid')
    assert mid.nexus_to_center_time(melee.speed) == 24
