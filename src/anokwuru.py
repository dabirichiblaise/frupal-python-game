# import dustin
import random

##################################################
# FUNCTION IMPLEMENTATIONS                       #
##################################################

#testfile = "./larger_test_data.txt" 
#load_data = dustin.load_file(testfile)

#Pass in the coordinates as x and y and the function checks to see if the player is at the locations of the jewels.
#Named the coordinates this way so that they match with what Dustin has in his file. The names can be changed
#Depending on what we agree.

def royal_diamonds(load_data):
    startx = load_data[0].hm.column
    starty = load_data[0].hm.row
    jewelsx = load_data[1].jewels_location[0]
    jewelsy = load_data[1].jewels_location[1]
    if startx == jewelsx and starty == jewelsy: #changed the coordinates to the one's loaded from the file
        return True

#Same logic with this, pass in the integer value of energy and it checks if it's gone below one. Prints message and returns.
def out_of_energy(energy):
    if energy < 1:
        return True


#What this function does is that it takes in the hero's current coordinates and energy level, and
#checks it with what is on the loaded file. If they match, some additional checks are done to determine the terrain
#Once the terrain is determined, it removes the appropriate amount of energy for that terrain. 
#Pass a map object

def terrain_energy_depletion(load_data):
    hero_x = load_data[0].hm.column
    hero_y = load_data[0].hm.row
    cell = load_data[1].board[hero_x][hero_y]
    energy = load_data[0].hm.energy

    if cell.terrain == 0 or cell.terrain == 1:
            energy -= 1
    elif cell.terrain == 2 or cell.terrain == 3:
            energy -= 1
    elif cell.terrain == 4 or cell.terrain == 5:
            energy -= 2
    return energy


#Encounter a Clue Prompt
#Returns a prompt to display to the user prompting to purchase a clue
def encounter_clue_prompt(load_data):
    hero_x = load_data[0].hm.column
    hero_y = load_data[0].hm.row
    cell = load_data[1].board[hero_x][hero_y]

    if cell.content == "Clue".lower():
        return "You have encountered a Clue! It costs 40 Whiffles to purchase. Do you want to purchase the Clue? (yes/no)."
    return ""

     
#Encounter a Clue
#Checks if the player has encountered a clue and informs them. Also prompte them to buy or not
#Outputs the clue information True or False which is randomized if the clue is purchased.
def encounter_clue(load_data):
    #Check if the player is at the clue's location
    hero_x = load_data[0].hm.column
    hero_y = load_data[0].hm.row
    cell = load_data[1].board[hero_x][hero_y].content

    jewelsx = load_data[1].jewels_location[0]
    jewelsy = load_data[1].jewels_location[1]
    money =  load_data[0].money
    
    if cell == "Clue".lower():
            #Check if the player has enough whiffles
            if money >= 40:
                load_data[0].money -= 40
                if random.choice([True, False]): #Determine if the clue is true or false
                    #True Clue
                    #Generate clue information
                    i = hero_x # i cells from the western border (X coordinate)
                    j = 40 - 1 #j is a number less than the hero's current whiffles
                    clue = (f"You are {i} cells from the western border, "
                            f"you possess more than {j} Whiffles, and the Royal Diamonds "
                            f"are located at coordinate {jewelsx, jewelsy}") #changed to royal diamonds loaded from the file
                else:
                    #False Clue
                    false_i = hero_x + random.randint(1, 3)
                    false_j = money + random.randint(10, 20) #j greater than bank account
                    clue = (f"You are {false_i} cells from the western border, "
                            f"you possess more than {false_j} Whiffles, and the Royal Diamonds "
                            f"are located at coordinate (30,30)")
                return clue
            elif money < 40:
                return "You do not have enough whiffles to purchase this Clue"
    elif cell != "Clue":
        return "There is no Clue at your current location"
    
    #Remove clue from the board
    cell = "None"
    return "Clue Purchased!"

            
##################################################
# Main to test the functions                      #
##################################################
if __name__ == "__main__":
    """
    testfile = "./larger_test_data.txt" 
    load_data = dustin.load_file(testfile) #tuple, 0 is a hero object and 1 is a map object.
    test_terrain_depletion = terrain_energy_depletion(load_data)
    print(test_terrain_depletion)

#Test for encounter a clue
    test_encounter_clue = encounter_clue(load_data)
    print(test_encounter_clue)
    """
