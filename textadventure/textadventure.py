from world import Map, Field, Item, HealthPotion, BauleMask, KweleMask, TekeMask, KotaMask, Grootslang, Kongamato, \
                    Impundulu, NinkiNanka, Character, Jackrabbit, Snake, Turtle, Jackal, Hyena, Ferret
import random
import pickle
from pathlib import Path
import os
from kigegner import MapForAi


def forward(m, g_class, ai_m):
    m.forward(g_class, ai_m)


def right(m, g_class, ai_m):
    m.right(g_class, ai_m)


def left(m, g_class, ai_m):
    m.left(g_class, ai_m)


def backwards(m, g_class, ai_m):
    m.backwards(g_class, ai_m)


def items(m, g_class, ai_m):
    i = Item()
    i.items(g_class)


def pickup(m, g_class, ai_m):
    loot = m.get_items()
    if len(loot) > 0:
        for x in loot:
            x.pickup(g_class, x, loot)


def save(m, g_class, ai_m):
    with open('saveplayerdata.pickle', 'wb') as f:
        pickle.dump([g_class, g_class.name, g_class.hp], f, protocol=pickle.HIGHEST_PROTOCOL)
    with open('saveworlddata.pickle', 'wb') as f:
        pickle.dump(m.state, f, protocol=pickle.HIGHEST_PROTOCOL)


def load(m, g_class, ai_m):
    # ich weiß nicht, mal schauen später

    with open('saveplayerdata.pickle', 'rb') as f:
        g_class, g_class.hp, g_class.name = pickle.load(f)
    with open('saveplayerdata.pickle', 'rb') as f:
        m.state = pickle.load(f)


def quit_game(m, g_class, ai_m):
    while True:
        end = input("Would you like to save your progress? yes/no").lower().strip()
        if end == "yes":
            save(m, g_class)
            print("Thanks, Game saved!")
            exit()
        elif end == "no":
            print("Bye")
            exit()
        else:
            continue


def print_help(m, g_class, ai_m):
    print(f'{" ".join(str(x) for x in Commands.keys())}')


def fight(m, g_class, ai_m): #refactoring
    enemies = m.get_enemies()
    if len(enemies) > 0:
        enemies[0].hp = enemies[0].hp - g_class.ad
        if enemies[0].hp <= 0:
            enemies[0].die()
            m.get_loot_from_enemies(enemies, g_class)
            enemies.remove(enemies[0])
            print("You have " + str(g_class.hp) + " hp left")
            if g_class.name == "Turtle":
                g_class.update_skill()
        else:
            print(f"{enemies[0].name} has {enemies[0].hp} hp left")
            if g_class.name == "Turtle" and g_class.skill(enemies):
                return
            if enemies[0].hp <= enemies[0].max_hp / 4 and g_class.name == "Jackal" and g_class.enemies_teammate == 0:
                teammate = input(f"You can take {enemies[0].name} with you as a teammate. yes/no").lower().strip()
                if teammate == "yes":
                    g_class.skill(enemies)
                    return
                elif teammate == "no":
                    pass
                else:
                    print("Think faster")
            if g_class.name == "Hyena":
                g_class.skill(enemies)
            print(f"{enemies[0].name} fight back")
            if g_class.name == "Jackal" and g_class.enemies_teammate > 0 and g_class.shield < enemies[0].ad:
                g_class.shield = 0
                g_class.enemies_teammate -= 1
                g_class.ad = g_class.ad - g_class.teammate_ad
                g_class.teammate_ad = 0
                print("Your teammate is dead")
            elif g_class.name == "Jackal" and g_class.enemies_teammate > 0 and g_class.shield > enemies[0].ad:
                g_class.shield = g_class.shield - enemies[0].ad
                print("Your teammate is wounded and have " + str(g_class.shield) + " hp left")
                return
            g_class.hp = g_class.hp - enemies[0].ad + g_class.protect
            if g_class.hp <= 0:
                g_class.die()
            print("You are wounded and have " + str(g_class.hp) + " hp left")
            if g_class.name == "Snake" and len(enemies) > 0:
               g_class.skill(enemies, g_class, m)
    else:
        print("You should not fight")


def rest(m, g_class, ai_m):
    enemies = m.get_enemies()
    if len(enemies) > 0:
        print("You can not rest, the enemy is here ")
    else:
        g_class.hp = g_class.max_hp
        print(f"Your hp is {g_class.hp}")


def escape(m, g_class, ai_m):
    m.escape(g_class)


def stats(m, g_class, ai_m):
    print(f"Your hp - {g_class.hp},\n your damage - {g_class.ad},\n you shield - {g_class.protect},\n "
          f" your inventory has {g_class.max_inventory - g_class.inv} free locations.\n")
    i = Item()
    i.items_in_inventory(g_class)
    if len(g_class.mask) > 0:
        for x in g_class.mask:
            print(f"You take on {x.name} {x.des}")
    #was mit teammate


Commands = {
    'help': print_help,
    "status": stats,
    'up': forward,
    'right': right,
    'left': left,
    'down': backwards,
    'quit': quit_game,
    'pickup': pickup,
    'items': items,
    'fight': fight,
    'save': save,
    'load': load,
    'rest': rest,
    "escape": escape
}


def choose_class():
    print('God sent the chameleon to announce to men that they would never die. The chameleon went on his mission,\n' +
          "but he walked slowly and stopped along the way to eat. Some time after the chameleon had left, a lizard\n" +
          "went to announce to men that they would die. You are a small fable in the battle")
    while True:
        decision_l_o_ch = input("Are you at the side of the chameleon or the lizard?").lower().strip()
        if decision_l_o_ch == "chameleon":
            a = [Jackal(), Jackrabbit(), Turtle()]
            g_class = random.choice(a)
            break
        elif decision_l_o_ch == "lizard":
            a = [Snake(), Hyena(), Ferret()]
            g_class = random.choice(a)
            break
        else:
            print("not in play")
    m = Map(10, 10, g_class)
    ai_m = MapForAi(10, 10, m)
    play_loop(m, g_class, ai_m)


def play_loop(m, g_class, ai_m):
    print(f"You was born as {g_class.name} and you are {g_class.skills_description}")
    stats(m, g_class, ai_m)
    m.print_state()
    print("(type help to list the commands available)\n")
    while True:
        command = input(">").lower().strip().split(" ")
        if command[0] in Commands:
            Commands[command[0]](m, g_class, ai_m)
        else:
            print("You run around in circles and don't know what to do.")

def check_for_valid_save():
    try:
        saved_world = pickle.load(open("saved_world.p", "rb"))
        saved_player = pickle.load(open("saved_player.p", "rb"))
    except:
        Path("saveplayerdata.pickle").unlink()
        Path("saveworlddata.pickle").unlink()

def check_for_save():
    saved = False
    if Path("saveplayerdata.pickle").is_file() and Path("saveworlddata.pickle").is_file():
        while True:
            check_load = input("Saved game found! Do you want to load the game? yes/no ").lower().strip()
            if check_load == "yes":
                load(m, g_class)
                saved = True
                break
            elif check_load == "no":
                Path("saveplayerdata.pickle").unlink()
                Path("saveworlddata.pickle").unlink()
                break
            else:
                print("Invalid choice.")
        return saved


if __name__ == '__main__':
    #saved = check_for_save()
    #if saved:
        #play_loop()
    #else:
    choose_class()
