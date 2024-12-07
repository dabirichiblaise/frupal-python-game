import anokwuru


class Hero_Movement:

    def __init__(self, max_size = 25):
        self.max_size = max_size
        self.row = max_size // 2
        self.column = max_size // 2
        self.energy = 100


    def move_north(self, hero, map):
        if self.row < self.max_size - 1: #if the hero's position is less than max size - 1, they will move up a row by one
            self.row += 1

        else:
            self.row = 0
        self.energy = anokwuru.terrain_energy_depletion((hero, map))

    
    def move_east(self, hero, map):
        if self.column < self.max_size - 1:
            self.column += 1

        else:
            self.column = 0
        self.energy = anokwuru.terrain_energy_depletion((hero, map))



    def move_south(self, hero, map):
        if self.row > 0:
            self.row -= 1

        else:
            self.row = self.max_size - 1
        self.energy = anokwuru.terrain_energy_depletion((hero, map))



    def move_west(self, hero, map):
        if self.column > 0:
            self.column -= 1
        
        else:
            self.column = self.max_size - 1
        self.energy = anokwuru.terrain_energy_depletion((hero, map))


    
    #made a getter for position and energy so that my test file can use them properly

    def get_position(self):
        return self.row, self.column
    
    def get_energy(self):
        return self.energy
    





    