from dustin import OBSTACLE_TOOL_REL
#from dustin import DEFAULT

def handle_obstacle_encounter(hero, game_map):

    """
    handles the encounter(s) with an obstacle:
    
    -deducts energy based on the obstacle and the tool the hero possesses
    -removes the obstacle if the hero has enough energy
    -ends the game if the hero doesnt have enough energy 
    -returns a tuple (bool, string) where bool indicates if the obstacle encounter has happened, and the string outputs a message to the user
    """

    current_cell = game_map.board[hero.hm.column][hero.hm.row]
    obstacle = current_cell.content #setting an obstacle variable to whatever a map cell contains


    #defining the default energy costs for obstacles without the right tools
    default_energy_costs = {
        "tree": 10,
        "boulder": 16,
        "blackberry_bushes": 4
    }

    #checking if the content of the map cell is an obstacle
    if obstacle not in OBSTACLE_TOOL_REL and obstacle not in default_energy_costs: 
        return "" # False, "No obstacle at this location." #i know this output message isn't necessary in the game itself, but I have it there for testing purposes
        # Brendan changed this

    #setting a variable for energy deduction w/o the right tool
    energy_removal = default_energy_costs[obstacle]


    #check if the hero has the appropriate tool to reduce the energy cost
    if obstacle in OBSTACLE_TOOL_REL:
        for tool, energy_cost in OBSTACLE_TOOL_REL[obstacle].items():
            if tool in hero.inventory:
                #if the hero has the tool, set the default energy cost to thee tool's energy cost instead
                energy_removal = energy_cost
                break


    #here, I add the movement cost to the total energy cost. I may be misunderstanding what the user story is asking for though
    total_energy_cost = energy_removal + 1 #the 1 is for the additional movement


    #check if the hero has enough energy to remove the obstacle
    if hero.hm.energy <= total_energy_cost:
        return "You do not have enough energy to remove the obstacle. Game over." # True, "You do not have enough energy to remove the obstacle. Game over."
        # Brendan changed this
    #deduct the total energy cost from the hero's energy
    hero.hm.energy -= total_energy_cost


    #remove the obstacle from the current cell if it has been overcome
    current_cell.content = "none"

    #return message showing that the obstacle has been removed
    return "You removed the {0} and lost {1} energy points." .format(obstacle, total_energy_cost) # True, "You removed the {obstacle} and lost {total_energy_cost} energy points."
    # Brendan changed this
