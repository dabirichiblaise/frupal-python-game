import os
import rayne_hero_movement as heromove
from rayne_power_bar_encounter import handle_power_bar_encounter, handle_purchase
from anokwuru import encounter_clue_prompt, encounter_clue



##################################################
# Globals                                        #
##################################################

# Valid content for inventory / gameboard objects
VALID_CONTENT = [
    "tree", "boulder", "blackberry_bushes", "power_bar", 
    "type_1_treasure_chest", "type_2_treasure_chest", 
    "clue", "hatchet", "axe", "chainsaw", 
    "chisel", "sledge", "jackhammer", "machete", 
    "shears", "binoculars", "none", "pretty_rock",
    "boat", "rock", "diamonds"
]


# Item prices dictionary (item as key, price as value)
ITEM_PRICES = {
    "binoculars" : 50,
    "boat" : 250,
    "clue" : 25,
    "pretty_rock" : 1,
    "power_bar" : 1,
    "hatchet" : 15,
    "axe" : 30,
    "chainsaw" : 60,
    "chisel" : 5,
    "sledge" : 25,
    "jackhammer" : 100,
    "machete" : 25,
    "shears" : 35
}


OBSTACLE_TOOL_REL = {
    "tree" : {
        "hatchet" : 8,
        "axe" : 6,
        "chainsaw" : 2
    },
    "boulder" : {
        "chisel" : 15,
        "sledge" : 12,
        "jackhammer" : 4
    },
    "blackberry_bushes" : {
        "machete" : 2,
        "shears" : 2
    }
}


# Terrain Relation (numeric value as key, string representation as value)
TERRAIN_REL = {
    0:"meadow",
    1:"forest", 
    2:"water",
    3:"wall", 
    4:"bog",
    5:"swamp"
}



##############################################################################
# Class Implementations                          
##############################################################################

# Cell Object: Holds individual cell data on map
#   visibility ->  0 = not visible, 1 = visible
#   terrain -> number identification for terrain type
#   content -> item / thing present in cell
class Cell:
    def __init__(self, v=0, t=0, c="None"):
        self.visibility = v
        self.terrain = t
        self.content = c


    # String operator for easily displaying cell content
    def __str__(self):
        return (
            "VISIBLE:"+str(self.visibility)+" TERRAIN_NUM:"+str(self.terrain)+
            " CONTENT:"+self.content
        )



##############################################################################
# Map Object: Holds the data for the map
#   jewels_location -> tuple holding the coordinates of the jewels
#   board -> matrix of cells holding the map data
#   max -> maximum width and height available on the map
class Map:
    def __init__(self, jx : int, jy : int, dims : int):
        self.jewels_location = (jx, jy)
        self.board = []
        self.max = dims

        # Initialize map to default cells
        for i in range(0,dims+1):
            self.board.append([])
            for j in range(0, dims+1):
                self.board[i].append(Cell())


    # Add cell content at coordinate specified by x and y
    # Returns: true - success, false - failure (invalid content given)
    def add_cell(self, toadd : Cell, x : int, y : int):
        if x >= self.max or y >= self.max:
            return False
        self.board[x][y] = toadd
        return True


    # Item Purchase Prompt
    # Returns either a prompt to display to the user prompting to purchase an item
    # for whatever that item price may be, or returns an empty string, signifying that
    # there is no item in the row X column cell specified in the argument.
    def item_purchase_prompt(self, hero):

        #call the handle_power_bar_encounter function here
        power_bar_encountered, power_bar_message = handle_power_bar_encounter(hero, self)
        if power_bar_encountered:
            return power_bar_message
 
        item = self.board[hero.hm.column][hero.hm.row].content 

        # if content is clue
        if item == "clue":
            return encounter_clue_prompt((hero, self))

        # if the user encountered a treasure chest
        if item in ["type_1_treasure_chest", "type_2_treasure_chest"]:
            return "You've encountered a treasure chest. Would you like to open it?"

        if item in ITEM_PRICES.keys():
            return "Would you like to purchase the {0} at your location for {1} whiffles?".format(item, ITEM_PRICES[item])
        return ""
        
    
    # Item Purchase
    # Purchase the item in the cell where the hero is if hero has enough money
    def item_purchase(self, hero):
        item = self.board[hero.hm.column][hero.hm.row].content

        if item == "power_bar":
            return handle_purchase(hero, self)
        elif item == "clue":
            return encounter_clue((hero, self))

        # If the user is opening a treasure chest
        if item == "type_1_treasure_chest":
            hero.money += 100
            self.board[hero.hm.column][hero.hm.row].content = "none"
            return "You got 100 more whiffles from the treasure chest."
        elif item == "type_2_treasure_chest":
            hero.money = 0
            self.board[hero.hm.column][hero.hm.row].content = "none"
            return "The treasure chest took all of your money."

        # Check for failure cases (no item or not enough whiffles)
        if item not in ITEM_PRICES.keys():
            return "There is no item to purchase at your location"
        elif hero.money < ITEM_PRICES[item]:
            return "You do not have enough whiffles to purchase this item"

        # Purchase the item and remove it from the board
        hero.money -= ITEM_PRICES[item]

        # account for if power bar is at location
        if item not in ["power_bar"]:
            hero.inventory.append(item)

        # Remove item from board
        self.board[hero.hm.column][hero.hm.row].content = "none" 
        return "Successfuly purchased: {}".format(item)




