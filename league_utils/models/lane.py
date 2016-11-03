class Lane(object):
    def __init__(self, name):
        self.name = name.lower()
        assert self.name in ('bot', 'mid', 'top')

    def __repr__(self):
        return '[{}]'.format(self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    @property
    def nexus_to_center_distance(self):
        if self.name == 'mid':
            return 7800

        return 10725

    def nexus_to_center_time(self, speed):
        return self.nexus_to_center_distance / speed
