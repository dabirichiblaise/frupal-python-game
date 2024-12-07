def handle_power_bar_encounter(hero, game_map):
        """
        function to handle an encounter with a power bar.
        functionalities:
            -takes hero and map objects as arguments
            -checks if the player's current position has a power bar
            -prompts the player to purchase it
            -updates energy and bank balance
            -removes power bar from the map if purchased
        """

        current_location = game_map.board[hero.hm.column][hero.hm.row]

        #no power bar found found
        if current_location.content != 'power_bar':
                return False, "No power bar at this location."
        
        #power bar found, but not enough money for it
        if hero.money <= 0:
                return True, "You do not have enough whiffles to purchase the power bar."
        
        #if power bar is found and the hero has 1 or more  whiffles
        print("You have encountered a Power Bar! It costs 1 whiffle and provides 20 energy points.")



def handle_purchase(hero, game_map):

        current_location = game_map.board[hero.hm.column][hero.hm.row]
        purchase = input("Do you want to purchase the Power Bar? (yes/no): ").strip().lower()


        if purchase == 'yes':
                if hero.money >= 1:
                        hero.money -= 1
                        hero.hm.energy += 20
                        current_location.content = "none" #this should remove the power bar from the cell, in theory
                        return True
                
                else:
                        return True, "You do not have enough whiffles to purchase the Power Bar."  #this is already done above, but I figured I'd add it just to ensure that the hero can't purchase if they dont have enough money

        else:
                return True, "You chose not to purchase the Power Bar."