##############################################################################
# Hero object: holds hero data and functions
#   hm -> Hero_Movement object
#   money -> money amount [int]
#   energy -> heros energy level [int]
#   inventory -> heros inventory as a [list(str)]
class Hero:
    def __init__(self, dims : int, x : int, y : int, energy : int, money : int, inventory : list):
        # Hero movement stuff
        self.hm = heromove.Hero_Movement(dims) # fixed dimension value by passing it into contructor here
        self.hm.column = x
        self.hm.row = y
        self.hm.energy = energy

        # Hero money
        self.money = money

        # Hero inventory
        self.inventory = inventory
        if len(self.inventory) == 0:
            self.inventory += [""]


    ######################################################################
    # HERO MOVEMENT FUNCTION
    # wrapper functions for Rayne's movement functions
    # to account for water with and without a boat
    # treasure chests
    ######################################################################

    # MOVE NORTH
    # Arguments: map -> Game map
    def move_north(self, map : Map):

        t = map.board[self.hm.column][(self.hm.row+1) % map.max].terrain

        if TERRAIN_REL[t] == "water":
            if "boat" in self.inventory:
                self.hm.row = (self.hm.row+1) % map.max
            else:
                self.hm.energy -= 1
        else:
            self.hm.move_north(self, map)


    # MOVE EAST
    # Arguments: map -> Game map
    def move_east(self, map : Map):

        t = map.board[(self.hm.column+1) % map.max][self.hm.row].terrain

        if TERRAIN_REL[t] == "water":
            if "boat" in self.inventory:
                self.hm.column = (self.hm.column + 1) % map.max
            else:
                self.hm.energy -= 1
        else:
            self.hm.move_east(self, map)


    # MOVE SOUTH
    # Arguments: map -> Game map
    def move_south(self, map : Map):
        if self.hm.row - 1 < 0:
            self.hm.energy -= 1
            return

        t = map.board[self.hm.column][self.hm.row-1].terrain

        if TERRAIN_REL[t] == "water":
            if "boat" in self.inventory:
                self.hm.column -= 1
            else:
                self.hm.energy -= 1
        else:
            self.hm.move_south(self, map)


    # MOVE WEST
    # Arguments: map -> Game map
    def move_west(self, map : Map):
        if self.hm.column - 1 < 0:
            self.hm.energy -= 1
            return

        t = map.board[self.hm.column-1][self.hm.row].terrain

        if TERRAIN_REL[t] == "water":
            if "boat" in self.inventory:
                self.hm.row -= 1
            else:
                self.hm.energy -= 1
        else:
            self.hm.move_west(self, map)





##################################################
# Load File Function Implementation              #
##################################################

