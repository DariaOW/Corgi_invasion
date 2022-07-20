from world import Map, Field, Item, HealthPotion, BauleMask, KweleMask, TekeMask, KotaMask, Grootslang, Kongamato, \
                    Impundulu, NinkiNanka, Character, Jackrabbit, Snake, Turtle, Jackal, Hyena, Ferret
import random
import pickle
from pathlib import Path
import os
from kigegner import MapForAi


def forward(m, g_class, ai_m, i, enemies):
    m.forward(g_class, ai_m)


def right(m, g_class, ai_m, i, enemies):
    m.right(g_class, ai_m)


def left(m, g_class, ai_m, i, enemies):
    m.left(g_class, ai_m)


def backwards(m, g_class, ai_m, i, enemies):
    m.backwards(g_class, ai_m)


def items(m, g_class, ai_m, i, enemies):
    i.items(g_class)


def pickup(m, g_class, ai_m, i, enemies):
    loot = m.get_items()
    if len(loot) > 0:
        for x in loot:
            x.pickup(g_class, x, loot)


def save(m, g_class, ai_m, i, enemies):
    player_pickle, map_pickle, ai_map_pickle = open('saveplayerdata.pickle', 'wb'), open('savemapdata.pickle', 'wb'),\
                                              open('saveaimapdata.pickle', 'wb')
    pickle.dump(g_class, player_pickle)
    player_pickle.close()
    pickle.dump(m, map_pickle)
    map_pickle.close()
    pickle.dump(ai_m, ai_map_pickle)
    ai_map_pickle.close()
    print("You have successfully saved!")


def load(m, g_class, ai_m, i, enemies):
    if len(enemies) > 0:
        return "You can not load the game if there are enemies on your field"
    else:
        start_with_load_pickle_data()


def quit_game(m, g_class, ai_m, i, enemies):
    while True:
        end = input("Would you like to save your progress? yes/no").lower().strip()
        if end == "yes":
            save(m, g_class, ai_m, i, enemies)
            print("Thanks, Game saved!")
            exit()
        elif end == "no":
            print("Bye")
            exit()
        else:
            continue


def print_help(m, g_class, ai_m, i, enemies):
    return f'{" ".join(str(x) for x in Commands.keys())}'


def use_skills(g_class, enemies, m, step):
    if step == 1 and g_class.name in ["Turtle", "Jackal", "Hyena"]:
        if g_class.name == "Turtle" and g_class.skill(enemies):
            return
        elif enemies[0].hp <= enemies[0].max_hp / 4 and g_class.name == "Jackal" and g_class.enemies_teammate == 0:
            g_class.skill(enemies)
            if g_class.enemies_teammate:
                return
        elif g_class.name == "Hyena":
            g_class.skill(enemies)
    elif step == 2 and g_class.name in ["Jackal"] and g_class.enemies_teammate > 0:
        #nach dem fight back
        if g_class.shield < enemies[0].ad:
            g_class.teammate_dead()
        elif g_class.shield > enemies[0].ad:
            g_class.shield = g_class.shield - enemies[0].ad
            print("Your teammate is wounded and have " + str(g_class.shield) + " hp left")
            return
    elif step == 3 and g_class.name in ["Snake"] and len(enemies) > 0:
        # am ende nach dem schaden
        g_class.skill(enemies, g_class, m)


def enemies_die(enemies, m, g_class):
    enemies[0].die()
    m.get_loot_from_enemies(enemies, g_class)
    enemies.remove(enemies[0])
    print("You have " + str(g_class.hp) + " hp left")
    if g_class.name == "Turtle":
        g_class.update_skill()


def fight(m, g_class, ai_m, i, enemies):
    if len(enemies) > 0:
        enemies[0].hp = enemies[0].hp - g_class.ad
        if enemies[0].hp <= 0:
            enemies_die(enemies, m, g_class)
        else:
            print(f"{enemies[0].name} has {enemies[0].hp} hp left")
            use_skills(g_class, enemies, m, step=1)
            print(f"{enemies[0].name} fight back")
            use_skills(g_class, enemies, m, step=2)
            g_class.hp = g_class.hp - enemies[0].ad + g_class.protect
            if g_class.hp <= 0:
                g_class.die()
            print("You are wounded and have " + str(g_class.hp) + " hp left")
            use_skills(g_class, enemies, m, step=3)
    else:
        print("You should not fight")


def rest(m, g_class, ai_m, i, enemies):
    if len(enemies) > 0:
        print("You can not rest, the enemy is here ")
    else:
        g_class.hp = g_class.max_hp
        print(f"Your hp is {g_class.hp}")


def escape(m, g_class, ai_m, i, enemies):
    m.escape(g_class)


def stats(m, g_class, ai_m, i, enemies):
    print(f"Your hp - {g_class.hp},\n your damage - {g_class.ad},\n you shield - {g_class.protect},\n "
          f" your inventory has {g_class.max_inventory - g_class.inv} free locations.\n")
    i.items_in_inventory(g_class)
    if g_class.name == "Jackal" and g_class.enemies_teammate:
        print(f" You have {g_class.enemies_teammate} teammate/s")


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
    i = Item()
    enemies = m.get_enemies()
    stats(m, g_class, ai_m, i)
    m.print_state()
    print("(type help to list the commands available)\n")
    while True:
        command = input(">").lower().strip().split(" ")
        if command[0] in Commands:
            Commands[command[0]](m, g_class, ai_m, i, enemies)
        else:
            print("You run around in circles and don't know what to do.")


def start_with_load_pickle_data():
    player_pickle, map_pickle, ai_map_pickle = open('saveplayerdata.pickle', 'rb'), \
                                               open('savemapdata.pickle', 'rb'), \
                                               open('saveaimapdata.pickle', 'rb')
    g_class, m, ai_m = pickle.load(player_pickle), pickle.load(map_pickle), pickle.load(ai_map_pickle)
    player_pickle.close()
    map_pickle.close()
    ai_map_pickle.close()
    play_loop(m, g_class, ai_m)


def check_for_save():
    while True:
        check_load = input("Saved game found! Do you want to load the game? yes/no ").lower().strip()
        if check_load not in ["yes", "no"]:
            print("Invalid choice.")
            continue
        else:
            break
    if check_load == "yes":
        start_with_load_pickle_data()
    elif check_load == "no":
        Path("saveplayerdata.pickle").unlink()
        Path("savemapdata.pickle").unlink()
        Path("saveaimapdata.pickle").unlink()


if __name__ == '__main__':
    if Path("saveplayerdata.pickle").is_file() and Path("savemapdata.pickle").is_file() and \
            Path("saveaimapdata.pickle").is_file():
        check_for_save()
    choose_class()


