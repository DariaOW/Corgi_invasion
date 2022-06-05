import random
from player import Character, Jackrabbit, Snake, Turtle, Jackal, Hyena, Ferret
from enemies import Grootslang, Kongamato, Impundulu, NinkiNanka, Men
from pathlib import Path
from items import Item, HealthPotion, BauleMask, KweleMask, TekeMask, KotaMask


class Field:
    def __init__(self, enemies, loot):
        self.enemies = enemies
        self.loot = loot

    @staticmethod
    def enemies_random(g_class):
        r = random.random()
        if g_class.name == "Ferret":
            items_to_found = ([HealthPotion()], [BauleMask()], [], [])
        else:
            items_to_found = ([HealthPotion()], [BauleMask()], [],[],[], [])
        random_loot = random.choice(items_to_found)
        if r < 0.30:
            return Field([Grootslang()], random_loot)
        elif r < 0.60:
            return Field([Kongamato()], random_loot)
        elif r < 0.80:
            return Field([Impundulu()], random_loot)
        elif r < 0.90:
            return Field([NinkiNanka()], random_loot)
        else:
            return Field([], random_loot)

    def print_state(self):
        if len(self.enemies) > 0:
            for i in self.enemies:
                n = i.name
                if i.name == "Men":
                    print(f"You look around and see {n}.You won")
                    exit()
                else:
                    desc = str(self.enemies[0].desc) + "\nhis hp "+ str(self.enemies[0].hp) + \
                    "\n" + "his damage " + str(self.enemies[0].ad)
                    n = n + ".\n" + desc
        else:
            n = "only a desert. You are alone"
        print(f'You look around and see {n} ')
        if len(self.loot) > 0:
            for i in self.loot:
                l = i.name
            print(f'And luckily {l} lies in the shadow.Its weigth is {i.weight}')


class Map:
    def __init__(self, width, height, g_class):
        self.state = []
        self.coordinates = []
        self.escape_try = True
        self.x = 0
        self.y = 0
        for i in range(width):
            fields = []
            for j in range(height):
                fields.append(Field.enemies_random(g_class))

            self.random_index = random.randint(0, len(fields) - 1)
            fields[self.random_index] = Field([Men()], [])
            self.state.append(fields)
            self.men_field_to_aimap()





    def get_enemies(self):
        if self.x == 0 and self.y == 0:
            return []
        else:
            return self.state[self.x][self.y].enemies
    def get_items(self):
        if self.x == 0 and self.y == 0:
            return []
        else:
            return self.state[self.x][self.y].loot

    def get_loot_from_enemies(self, enemies, g_class):
        r = random.random()
        lfe = {"Kongamato": KweleMask(), "Impundulu": TekeMask(), "Ninki Nanka": KotaMask()}
        if enemies[0].name in lfe:
            if (g_class.name == "Ferret" and r < 0.88) or r < 0.40:
                self.state[self.x][self.y].loot.append(lfe.get(enemies[0].name))
                print(f"Wow your enemy has lost {lfe.get(enemies[0].name).name}")

    def save_coordinates_for_escape(self):
        if self.coordinates:
            self.coordinates.pop()
            self.coordinates.pop()
        self.coordinates.append(self.x)
        self.coordinates.append(self.y)

    def men_field_to_aimap(self):
        return self.random_index


    def print_state(self):
        print(f"your coordinates are {self.x, self.y}")
        if self.x == 0 and self.y == 0:
            print("Thus, you are at the start, here is safe")
        else:
            self.state[self.x][self.y].print_state()

    def print_endofrange(self):
        print(f"You see huge mountains, which you can't pass. your coordinates are still  {self.x, self.y}")
        if self.x == 0 and self.y == 0:
            print("Thus, you are at the start, here is safe")
        else:
            self.state[self.x][self.y].print_state()

    def free_move(self, g_class):
        if self.get_enemies():
            if len(g_class.mask) > 0 and g_class.mask[0].name == "Teke Mask" and self.get_enemies()[0].name == "Impundulu": ## mal gucken
                return False
            if g_class.name == "Jackrabbit":
                r = random.random()
                if r < 0.70:
                    return False
            return True
        else:
            return False

    def turtle_update_check(self, g_class):
        if g_class == Turtle():
            g_class.update_skill()

    def forward(self, g_class, ai_m):
        if self.free_move(g_class):
            print("You can not escape, Fight!")
            return
        elif self.x == len(self.state) - 1:
            self.print_endofrange()
        else:
            self.save_coordinates_for_escape()
            self.x = self.x + 1
            ai_m.ai_random_move()
            self.turtle_update_check(g_class)
            self.escape_try = True
            self.print_state()

    def backwards(self, g_class, ai_m):
        if self.free_move(g_class):
            print("You can not escape, Fight!")
            return
        elif self.x == 0:
            self.print_endofrange()
        else:
            self.save_coordinates_for_escape()
            self.x = self.x - 1
            ai_m.ai_random_move()
            self.turtle_update_check(g_class)
            self.escape_try = True
            self.print_state()

    def right(self, g_class, ai_m):
        if self.free_move(g_class):
            print("You can not escape, Fight!")
            return
        elif self.y == len(self.state[self.x]) - 1:
            self.print_endofrange()
        else:
            self.save_coordinates_for_escape()
            self.y = self.y + 1
            ai_m.ai_random_move()
            self.turtle_update_check(g_class)
            self.escape_try = True
            self.print_state()

    def left(self, g_class, ai_m):
        if self.free_move(g_class):
            print("You can not escape, Fight!")
            return
        elif self.y == 0:
            self.print_endofrange()
        else:
            self.save_coordinates_for_escape()
            self.y = self.y - 1
            ai_m.ai_random_move()
            self.turtle_update_check(g_class)
            self.escape_try = True
            self.print_state()

    def escape(self, g_class, ai_m):
        if self.escape_try:
            r = random.random()
            if r < 0.60:
                if not self.coordinates:
                    print("You can not escape one after another")
                else:
                    self.y = self.coordinates.pop()
                    self.x = self.coordinates.pop()
                    ai_m.ai_random_move()
                    self.turtle_update_check(g_class)
                    self.print_state()
            else:
                print("attempt failed")
                self.escape_try = False
        else:
            print("You have tried to escape and lost")