# Load File Data
# Args: filename (str) : name of file
# Throws:
#       FileError : error reading file
#       FileOpenError : inaccessible file 
# Returns: Hero object, Map object
def load_file(filename: str):
    line = "" # hold readline data
    listed = [] # hold split line data
    ret_map = None # Returning map object


    if not os.path.exists(filename):
        raise FileOpenError()  # File is not accessible

    f = open(filename, "r")


    # Load board size
    board_size = _check_int(filename, f.readline().strip())
    _check_buff(filename, f.readline().strip())

    # Load starting coordinates
    line = f.readline().strip()
    listed = line.split(",")
    startx = _check_int(filename, listed[0], line)
    starty = _check_int(filename, listed[1], line)

    # Load starting energy, money
    energy = _check_int(filename, f.readline().strip())
    money = _check_int(filename, f.readline().strip())

    # Load jewels coordinates
    line = f.readline().strip()
    listed = line.split(",")
    jewelsx = _check_int(filename, listed[0], line)
    jewelsy = _check_int(filename, listed[1], line)

    # Load Inventory
    inventory = []
    line = f.readline().strip()
    while line != "###":
        inventory.append(_check_content(filename, line))
        line = f.readline().strip()
        if not line:
            raise FileError(filename, "EOF")

    # Load Map Data
    ret_map = Map(jewelsx, jewelsy, board_size)

    line = f.readline().strip()
    while line:
        listed = line.split(",")
        if len(listed) != 3:
            raise FileError(filename, line)

        ret_map.add_cell(
            Cell(
                _check_int(filename, listed[2][0], line),
                _check_int(filename, listed[2][1], line),
                _check_content(filename, listed[2][2:], line)
            ),
            _check_int(filename, listed[0], line),
            _check_int(filename, listed[1], line)
        )
        line = f.readline().strip()

    return Hero(board_size, startx, starty, energy, money, inventory), ret_map 




# Private Functions: don't use outside of module please

# Used for checking file is formatted correctly
def _check_buff(filename, line):
    if line != "###":
        raise FileError(filename, line)

def _check_int(filename, num_str, full_line = ""):
    num = 0
    try:
        num = int(num_str)
    except ValueError as e:
        if full_line != "":
            raise FileError(filename, full_line)
        raise FileError(filename, num_str)
    return num

def _check_content(filename, content, full_line = ""):
    if content.lower() not in VALID_CONTENT:
        if content.lower() == "powerbar":
            return "power_bar"
        if full_line == "":
            raise FileError(filename, content)
        raise FileError(filename, full_line)
    return content.lower()



##################################################
# File exception objects for raising file errors #
# Note: all of these have string operators impl. #
##################################################

# File Open Error: Inaccessible file error
class FileOpenError(BaseException):
    def __init__(self, filename: str):
        self.filename = filename
    def __str__(self):
        return "inaccessible file: "+self.filename

# File Error: Incorrect formatting in file
class FileError(BaseException):
    def __init__(self, filename: str, line: str):
        self.filename = filename
        self.line = line
    def __str__(self):
        return "bad formatting in file: "+self.filename+":"+self.line





###############################################################################
# Module testing stuff, including module main call and temporary data objects
###############################################################################

# Function for printing loaded data
def test_print(board_size, startx, starty, energy, money, jewelsx, jewelsy, inventory, ret_map):
    print("board size: "+str(board_size)+"X"+str(board_size))
    print("start coordinates: "+str(startx)+"X"+str(starty))
    print("energy: "+str(energy))
    print("money: "+str(money))
    print("jewels coordinates: "+str(jewelsx)+"X"+str(jewelsy))
    print("Inventory:",inventory)
    print("map data:")
    for i in range(0,ret_map.max):
        for j in range(0,ret_map.max):
            print("X:",i,"Y:",j,ret_map.board[i][j])
    return


# Module Main
if __name__ == "__main__":

    # Load file function test
    testfile = "./larger_test_data.txt"
    try:
        hero, map = load_file(testfile)
    except FileOpenError as badfile:
        print(badfile)
    except FileError as badline:
        print(badline)
    
    """
    test_print(
        hero.hm.max_size, 
        hero.hm.column, 
        hero.hm.row,
        hero.hm.energy,
        hero.money,
        map.jewels_location[0],
        map.jewels_location[1],
        hero.inventory,
        map
    )
    """

    # Purchase useful item test
    print("\nHero whiffles:", hero.money)
    print("Hero inventory:", end = " ")
    for item in hero.inventory:
        print("-> "+item+" ", end = "")
    print("\nChanging hero location to (15,15)...")
    hero.hm.column = 15
    hero.hm.row = 15

    print("Current map cell item: ", map.board[hero.hm.column][hero.hm.row].content, end = "\n\n")
    print("Purchase and purchasing prompts:")
    print(map.item_purchase_prompt(hero))
    print(map.item_purchase(hero))

    print("\nHero whiffles:", hero.money)
    print("Hero inventory:", end = " ")
    for item in hero.inventory:
        print("-> "+item+" ", end = "")
    print("\nCurrent map cell item: ", map.board[hero.hm.column][hero.hm.row].content, end = "\n\n")