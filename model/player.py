class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def move(self, direction):
        print(f"{self.name} se déplace {direction}.")