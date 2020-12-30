from a2_support import *

class GameLogic:
    """
    GameLogic contains all the game information and how the game should play out. By default,
    GameLogic should be constructed with ​GameLogic(dungeon_name=”game1.txt”)​.
    """

    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """

        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        # you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])

        # you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()

        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """

        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def get_dungeon_size(self) -> int:
        '''
        Returns:
            int: Return the width of the dungeon as an integer.
        '''
        return self._dungeon_size

    def init_game_information(self) -> dict:
        """
        This method should return a dictionary containing the position and the corresponding Entity as the
        keys and values respectively. This method also sets the Player’s position. At the start of the
        game this method should be called to find the position of all entities within the current dungeon.

        Returns:
            d(dict<tuple<int, int>): Return a dictionary containing the position and the corresponding Entity.
        """
        d = {}
        wall = Wall()
        door = Door()
        move_increase = MoveIncrease()
        key = Key()

        list_player = self.get_positions(PLAYER)
        self._player.set_position(list_player[0])

        list_key = self.get_positions(KEY)
        if list_key:
            d[list_key[0]] = key

        list_door = self.get_positions(DOOR)
        d[list_door[0]] = door

        list_wall = self.get_positions(WALL)
        for i in list_wall:
            d[i] = wall

        list_move_increase = self.get_positions(MOVE_INCREASE)
        for i in list_move_increase:
            d[i] = move_increase

        return d

    def get_game_information(self) -> dict:
        """
        Returns a dictionary containing the position and the corresponding Entity, as the keys and values, for the
        current dungeon.

        Returns:
            d(dict<tuple<int, int>): Return a dictionary containing the position and the corresponding Entity.
        """
        d = {}
        wall = Wall()
        door = Door()
        move_increase = MoveIncrease()
        key = Key()

        list_key = self.get_positions(KEY)
        if list_key:
            d[list_key[0]] = key

        list_door = self.get_positions(DOOR)
        d[list_door[0]] = door

        list_wall = self.get_positions(WALL)
        for i in list_wall:
            d[i] = wall

        list_move_increase = self.get_positions(MOVE_INCREASE)
        for i in list_move_increase:
            d[i] = move_increase

        return d

    def get_player(self):
        """
        This method returns the Player object within the game.

        Returns:
            Player: Return Player object within the game.
        """
        return self._player

    def get_entity(self, position):
        """
        Returns an Entity at a given position in the dungeon. Entity in the given direction or if the position is off
        map then this function should return None

        Parameters:
            position(tuple<int,int>): Position of the Entity to be returned.

        Returns:
            Entity or None: Return the Entity in the given direction.

        """
        d = self.get_game_information()
        if position in d:
            return d[position]
        else:
            return None

    def get_entity_in_direction(self, direction):
        """
        Returns an Entity in the given direction of the Player’s position. If there is no Entity in the given direction
        or if the direction is off map then this function should return None.

        Parameters:
            direction(str): Direction of the Player’s position.

        Returns:
            Entity: Return the Entity at the given direction.

        """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def collision_check(self, direction) -> bool:
        """
        Returns ​False​ if a player can travel in the given direction, they won’t collide. ​True, they will collide,
        otherwise

        Parameters:
            direction(str):The given direction of the player to travel.

        Returns:
            bool: Return ​False​ if a player can travel in the given direction. ​True, they will collide.
        """
        entity = self.get_entity_in_direction(direction)
        if entity:
            return not entity.can_collide()
        else:
            return False

    def new_position(self, direction) -> tuple:
        """
        Returns a tuple of integers that represents the new position given the direction.

        Parameters:
            direction(str):Given the direction to be updated.

        Returns:
            new_position(tuple<int,int>): Return the new position given the direction.
        """
        dx, dy = DIRECTIONS[direction]
        x, y = self._player.get_position()
        new_position = (x + dx, y + dy)
        return new_position

    def move_player(self, direction) -> None:
        """
        Update the Player’s position to place them one position in the given direction.

        Parameters:
            direction(str): New position of the player.
        """
        new_position = self.new_position(direction)
        self._player.set_position(new_position)

    def check_game_over(self) -> bool:
        """
        Return True if the game has been ​lost and False otherwise.

        Returns:
            bool: Return True if the game has been ​lost and False otherwise.
        """
        if self._player.moves_remaining() == 0:
            return True
        else:
            return False

    def set_win(self, win) -> None:
        """
        Set the game’s win state to be True or False.

        Parameters:
            win(bool): The game’s win state to be True or False.
        """
        self._win = win

    def won(self) -> bool:
        """
        Return game’s win state.

        Returns:
            bool:Return game’s win state.
        """
        return self._win


