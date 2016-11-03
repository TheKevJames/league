MIN20 = 20 * 60
MIN35 = 35 * 60


class Minion(object):
    def __init__(self, name):
        self.name = name.lower()
        assert self.name in ('caster', 'melee', 'siege')

        self.speed = 325

    def __repr__(self):
        return '[{}]'.format(self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    @property
    def first_spawn(self):
        return {
            'caster': 90,
            'melee':  75,
            'siege':  135,
        }[self.name]

    @property
    def group_size(self):
        return {
            'caster': 3,
            'melee':  3,
            'siege':  1,
        }[self.name]

    def in_lane(self, lane, time):
        return self.spawned(time - lane.nexus_to_center_time(self.speed))

    def interval(self, time=0):
        return {
            'caster': 30,
            'melee':  30,
            'siege':  30 if time > MIN35 else 60 if time > MIN20 else 90,
        }[self.name]

    def intervals(self, time_current, time_first_spawn):
        interval = self.interval(time_current)
        return (time_current - time_first_spawn + interval) // interval

    def spawned(self, time):
        if self.name == 'siege':
            spawn_count = 0

            if time > MIN35:
                intervals = self.intervals(time, MIN35 + 15)
                spawn_count += max(0, intervals * self.group_size)

                time = MIN35

            if time > MIN20:
                intervals = self.intervals(time, MIN20 + 15)
                spawn_count += max(0, intervals * self.group_size)

                time = MIN20

            intervals = self.intervals(time, self.first_spawn)
            spawn_count += max(0, intervals * self.group_size)
            return spawn_count

        intervals = self.intervals(time, self.first_spawn)
        return max(0, intervals * self.group_size)

    def value(self, time):
        return {
            'caster': 17.5 + (0.125 * (time // 90)),
            'melee':  20.5 + (0.125 * (time // 90)),
            'siege':  45.5 + (0.350 * (time // 90)),
        }[self.name]
