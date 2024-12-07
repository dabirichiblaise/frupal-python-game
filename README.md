# Frupal Game
A Python-based adventure game where players explore a terrain-based map searching for  royal diamonds while managing resources and overcoming obstacles.

## Features

- Interactive tile-based exploration
- Resource management:
  - Energy system for movement and actions
  - Whiffles (in-game currency)
- Terrain types affecting gameplay:
  - Meadow
  - Forest
  - Water
  - Wall
  - Bog
  - Swamp
- Items and Tools:
  - Various tools for obstacle removal
  - Power bars for energy restoration
  - Clues for finding diamonds
  - Treasure chests
  - Binoculars, boats, and more
- Obstacles requiring specific tools:
  - Trees (Hatchet, Axe, Chainsaw)
  - Boulders (Chisel, Sledge, Jackhammer)
  - Blackberry Bushes (Machete, Shears)


## Requirements

- Python 3
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dabirichiblaise/frupal-python-game.git
cd frupal-python-game
```
2. Run the game:
```bash
python src/chang.py
```

## Game Components
1. Map System
   - Modular cell-based map system
   - Different terrain types affecting movement energy cost
   - Hidden items and obstacle to discover

2. Player Mechanics
   - Energy management
   - Currency (Whiffles) system
   - Inventory management
   - Tool usage for obstacle removal

3. Items
   - Tools for removing obstacles
   - Power bars for energy restoration
   - Clues for finding the royal diamonds
   - Treasure chests with rewards or penalties
   - Special items like boats for water traversal

## Code Structure
- chang.py: Main game GUI and event handling
- dustin.py: Core game data structures and file operations
- anokwuru.py: Game logic and state management
- rayne_hero_movement.py: Player movement system
- rayne_encounter_obstacle.py: Obstacle interaction system
- rayne_power_bar_encounter.py: Power bar encounter system


## Development
The game is built with a modular architecture allowing for easy expansion of:
- New terrain types
- Additional items and tools
- New obstacle types
- Enhanced gameplay mechanics

## Authors
- Dabirichi Blaise Anokwuru
- Rayne Allen
- Brendan Chang
- Miles Dustin

## License
MIT License
