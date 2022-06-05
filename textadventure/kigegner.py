import random


class MapForAi:
    def __init__(self, width, height, m):
        self.state = []
        self.coordinates = []
        self.x = 0
        self.y = 0
        for i in range(width):
            empty_fields = []
            for j in range(height):
                empty_fields.append([])
            empty_fields[m.men_field_to_aimap()] = ["Men"]
            self.state.append(empty_fields)


    def ai_random_move(self):
        r = random.random()
        if r < 0.2 and not self.x == len(self.state) - 1:
            self.x = self.x + 1
        elif r < 0.4 and not self.x == 0:
            self.x = self.x - 1
        elif r < 0.6 and not self.y == len(self.state[self.x]) - 1:
            self.y = self.y + 1
        elif r < 0.8 and not self.y == 0:
            self.y = self.y - 1
        else:
            pass
        print(f"ai s coordinates are {self.x, self.y}")
        self.men_found()


    def men_found(self):
        if self.state[self.x][self.y] == ["Men"]:
            print("ai won!")
            exit()