class GameApp:
    """
    GameApp acts as a communicator between the GameLogic and the Display. GameApp should be constructed with ​GameApp()​.
    """

    def __init__(self):
        """
        Constructor of the GameApp class.
        """
        self._game = GameLogic()

    def play(self) -> None:
        """
        Handles the player interaction.
        """
        while not self._game.won() and not self._game.check_game_over():
            self.draw()
            action = input("Please input an action: ")
            if action == HELP:
                print(HELP_MESSAGE)
            elif action == QUIT:
                q = input("Are you sure you want to quit? (y/n): ")
                if q == 'y':
                    return
            elif action in DIRECTIONS:
                entity = self._game.get_entity_in_direction(action)
                if not self._game.collision_check(action):
                    self._game.move_player(action)
                else:
                    print(INVALID)
                self._game.get_player().change_move_count(-1)
                if entity and entity.can_collide():
                    entity.on_hit(self._game)
            else:
                actions = action.split()
                if actions and actions[0] == INVESTIGATE and actions[1] in DIRECTIONS:
                    entity = self._game.get_entity_in_direction(actions[1])
                    print(str(entity) + " is on the " + actions[1] + " side.")
                    self._game.get_player().change_move_count(-1)
                else:
                    print(INVALID)
        if self._game.won():
            print(WIN_TEXT)
        elif self._game.check_game_over():
            print(LOSE_TEST)

    def entity_in_direction(self, direction):
        """
        Returns the Entity in a given direction.

        Parameters:
            direction: The given direction of the Entity.

        Returns:
            Entity: Returns the Entity in a given direction.
        """
        self._game.get_entity_in_direction(direction)

    def draw(self) -> None:
        """
        Displays the dungeon with all Entities in their positions.
        """
        game_information = self._game.get_game_information()
        dungeon_size = self._game._dungeon_size
        display = Display(game_information, dungeon_size)

        player_pos = self._game.get_player().get_position()
        display.display_game(player_pos)

        moves = self._game.get_player().moves_remaining()
        display.display_moves(moves)
    # pass


class Entity:
    """
    Each Entity has an id, and can either be collided with (two entities can be in the same position)
    or not (two entities cannot be in the same position.) The collidable attribute should be set to
    True for an Entity upon creation. Entity should be constructed with Entity().
    """

    def __init__(self):
        """
        Constructor of the Entity class.
        """
        self.id = 'Entity'
        self.collidable = True

    def get_id(self) -> str:
        """
        Returns a string that represents the Entity’s ID.

        Returns:
            self.id(str): Returns a string that represents the Entity’s ID.
        """
        return self.id

    def set_collide(self, collidable: bool):
        """
        Set the collision state for the Entity to be True

        Parameters:
            collidable(bool): The collision state for the Entity.
        """
        self.collidable = collidable

    def can_collide(self) -> bool:
        """
        Returns True if the Entity can be collided with (another Entity can share the position that this one is in)
        and False otherwise.

        Returns:
            bool: Returns True if the Entity can be collided with and False otherwise.
        """
        return self.collidable

    def __str__(self) -> str:
        """
        Returns the string representation of the Entity. e.g. "Entity('Entity')"

        Returns:
            s(str): Return the string representation of the Entity.
        """
        s = "Entity('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()


class Wall(Entity):
    """
    A Wall is a special type of an Entity within the game.
    The Wall Entity cannot be collided with. Wall should be constructed with Wall().
    """

    def __init__(self):
        """
        Constructor of the Wall class.
        """
        self.id = WALL
        self.collidable = False

    def __str__(self) -> str:
        """
        Returns the string representation of the Wall. e.g. "Wall('#')"

        Returns:
            s(str): Return the string representation of the Wall.
        """
        s = "Wall('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()


class Item(Entity):
    """
    An Item is a special type of an Entity within the game. This is an abstract class.
    By default the Item Entity can be collided with. Item should be constructed with Item().
    """

    def __str__(self) -> str:
        """
        Returns the string representation of the Wall. e.g. "Item('Entity')"

        Returns:
            s(str): Return the string representation of the Wall.
        """
        s = "Item('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game: GameLogic):
        """
        This function should raise the NotImplementedError.

        Parameters:
            game(GameLogic): The game.
        """
        raise NotImplementedError


