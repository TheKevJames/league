class Map(object):
    def __init__(self, id_):
        self.id = int(id_)

        self.name, self.starting_gold, self.gold_per_ten = {
            1: ("Summoner's Rift (Summer)", 500, 20.4),
            2: ("Summoner's Rift (Autumn)", 500, 20.4),
            3: ('Proving Grounds', 0, 0),
            4: ('Twisted Treeline (Original)', 850, 16),
            8: ('Crystal Scar', 1300, 56),
            10: ('Twisted Treeline', 850, 16),
            11: ("Summoner's Rift", 500, 20.4),
            12: ('Howling Abyss', 1400, 50),
            14: ("Butcher's Bridge", 1400, 50),
        }[self.id]

    def __repr__(self):
        return '[{}]'.format(self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
