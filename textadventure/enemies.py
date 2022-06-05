class Enemies:
    def __init__(self, hp, max_hp, ad, name):
        self.hp = hp
        self.max_hp = max_hp
        self.ad = ad
        self.name = name

    def is_dead(self):
        return self.hp <= 0

    def die(self):
        print(self.name + " died")


class Grootslang(Enemies):
    def __init__(self):
        Enemies.__init__(self, 250, 250, 50, "Grootslang")
        self.desc = "huge elephant - sized serpent the cave is filled with diamonds."



class Kongamato(Enemies):
    def __init__(self):
        Enemies.__init__(self, 300, 300, 70, "Kongamato")
        self.desc = "is described as a flying reptile we may recognize as a pterosaur."


class Impundulu(Enemies):
    def __init__(self):
        Enemies.__init__(self, 350, 350, 90, "Impundulu")
        self.desc = "supernatural bird."


class NinkiNanka(Enemies):
    def __init__(self):
        Enemies.__init__(self, 1000, 1000, 99, "Ninki Nanka")
        self.desc = "It is a dragon-like creature with the body of a crocodile, the head of a horse (with horns) and" \
                     "a long neck like a giraffe."


class Men:
    def __init__(self):
        self.name = "Men"