class Key(Item):
    """
    A Key is a special type of Item within the game.
    The Key Item can be collided with. Key should be constructed with Key().
    """

    def __init__(self):
        """
        Constructor of the Key class.
        """
        self.id = KEY
        self.collidable = True

    def __str__(self) -> str:
        """
        Returns the string representation of the Key. e.g. "Key('K')"

        Returns:
            s(str): Return the string representation of the Key.
        """
        s = "Key('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game: GameLogic) -> None:
        """
        When the player takes the Key the Key should be added to the Player’s inventory. The Key should then be
        removed from the dungeon once it’s in the Player’s inventory.

        Parameters:
            game(GameLogic): The game.
        """
        player = game.get_player()
        player.add_item(self)
        i, j = game.get_positions(KEY)[0]
        game._dungeon[i][j] = SPACE


class MoveIncrease(Item):
    """
    MoveIncrease is a special type of Item within the game. The MoveIncrease Item can be collided with. MoveIncrease
    should be constructed with MoveIncrease(moves=5: int) where moves describe how many extra moves the Player will be
    granted when they collect this Item, the default value should be 5.
    """

    def __init__(self, moves=5):
        """
        Constructor of the MoveIncrease class.

        Parameters:
            moves(int): moves describe how many extra moves the Player will be granted when they collect this Item.
        """
        self.id = MOVE_INCREASE
        self.collidable = True
        self.moves = moves

    def __str__(self) -> str:
        """
        Returns the string representation of the MoveIncrease. e.g. "MoveIncrease('M')"

        Returns:
            s(str): Return the string representation of the MoveIncrease.
        """
        s = "MoveIncrease('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game) -> None:
        """
        When the player hits the MoveIncrease (M) item the number of moves for the player increases and the M item is
        removed from the game. These actions are implemented via the on_hit method. Specifically, extra moves should
        be granted to the Player and the M item should be removed from the game.

        Parameters:
            game(GameLogic): The game.
        """
        game.get_player().change_move_count(self.moves)
        i, j = game.get_positions(MOVE_INCREASE)[0]
        game._dungeon[i][j] = SPACE


class Door(Entity):
    """
    A Door is a special type of an Entity within the game. The Door Entity can be collided with (The Player should be
    able to share its position with the Door when the Player enters the Door.) Door should be constructed with Door().
    """

    def __init__(self):
        """
        Constructor of the Door class.
        """
        self.id = DOOR
        self.collidable = True

    def __str__(self) -> str:
        """
        Returns the string representation of the Door. e.g. "Door('D')"

        Returns:
            s(str): Return the string representation of the Door.
        """
        s = "Door('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game: GameLogic) -> None:
        '''Act when the player hit the door'''
        player = game.get_player()
        inventory = player.get_inventory()
        if inventory:
            game.set_win(True)
        else:
            print("You don't have the key!")


class Player(Entity):
    """
    A Player is a special type of an Entity within the game. The Player Entity can be collided with. The Player
    should be constructed with Player(move_count: int) where moves represents how many moves a Player can have for
    the given dungeon they are in (see GAME_LEVELS).
    """

    def __init__(self, move_count):
        """
        Constructor of the Player class.

        Parameters:
            move_count(int): moves represents how many moves a Player can have for the given dungeon they are in.
        """
        self.id = PLAYER
        self.collidable = True
        self.move_count = move_count
        self.position = None
        self.inventory = []

    def set_position(self, position):
        """
        Sets the position of the Player.

        Parameters
            position(tuple<int, int>): The position of the Player.
        """
        self.position = position

    def get_position(self) -> tuple:
        """
        Returns a tuple of ints representing the position of the Player. If the Player’s position hasn’t been set yet
        then this method should return None.

        Returns:
            self.position(tuple<int, int>): Returns a tuple of ints representing the position of the Player.
        """
        return self.position

    def change_move_count(self, number):
        """
        Add the number to the Player’s move count.

        Parameters
            number(int): number to be added to the Player’s move count.
        """
        self.move_count += number

    def moves_remaining(self) -> int:
        """
        Returns an int representing how many moves the Player has left before they reach the maximum move count.

        Returns: self.move_count(int): Returns an int representing how many moves the Player has left before they
        reach the maximum move count.
        """
        return self.move_count

    def add_item(self, item):
        """
        Adds the item to the Player’s Inventory.

        Parameters:
            item(Entity): the item to be added to the Player’s Inventory.
        """
        self.inventory.append(item)

    def get_inventory(self) -> list:
        """
        Returns a list that represents the Player’s inventory. If the Player has nothing in their inventory then an
        empty list should be returned.

        Returns:
            self.inventory(list<Entity>): Returns a list that represents the Player’s inventory.
        """
        return self.inventory

    def __str__(self) -> str:
        """
        Returns the ​string representation of the Player​. e.g. "Player('O')"

        Returns:
            s(str): Returns the ​string representation of the Player
        """
        s = "Player('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()


def main():
    game = GameApp()
    game.play()


if __name__ == "__main__":
    main()
