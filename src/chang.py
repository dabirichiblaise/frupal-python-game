import tkinter
import dustin
import anokwuru
import rayne_encounter_obstacle


# Global game_over is set by the game window before it destroys itself so that the main program
# can present the user with the correct message.  
# Win = 1, Die = 0.
global game_over
game_over = -1


# FUNCTION: game_window()
# Manages the user interface/current game
def game_window():


    ############################################################
    #  Initialization                                          #
    ############################################################  


    # Window creation
    my_window = tkinter.Tk()
    my_window.title("THE KINGDOM OF FRUPAL")
    my_window.geometry("500x700")
    lbl_header = tkinter.Label(my_window, text="\n*********THE KINGDOM OF FRUPAL*********\n")
    lbl_header.pack()

    # Stores the frame for the encounter section
    global current_encounter_frame
    current_encounter_frame = None

    # Stores the currently displayed message
    global message 
    message = ""


    ############################################################
    #  Encounters (Obstacles, Items/Powerbars/Treasure/Clues)  #
    ############################################################


    # FUNCTION: obstacle_encounter() 
    # Calls rayne obstacle function and sets message to the return value if it is a non-empty string
    # There is no yes/no needed for obstacles, so the obstacle is not loaded as a "current encounter",
    # only set as a message
    def obstacle_encounter():
        global message

        obstacle_prompt = rayne_encounter_obstacle.handle_obstacle_encounter(load_data[0], load_data[1])

        if (obstacle_prompt != ""):
            message = obstacle_prompt


    # FUNCTION: item_encounters()
    # If the current cell has item content, the corresponding message is set and a frame is created
    # containing the yes/no buttons.
    # Returns: (1, frame) if there was an encounter, (0, frame) if there was no encounter
    def item_encounters():
        frame = tkinter.Frame(my_window)

        item_prompt = load_data[1].item_purchase_prompt(load_data[0])

        if (item_prompt != ""):
            global message
            message = item_prompt
            btn_yes = tkinter.Button(frame, text="yes", command=get_item)
            btn_no = tkinter.Button(frame, text="no")

            btn_yes.pack()
            btn_no.pack()
            return 1, frame            
        else:
            return 0, frame


    # FUNCTION: encounter_frame_help()
    # This function clears the current encounter frame and replaces it if there is a new one.
    # Without this function the yes/no buttons don't disappear and just keep stacking up lol.
    def encounter_frame_help():
        global current_encounter_frame

        if current_encounter_frame:
            current_encounter_frame.destroy()

        encounter_check = item_encounters()
        current_encounter_frame = encounter_check[1]

        if encounter_check[0] == 0:
            current_encounter_frame.destroy()
            current_encounter_frame = None
        else:
            current_encounter_frame.pack()


    # FUNCTION: get_item() 
    # A wrapper to call the purchase function.  
    # Called by the yes button in the encounter frame.
    def get_item():
        global message
        response = load_data[1].item_purchase(load_data[0])
        message = response

        update_display()
        update_inventory()


    # FUNCTION: update_inventory()
    # Updates the inventory, idk how it works dustin wrote this lol
    def update_inventory():
        drop_con.set('')
        drop['menu'].delete(0, 'end')

        for c in load_data[0].inventory:
            drop['menu'].add_command(label = c, command = tkinter._setit(drop_con, c))


    ############################################################
    #  End Game Conditions                                     #
    ############################################################


    # FUNCTION: check_endgame()
    # If the diamonds are found, game over is set to 1 so that the main function can see that
    # the player won and the window is destroyed.  If the player dies, game over is set to 0
    # and the window is destroyed.
    def check_endgame():
        global game_over

        if (anokwuru.royal_diamonds(load_data) is True):
            game_over = 1
            my_window.destroy()
        elif (anokwuru.out_of_energy(load_data[0].hm.energy) is True):
            game_over = 0
            my_window.destroy()
            

    ############################################################
    #  Primary Interface Utilities                             #
    ############################################################


    # FUNCTION: update_display()
    # Manually updates all the game data to the most recent values
    def update_display():
        hero_x = load_data[0].hm.column
        hero_y = load_data[0].hm.row
        biome = load_data[1].board[hero_x][hero_y].terrain
        tk_biome.set(biome)
        energy = load_data[0].hm.energy
        tk_energy.set(energy)
        wallet = load_data[0].money
        tk_wallet.set(wallet)
        coords = [hero_x, hero_y]
        tk_coords.set("(" + str(coords[0]) + "," + str(coords[1]) + ")")
        tk_biome.set(dustin.TERRAIN_REL[biome])
        check_endgame()
        tk_message.set(message)


    # FUNCTION: move_north()
    # Wrapper function called by the movement buttons.
    # Calls the hero movement functions and checks for encounters, then updates the display.
    def move_north():
        load_data[0].move_north(load_data[1])
        encounter_frame_help()
        obstacle_encounter()
        update_display()


    # FUNCTION: move_north()
    # Wrapper function called by the movement buttons.
    # Calls the hero movement functions and checks for encounters, then updates the display.
    def move_south():
        load_data[0].move_south(load_data[1])
        encounter_frame_help()
        obstacle_encounter()
        update_display()


    # FUNCTION: move_north()
    # Wrapper function called by the movement buttons.
    # Calls the hero movement functions and checks for encounters, then updates the display.
    def move_east():
        load_data[0].move_east(load_data[1])
        encounter_frame_help()
        obstacle_encounter()
        update_display()


    # FUNCTION: move_north()
    # Wrapper function called by the movement buttons.
    # Calls the hero movement functions and checks for encounters, then updates the display.
    def move_west():
        load_data[0].move_west(load_data[1])
        encounter_frame_help()
        obstacle_encounter()
        update_display()


    ############################################################
    #  Primary HUD and Buttons                                 #
    ############################################################


    #***********************************************************
    # Coordinate Update b/c otherwise it's really long to type

    hero_x = load_data[0].hm.column
    hero_y = load_data[0].hm.row


    #***********************************************************
    # Biome Display (Terrain)

    biome = load_data[1].board[hero_x][hero_y].terrain
    tk_biome = tkinter.StringVar()
    tk_biome.set(dustin.TERRAIN_REL[biome])

    lbl_biome_header = tkinter.Label(my_window, text="CURRENT TERRAIN:")
    lbl_biome = tkinter.Label(my_window, textvariable=tk_biome)

    lbl_biome_header.pack()
    lbl_biome.pack()


    #***********************************************************
    # Energy Display

    energy = load_data[0].hm.energy
    tk_energy = tkinter.IntVar()
    tk_energy.set(energy)
    lbl_energy_header = tkinter.Label(my_window, text="CURRENT ENERGY:")
    lbl_energy = tkinter.Label(my_window, textvariable=tk_energy)

    lbl_energy_header.pack()
    lbl_energy.pack()


    #***********************************************************
    # Wallet Display

    wallet = load_data[0].money
    tk_wallet = tkinter.IntVar()
    tk_wallet.set(wallet)
    lbl_wallet_header = tkinter.Label(my_window, text="WHIFFLES:")
    lbl_wallet = tkinter.Label(my_window, textvariable=tk_wallet)

    lbl_wallet_header.pack()
    lbl_wallet.pack()


    #***********************************************************
    # Current coordinate display

    coords = [hero_x, hero_y]
    tk_coords = tkinter.StringVar()
    tk_coords.set("(" + str(coords[0]) + "," + str(coords[1]) + ")")
    lbl_coords_header = tkinter.Label(my_window, text="CURRENT COORDINATES:")
    lbl_coords = tkinter.Label(my_window, textvariable=tk_coords)

    lbl_coords_header.pack()
    lbl_coords.pack()


    #***********************************************************
    # Movement controls

    lbl_move = tkinter.Label(my_window, text="\nMOVEMENT:")
    btn_up = tkinter.Button(my_window, text="NORTH", command=move_north)
    btn_down = tkinter.Button(my_window, text="SOUTH", command=move_south)
    btn_right = tkinter.Button(my_window, text="EAST", command=move_east)
    btn_left = tkinter.Button(my_window, text="WEST", command=move_west)

    lbl_move.pack()
    btn_up.pack()
    btn_down.pack()
    btn_right.pack()
    btn_left.pack()


    #***********************************************************
    # Inventory Display

    drop_con = tkinter.StringVar(my_window)
    lbl_inventory = tkinter.Label(my_window, text="OPEN INVENTORY")
    drop = tkinter.OptionMenu(my_window, drop_con, *load_data[0].inventory)

    lbl_inventory.pack()
    drop.pack()


    #***********************************************************
    # Message display

    tk_message = tkinter.StringVar()
    check_endgame()
    tk_message.set(message)
    lbl_message = tkinter.Label(my_window, textvariable=tk_message)
    
    lbl_message.pack()


    #***********************************************************
    # Main loop

    my_window.mainloop()
    


############################################################
#  GAME OVERRRR                                            #
############################################################


# FUNCTION: game_over_display()
# Displays a small window either congratulating the user for winning or informing them of their death.
def game_over_display():
    global game_over

    game_over_window = tkinter.Tk()
    game_over_window.title("THE KINGDOM OF FRUPAL")
    game_over_window.geometry("300x100")

    lbl_header = tkinter.Label(game_over_window, text="\n*********THE KINGDOM OF FRUPAL*********\n")

    if (game_over == 1):
        lbl_game_over_message = tkinter.Label(game_over_window, text="Found Diamonds, you won the game!")
    elif (game_over == 0):
        lbl_game_over_message = tkinter.Label(game_over_window, text="You ran out of energy and died")

    lbl_header.pack()
    lbl_game_over_message.pack()

    game_over_window.mainloop()


############################################################
#  Python Main Function                                    #
############################################################


if __name__ == "__main__":
    testfile = "./#map.txt"
    load_data = dustin.load_file(testfile)
    game_window()
    game_over_display()
