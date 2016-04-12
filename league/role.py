class Role(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '[{}]'.format(self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
