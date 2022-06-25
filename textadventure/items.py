import random


class Item:
    def use_one_item(self, g_class):
        if len(g_class.items) == 1:
            x = g_class.items[0]
        else:
            items = []
            for p in g_class.items:
                items.append(p.name)
            while True:
                choice = input("Which one?")
                if choice in items:
                    x = p
                    break
                else:
                    print("not found")
        if x.typ == "mask":
            self.put_on_mask(g_class, x)
        x.use_item(g_class)

    def check_inventory(self, x, g_class):
        inventory = True
        if x.weight + g_class.inv > g_class.max_inventory:
            inventory = False
            print("You have not place in the inventory")
        return inventory

    def pickup(self, g_class, x, loot):
        if self.check_inventory(x, g_class):
            g_class.items.append(x)
            g_class.inv = g_class.inv + x.weight
            loot.remove(x)
            print(f'You picked up {x.name}')
        else:
            self.put_away_or(g_class, x, loot)

    def put_away_or(self, g_class, x, loot):
        while True:
            put = input("Do you want to put away one item?").lower().strip()
            if put == "yes":
                self.put_away(g_class, x, loot)
                break
            elif put == "no":
                break
            else:
                print("hm?")

    def put_away(self, g_class, x, loot):
        self.items_in_inventory(g_class)
        while True:
            put = input("What do you want to put away?")
            for i, o in enumerate(g_class.items):
                if o.name == put:
                    g_class.inv = g_class.inv - o.weight
                    del g_class.items[i]
                    self.pickup(g_class, x, loot)
                    break
                else:
                    print("not found")

    def items_in_inventory(self, g_class):
        if len(g_class.items) == 0:
            print("You have not any items")
        else:
            if len(g_class.items) > 1:
                items = []
                for x in g_class.items:
                    items.append(x.name)
                    n = ','.join(items)
                print(f'You have {n}.')
                for x in g_class.items:
                    print(f"{x.name, x.des}")
            else:
                for x in g_class.items:
                    print(f'You have {x.name, x.des}')
        if len(g_class.mask) > 0:
            for x in g_class.mask:
                print(f"You take on {x.name} {x.des}")

    def items(self, g_class):
        self.items_in_inventory(g_class)
        print("The Poisons could be used only once, Masks you can use all time,you wear them, but only one ")
        while True:
            to_use = input("Do you want to use the item? yes/no").lower().strip()
            if to_use == "yes":
                self.use_one_item(g_class)
                break
            elif to_use == "no":
                break
            else:
                continue

    def put_on_mask(self, g_class, x):
        if self.change_mask(g_class, x):
            g_class.mask.append(x)
            g_class.inv = g_class.inv - x.weight
            for i, o in enumerate(g_class.items):
                if o.name == x.name:
                    del g_class.items[i]

    def change_mask(self, g_class, x):
        if g_class.mask:
            print(f"{g_class.mask[0].name} {g_class.mask[0].des} (old)\n{x.name} {x.des}(new)")
            new = input("Will you change? yes/no").lower().strip()
            while True:
                if new == "yes":
                    g_class.items.append(g_class.mask[0])
                    g_class.mask.clear()
                    g_class.ad = g_class.default_ad
                    g_class.protect = g_class.default_protect
                    return True
                elif new == "no":
                    return False
                else:
                    print("hmmm?")
        else:
            return True




class HealthPotion(Item):
    def __init__(self):
        Item.__init__(self)
        self.weight = 1
        self.name = "Health Potion"
        self.typ = "potion"
        self.des = "that gives you random hp"

    def use_item(self, g_class):
        r = random.random()
        if r < 0.50:
            g_class.hp = g_class.hp + 100
        elif r < 0.70:
            g_class.hp = g_class.hp + 200
        elif r < 0.90:
            g_class.hp = g_class.max_hp
        else:
            g_class.hp = g_class.hp + 10
        if g_class.hp > g_class.max_hp:
            g_class.hp = g_class.max_hp
        print("You have " + str(g_class.hp) + " hp")
        self.empty(g_class)

    def empty(self, g_class):
        for i, o in enumerate(g_class.items):
            if o.name == self.name:
                del g_class.items[i]
        g_class.inv = g_class.inv - self.weight

class BauleMask(Item):
    def __init__(self):
        Item.__init__(self)
        self.weight = 2
        self.name = "Baule Mask"
        self.typ = "mask"
        self.des = "that gives you 70 ad more"

    def use_item(self, g_class):
        g_class.ad = g_class.ad + 70
        print("You have " + str(g_class.ad) + " ad")


class KweleMask(Item):
    def __init__(self):
        Item.__init__(self)
        self.weight = 2
        self.name = "Kwele Mask"
        self.typ = "mask"
        self.des = "that gives you 30 shield"

    def use_item(self, g_class):
        g_class.protect = g_class.protect + 30
        print("You have " + str(g_class.protect) + " shield")


class TekeMask(Item):
    def __init__(self):
        Item.__init__(self)
        self.weight = 2
        self.name = "Teke Mask"
        self.typ = "mask"
        self.des = "that gives you an ability to escape when an Impundulu at the field"

    def use_item(self, g_class):
        pass


class KotaMask(Item):
    def __init__(self):
        Item.__init__(self)
        self.weight = 2
        self.name = "Kota Mask"
        self.typ = "mask"
        self.des = "that gives you 50 shield and 100 ad more"

    def use_item(self, g_class):
        g_class.protect = g_class.protect + 50
        g_class.ad = g_class.ad + 100
        print(f"You have {g_class.protect} shield and {g_class.ad} ad")
