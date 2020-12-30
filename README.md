# Key-Cave-Adventure-Game
## Background
Key Cave Adventure Game is a single-player dungeon-crawler game where the player adventurously explores a dungeon. The objective is for the player to find the key and get out of the dungeon through the door. The game play utilises simple key commands. The positions of Entities are always represented as (row, col).  
## Class structure
The program follows the Apple model-view-controller (Apple MVC) structure.
![Class structure](class_structure(1).png)
## Usage
Run a2.py to start the game.  
a2_support.py,  gamen.txt (game1.txt, game2.txt, or game3.txt) are required for a2.py.  
gamen.txt is the n-th dungeon layout. There will be multiple provided. “game1.txt” is the simplest one to start from.  
## Test
This project comes from an assignment from CSSE1001.
Run test_a2.py for function testing.
## Appendix
### Printing Example
    #####
    # #K#
    #O  #
    # D #
    #####
    Moves left: 7

    Please input an action: H
    Here is a list of valid actions: ['I', 'Q', 'H', 'W', 'S', 'D', 'A']
    #####
    # #K#
    #O  #
    # D #
    #####
    Moves left: 7

    Please input an action: D
    #####
    # #K#
    # O #
    # D #
    #####
    Moves left: 6

    Please input an action: D
    #####
    # #K#
    #  O#
    # D #
    #####
    Moves left: 5

    Please input an action: I D
    Wall('#') is on the D side.
    #####
    # #K#
    #  O#
    # D #
    #####
    Moves left: 4

    Please input an action: W
    #####
    # #O#
    #   #
    # D #
    #####
    Moves left: 3

    Please input an action: S
    #####
    # # #
    #  O#
    # D #
    #####
    Moves left: 2

    Please input an action: S
    #####
    # # #
    #   #
    # DO#
    #####
    Moves left: 1

    Please input an action: A
    You have won the game with your strength and honour!
