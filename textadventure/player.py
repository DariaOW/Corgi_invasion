import random


class Character:
    def __init__(self, hp, max_hp, ad, default_ad, protect, default_protect, name, items, mask, max_inventory, inv):
        self.hp = hp
        self.ad = ad
        self.default_ad = default_ad
        self.name = name
        self.max_hp = max_hp
        self.items = items
        self.mask = mask
        self.protect = protect
        self.default_protect = default_protect
        self.max_inventory = max_inventory
        self.inv = inv

    def is_dead(self):
        return self.hp <= 0

    def die(self):
        print(self.name + " died")
        exit()


class Jackrabbit(Character): #skills gemacht
    def __init__(self):
        Character.__init__(self, 500, 500, 50, 50, 0, 0,"Jackrabbit", list(), list(), 6, 0)
        self.skills_description = "so fast, that you can almost always left the battle field"

class Turtle(Character):
    def __init__(self):
        Character.__init__(self,900,900, 150,150, 0,0, "Turtle", list(), list(), 9, 0)
        self.skills_description = "so tough, that you can repel 2 attacks in the battle"
        self.repel_limit = 2

    def skill(self, enemies):
        self.repel_limit -= 1
        if self.repel_limit >= 0:
            print(f"{enemies[0].name} fight back, but you have repelled. You have {self.hp} hp")
            return True
        else:
            return False

    def update_skill(self):
        self.repel_limit = 2


class Jackal(Character):
    def __init__(self):
        Character.__init__(self,700,700, 200,200, 0,0,"Jackal", list(), list(), 6, 0)
        self.skills_description = "so tricky, that you can employ your enemies if they are almost dead (25% of hp) "
        self.enemies_teammate = 0
        self.shield = 0
        self.teammate_ad = 0

    def skill(self, enemies):
        while True:
            teammate = input(f"You can take {enemies[0].name} with you as a teammate. yes/no").lower().strip()
            if teammate == "yes":
                self.hp = self.hp + enemies[0].hp
                self.ad = self.ad + enemies[0].ad
                self.enemies_teammate += 1
                self.shield = self.shield + enemies[0].hp
                self.teammate_ad = enemies[0].ad
                enemies.remove(enemies[0])
                print(f"your teammate has {self.shield} hp, if hp is equal null he will die")
                break
            elif teammate == "no":
                pass
            else:
                print("Think faster")

    def teammate_dead(self):
        self.shield = 0
        self.enemies_teammate -= 1
        self.ad = self.ad - self.teammate_ad
        self.teammate_ad = 0
        print("Your teammate is dead")

class Snake(Character):
    def __init__(self):
        Character.__init__(self, 100, 100, 50,50,0,0, "Snake", list(), list(), 4, 0)
        self.skills_description = "capably to poison your enemies"
        self.poison_hp = 60
        self.poison_damage = 30

    def skill(self, enemies, g_class, m):
        enemies[0].hp = enemies[0].hp - self.poison_hp
        enemies[0].ad = enemies[0].ad - self.poison_damage
        if enemies[0].hp <= 0 or enemies[0].ad <= 0:
            enemies[0].die()
            m.get_loot_from_enemies(enemies, g_class)
            enemies.remove(enemies[0])
            print("You have " + str(g_class.hp) + " hp left")
        else:
            print(f"{enemies[0].name} is poisoned and have {enemies[0].hp} hp left. His damage is only {enemies[0].ad}")


class Hyena(Character):
    def __init__(self):
        Character.__init__(self, 700, 700, 150,150,0,0, "Hyena", list(), list(), 6, 0)
        self.skills_description = "so magic, that you can steal hp of your enemies"

    def skill(self, enemies):
        r = random.random()
        if r < 0.70:
            x = random.randint(10, enemies[0].hp)
            self.hp = self.hp + x
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"You have stolen {x} hp")


class Ferret(Character):
    def __init__(self):
        Character.__init__(self, 300, 300, 100,100, 0,0, "Ferret", list(), list(), 6, 0)
        self.skills_description = "so greedy, that you can find double items at the field"

