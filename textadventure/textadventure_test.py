import unittest
from textadventure import Commands
from world import Map, Turtle, Item, NinkiNanka
from kigegner import MapForAi
from textadventure import print_help, save, load, enemies_die
from unittest.mock import Mock
from unittest.mock import patch
import builtins
import pickle


class MyTestCase(unittest.TestCase):
    def test_forward(self):
        g_class = Turtle()
        m = Map(10, 10, g_class)
        ai_m = MapForAi(10, 10, m)
        m.get_enemies = []
        m.x, m.y = 5, 5
        m.forward(m, g_class)
        self.assertEqual(m.x,
                         6)
    def test_save(self):
        g_class = Turtle()
        m = Map(10, 10, g_class)
        ai_m = MapForAi(10, 10, m)
        i = Item()
        enemies = m.get_enemies()
        save(m, g_class, ai_m, i, enemies)
        save_g_class = open('saveplayerdata.pickle', 'rb')
        save_m = open('savemapdata.pickle', 'rb')
        save_ai_m = open('saveaimapdata.pickle', 'rb')
        self.assertEqual("Turtle",
                         pickle.load(save_g_class).name)
        self.assertEqual(m.x,
                         pickle.load(save_m).x)
        self.assertEqual(ai_m.x,
                         pickle.load(save_ai_m).x)

    def test_load(self):
        g_class = Turtle()
        m = Map(10, 10, g_class)
        ai_m = MapForAi(10, 10, m)
        i = Item()
        self.assertEqual(load(m, g_class, ai_m, i, enemies=["enemies"]),
                         "You can not load the game if there are enemies on your field")

    def test_enemies_die(self):
        g_class = Turtle()
        g_class.hp = 10
        self.assertEqual(enemies_die(g_class, enemies=[NinkiNanka()], m=Map(10, 10, g_class)),
                          "You have 10  hp left")







if __name__ == '__main__':
    unittest.main()


def test_print_help() -> None:
    g_class = Turtle()
    m = Map(10, 10, g_class)
    ai_m = MapForAi(10, 10, m)
    assert print_help(m, g_class, ai_m) == 'help status up right left down quit pickup items fight save load rest escape'







