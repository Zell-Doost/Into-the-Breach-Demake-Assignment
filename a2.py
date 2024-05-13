# DO NOT modify or add any import statements
from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable

# Name: Fazell Dost
# Student Number: 48838830
# ----------------

# Write your classes and functions here

#################################### MODEL #####################################
class Tile():
    """A class that creates the attributes and methods for all tiles"""
    def __init__(self) -> None:
        """Initialises the attributes of the base tile class' objects"""
        self._tile_repr = f'{TILE_NAME}()'
        self._tile_str = TILE_SYMBOL
        self._tile_name = TILE_NAME
        self._can_block = False

    def __repr__(self) -> str:
        """Gets a machine readable string that could be used to construct an 
            identical instance of the tile.

        Returns:
            An object declaration of the class in its current state.

        >>>tile = Tile()
        >>>tile
        Tile()

        >>>mountain = Mountain()
        >>>mountain
        Mountain()
        """
        return self._tile_repr
    
    def __str__(self) -> str:
        """Gets the character representing the type of the tile.

        Returns:
            The first character of the name of the tile's type.

        >>>tile = Tile()
        >>>str(tile)
        'T'

        >>>ground = Ground()
        >>>str(ground)
        ' '
        """
        return self._tile_str
    
    def get_tile_name(self) -> str:
        """Gets the name of the type of the tile.

        Returns:
            The name of the tile's type.

        >>>tile = Tile()
        >>>tile.get_tile_name()
        'Tile'

        >>>mountain = Mountain()
        >>>mountain.get_tile_name()
        'Mountain'
        """
        return self._tile_name
    
    def is_blocking(self) -> bool:
        """Gets True only when the tile is blocking.

        Returns:
            A boolean representing the state of whether or not the tile 
                blocks entities.

        >>>tile = Tile()
        >>>tile.is_blocking()
        False

        >>>building = Building(5)
        >>>building.is_blocking()
        True
        """
        return self._can_block

class Ground(Tile):
    """A class that creates the tile object

    Inherits:
        Tile
    """
    def __init__(self) -> None:
        """Initialises the attributes for a ground object"""
        self._tile_repr = f'{GROUND_NAME}()'
        self._tile_str = GROUND_SYMBOL
        self._tile_name = GROUND_NAME
        self._can_block = False

class Mountain(Tile):
    """A class that creates the mountain object

    Inherits:
        Tile
    """
    def __init__(self) -> None:
        """Initialises the attributes for a Mountain object"""
        self._tile_repr = f'{MOUNTAIN_NAME}()'
        self._tile_str = MOUNTAIN_SYMBOL
        self._tile_name = MOUNTAIN_NAME
        self._can_block = True
   
class Building(Tile):
    """A class that creates the building object with health

    Inherits:
        Tile
    """
    def __init__(self, initial_health: int) -> None:
        """Initialises the attributes for a Building object

        Arguments: 
            The building's initial health when the game starts.
        """
        self._tile_repr = f'{BUILDING_NAME}({initial_health})'
        self._tile_name = BUILDING_NAME
        self._health = initial_health
        self._can_block = not self.is_destroyed() #can block if not destroyed
        self._tile_str = str(self._health)
    
    def is_destroyed(self) -> bool:
        """Returns True only when the building is destroyed, and False if not.

        Returns:
            A boolean stating whether or not the building is destroyed.

        >>>building = Building(5)
        >>>building.is_destroyed()
        False

        >>>building = Building(0)
        >>>building.is_destroyed()
        True
        """
        return self._health < 1 #building is destroyed when health is below 1
    
    def damage(self, damage: int) -> None:
        """Reduces the health of the building by the amount specified. Do 
            nothing if the building is already destroyed. If the damage is 
            negative, then heal the building's health.

        Arguments: 
            The amount of damage dealt to the building.

        >>>building = Building(5)
        >>>str(building)
        '5'
        >>>building.damage(-10)
        >>>str(building)
        '9'
        >>>building.damage(2)
        >>>str(building)
        '7'
        >>>building.damage(15)
        >>>str(building)
        '0'
        >>>building.damage(-3)
        >>>str(building)
        '0'
        """
        if not self.is_destroyed():
            self._health -= damage
            if self._health < 0:
                self._health = 0
            elif self._health > 9:
                self._health = 9
            self._can_block = not self.is_destroyed()
        self._tile_str = str(self._health)
        self._tile_repr = f'{BUILDING_NAME}({self._health})'

class Board():
    """A class that creates the board that will be in use during gameplay"""
    def __init__(self, board: list[list[str]]) -> None:
        """Initialises the attributes for a Board object

        Arguments:
            The board state through a 2d list with strings.
        Preconditions:
            Each row on the board will have the same length.
            Board array will have at least one row.
            Each character on the board will be a string representation 
                provided by the previous classes.
        """
        self._board = board
        self._board_object_dictionary = {TILE_SYMBOL: Tile(), GROUND_SYMBOL: Ground(), MOUNTAIN_SYMBOL: Mountain()}
        self._object_board = []
        for row_index, row in enumerate(self._board):
            self._object_board.append([])
            for tile in row:
                if tile.isdigit():
                    self._object_board[row_index].append(Building(int(tile)))
                else:
                    self._object_board[row_index].append(self._board_object_dictionary[tile])
        self._board_repr = f'Board({self._board})'
    
    def __repr__(self) -> str:
        """Gets a machine readable string that could be used to construct an 
            identical instance of the board.

        Returns:
            An object declaration of the class in its current state.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board
        Board([[' ', '4'], ['6', 'M']])
        """
        return self._board_repr
    
    def __str__(self) -> str:
        """Gets a string representation of the board.

        Returns:
            The board, with a new line when the next row on the board 
                is reached.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>str(board)
        ' 4\n6M'
        """
        self._board_str = ""
        for row_i, row in enumerate(self._board):
            for column_i, tile in enumerate(row):
                if (row_i, column_i) in self.get_buildings():
                    self._board[row_i][column_i] = str(self.get_buildings()[(row_i, column_i)])
                    self._board_str += str(self.get_buildings()[(row_i, column_i)])
                else:
                    self._board_str += tile
            if row_i < len(self._board)-1:
                self._board_str += "\n"
        return self._board_str
    
    def get_dimensions(self) -> tuple[int, int]:
        """Gets the (#rows, #columns) dimensions of the board.

        Returns:
            The dimenstions of the board in a tuple in the 
                form (#rows, #columns)
        Preconditions:
            Each row on the board will have the same length.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board.get_dimensions()
        (2, 2)
        """
        return len(self._board), len(self._board[0])
    
    def get_tile(self, position: tuple[int, int]) -> Tile:
        """Gets the Tile instance located at the given position.

        Arguments:
            The position of the desired tile in a tuple: (row, column).
        Returns:
            The tile object at the given position.
        Preconditions:
            The provided position will not be out of bounds.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board.get_tile((0, 1))
        Building(4)
        """
        return self._object_board[position[0]][position[1]]

    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """Gets a dictionary mapping the positions of buildings to the 
            building instances at those positions.

        Returns:
            A dictionary with the object's buildings with their positions 
                as their keys.
        
        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board.get_buildings()
        {(0, 1): Building(4), (1, 0): Building(6)}
        """
        building_dictionary = dict()
        for row_i, row in enumerate(self._board):
            building_dictionary.update({(row_i, column_i): self.get_tile((row_i, column_i)) for column_i, column in enumerate(row) if column.isdigit()})
        return building_dictionary

class Entity():
    """A class that creates the base for all entity objects, which include 
        mechs and enemies"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the entity class as well as all of 
            its children
        Arguments:
            position: a tuple with 2 ints that determines the starting row and 
                column of the entity.
            initial_health: the starting health of the entity.
            speed: the number of squares the mech can traverse in one turn.
            strength: the damage or healing power of the entity
        """
        self._position = position
        self._health = initial_health
        self._speed = speed
        self._strength = strength
        self._friendly = False
        self._entity_name = ENTITY_NAME
        self._entity_symbol = ENTITY_SYMBOL
        self._str_repr_updater()
    
    def _str_repr_updater(self):
        """Updates the entities variables for __repr__ and __str__, to be used 
            whenever the attributes of an entity change.
        
        >>>e1 = Entitiy((1, 1), 6, 3, 3)
        >>>e1
        Entity((1, 1), 6, 3, 3)
        >>>str(tank)
        'E,1,1,6,3,3'
        e1.damage(4) #Has _str_repr_updater inside damage function
        >>>e1
        Entity((1, 1), 2, 3, 3)
        >>>str(e1)
        'E,1,1,2,3,3'
        """
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._entity_repr = f'{self._entity_name}({self._position}, {self._health}, {self._speed}, {self._strength})'

    def __repr__(self) -> str:
        """Gets a machine readable string that could be used to construct an 
            identical instance of the entity.

        Returns:
            An object declaration of the class in its current state.
        
        >>>e1 = Entity((0,0),1,1,1)
        >>>e1
        Entity((0, 0), 1, 1, 1)
        """
        return self._entity_repr

    def __str__(self) -> str:
        """Gets the string representation of the entity, with all 
            of its attributes.

        Returns:
            A string containing the entity's position, health, 
                strength and speed.
        
        >>>e1 = Entity((0,0),1,1,1)
        >>>str(e1)
        'E,0,0,1,1,1'
        """
        return self._entity_str

    def get_symbol(self) -> str:
        """Gets the character that represents the entity type.

        Returns:
            The entity's symbol representation, being the 
                first letter of its name.
        
        >>>e1 = Entity((0,0),1,1,1)
        >>>e1.get symbol()
        'E'

        >>>mech = Mech((0, 0),1,1)
        >>>mech.get_symbol()
        'M'
        """
        return self._entity_symbol

    def get_name(self) -> str:
        """Gets a string of the name of the entity, specifically 
            the class' name.

        Returns:
            The entity's name.

        >>>e1 = Entity((0,0),1,1,1)
        >>>e1.get_name()
        'Entity'

        >>>tank = TankMech((0, 0), 1, 1, 1)
        >>>tank.get_name()
        'TankMech'
        """
        return self._entity_name

    def get_position(self) -> tuple[int, int]:
        """Gets the (row, column) position currently occupied by the entity.

        Returns:
            A tuple with the (row, column) position of the entity.

        >>>e1 = Entity((3,5),1,1,1)
        >>>e1.get_position()
        (3, 5)

        >>>heal = HealMech((4,2),1,1,1)
        >>>heal.get_position()
        (4, 2)
        """
        return self._position

    def set_position(self, position: tuple[int, int]) -> None:
        """Moves the entity to the specified position.

        Arguments:
            The position to place the entity within the grid.

        >>>e1 = Entity((3,5),1,1,1)
        >>>e1.get_position()
        (3, 5)
        >>>e1,set_postion((6, 3))
        >>>e1.get_position()
        (6, 3)
        """
        self._position = position
        self._str_repr_updater()

    def get_health(self) -> int:
        """Gets the current health of the entity

        Returns:
            The health value of the entity.

        >>>e1 = Entity((1,1),4,1,1)
        >>>e1.get_health()
        4

        >>>scorpion = Scorpion((1,1),9,1,1)
        >>>scorpion.get_health()
        9
        """
        return self._health

    def get_speed(self) -> int:
        """Gets the speed of the entity

        Returns:
            The speed value of the entity.

        >>>e1 = Entity((1,1),1,3,1)
        >>>e1.get_speed()
        3

        >>>firefly = Firefly((1,1),1,5,1)
        >>>firefly.get_speed()
        5
        """
        return self._speed

    def get_strength(self) -> int:
        """Gets the strength of the entity

        Returns:
            The strength value of the entity.

        >>>e1 = Entity((1,1),1,1,2)
        >>>e1.get_strength()
        2

        >>>tank = TankMech((1,1),1,1,8)
        >>>tank.get_strength()
        8
        """
        if self.get_symbol() == HEAL_SYMBOL:
            return -self._strength
        return self._strength

    def damage(self, damage: int) -> None:
        """Gets the health of the entity by the amount specified. If the 
            entity is a heal mech, then the damage will return negative, then 
            heal the targeted entity. Do nothing if the enemy is dead.
        
        Arguments:
            The amount of damage that will be dealt to the entity.

        >>>tank = TankMech((1, 1), 6, 3, 3)
        >>>tank
        TankMech((1, 1), 6, 3, 3)
        >>>str(tank)
        'T,1,1,6,3,3'
        tank.damage(4)
        >>>tank
        TankMech((1, 1), 2, 3, 3)
        >>>str(tank)
        'T,1,1,2,3,3'
        """
        #MIGHT NEED TO REMOVE HEALTH CAP FOR ENTIITIES
        #MIGHT BE ABLE TO REMOVE self.is_alive() CHECK SINCE DEAD ENEMY WILL NEVER GET TARGETED
        if self.is_alive():
            self._health -= damage
            if self._health < 0:
                self._health = 0
            elif self._health > 9:
                self._health = 9
            self._str_repr_updater()
    
    def is_alive(self) -> bool:
        """Returns True if and only if the entity is not destroyed.

        Returns:
            Returns whether or not the entity is alive.

        >>>e1 = Entity((1,1),5,3,2)
        >>>e1.is_alive()
        True
        >>>e1.damage(3)
        >>>e1.is_alive()
        True
        >>>e1.damage(5)
        >>>e1.is_alive()
        False
        """
        return self._health > 0

    def is_friendly(self) -> bool:
        """Returns True if and only if the entity is friendly. By default, 
            entities are not friendly.

        Returns:
            The boolean of whether or not the entity is friendly.

        >>>e1 = Entity((1,1),1,1,1)
        >>>e1.is_friendly()
        False
        >>>tank = TankMech((1,1),1,1,1)
        >>>tank.is_friendly()
        True
        >>>scorpion = Scorpion((1,1),1,1,1)
        >>>scorpion.is_friendly()
        False
        """
        return self._friendly

    def get_targets(self) -> list[tuple[int, int]]:
        """Gets the positions that would be attacked by the entity during a 
            combat phase. By default, entities target vertically and 
            horizontally adjacent tiles.

        Returns:
            A list containing all the positions that the entity will 
                target when attacking.

        >>>e1 = Entity((1,1),1,1,1)
        [(0,1),(2,1),(1,0),(2,0)]
        """
        #Default and heal mech targets, 1 space in 4 cardinal directions
        targets = [(self._position[0]-1, self._position[1]), (self._position[0]+1, self._position[1]), (self._position[0], self._position[1]-1), (self._position[0], self._position[1]+1)] #This sucks but I'll fix it later
        #Tank mech targets, 5 spaces in each direction horizontally
        if self.get_symbol() == TANK_SYMBOL:
            targets = [(self._position[0], self._position[1]+tile_index) for tile_index in range(-5, 6) if tile_index != 0]
        #Scorpion targets, 2 spaces in 4 cardinal directions
        elif self.get_symbol() == SCORPION_SYMBOL:
            targets1 = [(self._position[0], self._position[1]+tile_index) for tile_index in range(-2, 3) if tile_index != 0]
            targets2 = [(self._position[0]+tile_index, self._position[1]) for tile_index in range(-2, 3) if tile_index != 0]
            targets = targets1 + targets2 #THINK OF BETTER NAMES OR IMPROVE OTHERWISE
        #Firefly targets, 5 spaces in each direction vertcally
        elif self.get_symbol() == FIREFLY_SYMBOL:
            targets = [(self._position[0]+tile_index, self._position[1]) for tile_index in range(-5, 6) if tile_index != 0]
        return targets

    def attack(self, entity: "Entity") -> None:
        """Applies this entity’s effect to the given entity. By default, 
            entities deal damage equal to the strength of the entity.

        Arguments:
            The targeted entity that will recieve damage from this entity.

        >>>e1 = Entity((1,1),1,1,3)
        >>>e2 = Entity((1,1),5,1,1)
        >>>e1.get_strength()
        3
        >>>e2.get_health()
        5
        >>>e1.attack(e2)
        >>>e2.get_health()
        2
        """
        if self.get_symbol() == HEAL_SYMBOL and not entity.is_friendly(): #MIGHT BE A BETTER WAY OF DOING THIS (maybe self.get_strength() > 0 or entity.is_friendly(): leads to damage???)
            return
        entity.damage(self.get_strength())

class Mech(Entity):
    """A class that adapts the Entity class to create the base for all 
        friendly entities, which are tanks and healing mechs.

    Inherits:
        Entity
    """
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the Mech class as well as all of it's 
            children, inheriting certain attributes and methods from Entity.

        Arguments:
            position: a tuple with 2 ints that determines the starting 
                row and column of the mech.
            initial_health: the starting health of the mech.
            speed: the number of squares the mech can traverse in one turn.
            strength: the damage or healing power of the mech
        """
        super().__init__(position, initial_health, speed, strength)
        self._friendly = True
        self._entity_name = MECH_NAME
        self._entity_symbol = MECH_SYMBOL
        self._str_repr_updater()
        self._active_state = True

    def enable(self) -> None:
        """Sets the mech to be active, allowing it to move."""
        self._active_state = True

    def disable(self) -> None:
        """Sets the mech to not be active, disallowing it to move."""
        self._active_state = False

    def is_active(self) -> bool:
        """Returns true if and only if the mech is active.

        Returns:
            A boolean with the state of the mech's movement capability.
        
        >>>mech = Mech((1,1),1,1,1)
        >>>mech.is_active()
        True
        >>>mech.disable()
        >>>mech.is_active()
        False
        >>>mech.enable()
        >>>mech.is_active()
        True
        """
        return self._active_state

class TankMech(Mech):
    """A class that adapts the Mech class to create the class that 
        initialises a tank mech object.

    Inherits:
        Entity
        Mech
    """
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the TankMech class as well as all of 
            it's children, inheriting certain attributes and methods from Mech.

        Arguments:
            position: a tuple with 2 ints that determines the starting 
                row and column of the tank mech.
            initial_health: the starting health of the tank mech.
            speed: the number of squares the tank mech can traverse 
                in one turn.
            strength: the damage or healing power of the tank mech
        """
        super().__init__(position, initial_health, speed, strength) # there is probably a better way of doing the below lines, but hell if I know right now
        self._entity_name = TANK_NAME
        self._entity_symbol = TANK_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'

class HealMech(Mech):
    """A class that adapts the Mech class to create the class that 
        initialises a heal mech object.

    Inherits:
        Entity
        Mech
    """
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the HealMech class as well as all of 
            it's children, inheriting certain attributes and methods from Mech.

        Arguments:
            position: a tuple with 2 ints that determines the starting 
                row and column of the heal mech.
            initial_health: the starting health of the heal mech.
            speed: the number of squares the heal mech can 
                traverse in one turn.
            strength: the damage or healing power of the heal mech
        """
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = HEAL_NAME
        self._entity_symbol = HEAL_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'

class Enemy(Entity):
    """A class that adapts the Entity class to create the base for all 
        non-friendly entities, which are scorpions and fireflies.

    Inherits:
        Entity
    """
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the Enemy class as well as all of it's 
            children, inheriting certain attributes and methods from Entity.

        Arguments:
            position: a tuple with 2 ints that determines the starting 
                row and column of the enemy.
            initial_health: the starting health of the enemy.
            speed: the number of squares the enemy can traverse in one turn.
            strength: the damage or healing power of the enemy.
        """
        super().__init__(position, initial_health, speed, strength)
        self._friendly = False
        self._entity_name = ENEMY_NAME
        self._entity_symbol = ENEMY_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True
        self._objective = self._position

    def get_objective(self) -> tuple[int, int]:
        """Gets the current objective of the enemy.

        Returns:
            A tuple, being the position of the enemy's objective.
        """
        return self._objective

    def update_objective(
    self, 
    entities: list[Entity], 
    buildings: dict[tuple[int, int], Building]
    ) -> None:
        """Updates the objective of the enemy based on a list of entities and 
            dictionary of buildings. Scorpions target highest health mech, 
            fireflies target lowest health buildings. 
            Target own position by default.
        
        Arguments:
            entities: A list of all of the living entity objects.
            buildings: A dictionary with building objects, with their 
                keys being their positions.
        Preconditions:
            The given list of entities is sorted in descending priority order, 
                with the first entity in the list being the highest priority.

        >>>enemy = Enemy((1,1),1,1,1)
        entities = [enemy]
        buildings = {}
        enemy.update_objective()
        >>>enemy.get_objective()
        (1, 1)

        >>>tank = TankMech((1,6),9,1,1)
        >>>scorpion = Scorpion((8,8),1,1,1)
        entities = [tank, scorpion]
        buildings = {}
        enemy.update_objective()
        >>>scorpion.get_objective()
        (1, 6)
        """
        #Default target, being the enemy's current position
        objective = self._position
        #Scorpion targets, being the highest health mech, if there is a tie, 
        #   then target the highest priority.
        if self.get_symbol() == SCORPION_SYMBOL:
            possible_objective_healths = [entity.get_health() for entity in entities if entity.is_friendly()]
            if possible_objective_healths:
                objective = entities[possible_objective_healths.index(max(possible_objective_healths))].get_position() #gets the index of the highest priority entity with the most health and and sets objective to its position
        #Firefly targets, being the lowest health building, if there is a tie, 
        #   target the right most, bottom most.
        elif self.get_symbol() == FIREFLY_SYMBOL:
            possible_objectives = [(building_position, buildings[building_position]) for building_position in buildings if not buildings[building_position].is_destroyed()]
            possible_objective_healths = [int(str(healths[1])) for healths in possible_objectives]
            possible_objectives = [objective[0] for objective in possible_objectives if int(str(objective[1])) == min(possible_objective_healths)]
            objective = possible_objectives[0]
            for possible_objective in possible_objectives: #figure out a way to skip first iteration or change objective declaration
                if possible_objective[0] > objective[0]:
                    objective = possible_objective
                elif possible_objective[0] == objective[0]:
                    if possible_objective[1] > objective[1]:
                        objective = possible_objective

        self._objective = objective


class Scorpion(Enemy):
    """A class that adapts the Enemy class to create the class that 
        initialises a scorpion object

    Inherits:
        Entity
        Enemy
    """
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the Scorpion class including all of it's
             children, inheriting certain attributes and methods from Enemy.

        Arguments:
            position: a tuple with 2 ints that determines the starting 
                row and column of the scorpion.
            initial_health: the starting health of the scorpion.
            speed: the number of squares the scorpion can traverse in one turn.
            strength: the damage or healing power of the scorpion.
        """
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = SCORPION_NAME
        self._entity_symbol = SCORPION_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True

class Firefly(Enemy):
    """A class that adapts the Enemy class to create the class that 
        initialises a firefly object

    Inherits:
        Entity
        Enemy
    """
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the Firefly class including all of it's 
            children, inheriting certain attributes and methods from Enemy.

        Arguments:
            position: a tuple with 2 ints that determines the starting 
                row and column of the firefly.
            initial_health: the starting health of the firefly.
            speed: the number of squares the firefly can traverse in one turn.
            strength: the damage or healing power of the firefly.
        """
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = FIREFLY_NAME
        self._entity_symbol = FIREFLY_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True
    
class BreachModel():
    """A class that creates the object for the model, which determines 
        all of the logic within the game."""
    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """Initialises the model's board and entities to adapt and change.
        
        Arguments:
            board: The board object at the beginning of the game state.
            entities: The list of entities at the beginning of the game state.
        Preconditions:
            The provided list of entities is in descending priority order, 
                with the highest priority entity being the first element of 
                the list, and the lowest priority entity being the last 
                element of the list.
        """
        self._board = board
        self._entities = entities
        self._is_move_made = False

    def __str__(self) -> str:
        """Gets the string representation of the model.

        Returns:
            The string representation of the game board, followed by a 
                blank line, followed by the string representation of all game 
                entities in descending priority order, separated by 
                newline characters.
        
        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>str(model)
        'MMMMMMMMMM\nM        M\nM    3   M\nM   3M   M\nM        M\nM2       M
        \nM2   MMMMM\nM2     MMM\nM        M\nMMMMMMMMMM\n\nT,1,1,5,3,3\n
        T,1,2,3,3,3\nH,1,3,2,3,2\nS,8,8,3,3,2\nF,8,7,2,2,1\nF,7,6,1,1,1'
        """
        string_representation = f'{str(self._board)}\n'
        for entity in self._entities:
            string_representation += "\n"
            string_representation += str(entity)
        return string_representation

    def get_board(self) -> Board:
        """Gets the board object of the model

        Returns:
            The current board instance.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>model.get_board()
        Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], ['M', ' ', 
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',' ', '3', 
        ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', ' ', 'M']
        , ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', 
        ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M', 'M',
         'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'], 
         ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
         'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        """
        return self._board

    def get_entities(self) -> list[Entity]:
        """Gets a list of all of the entities
        
        Returns:
            The list of all entities in descending priority order, with the 
                highest priority entity being the first element of the list.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>model.get_entities()
        [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        """
        return self._entities

    def has_won(self) -> bool:
        """Returns True iff the game is in a win state according to the game 
            rules. The player wins if at least one mech and one building is 
            alive, and all enemies are dead.

        Returns:
            A boolean representing whether or not the player has won or not.

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),9,9,9), Scopion((0,1),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model.has_won()
        False
        >>>model.make_attack(model.get_entities()[0])
        >>>model.has_won()
        True
        """
        building_dict = [self.get_board().get_buildings()[building_position] for building_position in self.get_board().get_buildings() if not self.get_board().get_buildings()[building_position].is_destroyed()]
        building_check = bool(len(building_dict) > 0)
        entity_list = [entity.get_symbol() for entity in self._entities if entity.is_alive()]
        mech_alive_check = bool(TANK_SYMBOL in entity_list or HEAL_SYMBOL in entity_list)
        enemy_dead_check = bool(SCORPION_SYMBOL not in entity_list and FIREFLY_SYMBOL not in entity_list)
        return building_check and mech_alive_check and enemy_dead_check

    def has_lost(self) -> bool:
        """Returns True iff the game is in a loss state according to the 
            game rules. The player loses if all mechs and buildings are dead.

        Returns:
            A boolean representing whether or not the player has lost or not.

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),1,1,1), Scopion((0,1),9,9,9)]
        >>>model = BreachModel(board, entities)
        >>>model.has_lost()
        False
        >>>model.make_attack(model.get_entities()[1])
        >>>model.has_lost()
        True
        """
        #REPEATED CODE, NEED TO FIX
        building_dict = [self._board.get_buildings()[building_position] for building_position in self._board.get_buildings() if not self._board.get_buildings()[building_position].is_destroyed()]
        building_check = bool(len(building_dict) == 0)
        entity_list = [entity.get_symbol() for entity in self._entities if entity.is_alive()]
        mech_dead_check = bool(TANK_SYMBOL not in entity_list and HEAL_SYMBOL not in entity_list)
        return building_check or mech_dead_check

    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """Gets a dictionary containing all entities, indexed by 
            entity position.
        
        Returns:
            A dictionary with all of the entities, where the key is the 
                corresponding entity's position in a tuple.

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),1,1,1), Scopion((0,1),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model.entity_positions
        {(0, 0): TankMech((0,0),1,1,1), (0, 1): Scopion((0,1),1,1,1)}
        """
        entity_position_dict = {entity.get_position(): entity for entity in self._entities}
        return entity_position_dict

    def get_valid_movement_positions(self, 
    entity: Entity
    ) -> list[tuple[int, int]]:
        """Gets the list of positions that the given entity could move to 
            during the relevant movement phase.

        Arguments:
            entity: The entity for which the valid positions are requires.
        Returns:
            The list of positions that the given entity can move. The list 
                should be ordered such that positions in higher rows appear 
                before positions in lower rows. Within the same row, positions 
                in columns further left should appear before positions in 
                columns further right.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>tank = model.entity_positions()[(1,1)]
        >>>model.get_valid_movement_positions(tank)
        [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (4, 1)]
        """
        possible_moves = []
        pos = entity.get_position() #pos stands for the position of the mech
        for i in range(-entity.get_speed(), entity.get_speed()+1):
            for j in range(-abs(entity.get_speed()-abs(i)), abs(entity.get_speed()-abs(i))+1):
                distance = get_distance(self, pos, (pos[0]+i, pos[1]+j))
                if entity.get_speed() >= distance > 0:
                    possible_moves.append((pos[0]+i, pos[1]+j))
        return possible_moves

    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """Moves the given entity to the specified position only if the entity 
            is friendly, active, and can move to that position according to 
            the game rules. Does nothing otherwise. Disables entity if a 
            successful move is made.
        
        Arguments:
            entity: The entity that needs to be moved.
            position: The position to move the given entity to.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>tank = model.entity_positions()[(1,1)]
        >>>model.attempt_move(tank, (2,1))
        >>>model.entity_positions()
        {(2, 1): TankMech((2, 1), 5, 3, 3), (8, 5): Scorpion((8, 5), 3, 3, 2), 
        (7, 5): Firefly((7, 5), 1, 1, 1)}
        """
        if entity.is_friendly() and entity.is_active() and position in self.get_valid_movement_positions(entity):
            entity.set_position(position)
            entity.disable()
            self._is_move_made = True

    def ready_to_save(self) -> bool:
        """Returns true only when no move has been made since the last 
            call to end turn.

        Returns:
            Returns whether or not the player can save under the current 
                circumstances.

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),1,1,1), Scopion((0,1),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model.ready_to_save()
        True
        >>>tank = model.entity_positions()[(0,0)]
        >>>model.attempt_move(tank, (1, 0))
        >>>model.ready_to_save()
        False
        """
        return not self._is_move_made

    def assign_objectives(self) -> None:
        """Updates the objectives of all enemies based on the current 
            game state.

        >>>board = Board([[' ', ' ', '4', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),1,1,1), TankMech((1,3),5,1,1) Scopion((0,1),1,1,1), Firefly((0, 3),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model.assign_objectives()
        >>>scorpion = model.entity_positions()[(0,1)]
        >>>scorpion.get_objective()
        (1, 3)
        >>>firefly = model.entity_positions()[(0,3)]
        >>>firefly.get_objective()
        (0, 2)
        """
        mechs = [entity for entity in self._entities if entity.get_symbol() in [MECH_SYMBOL, TANK_SYMBOL, HEAL_SYMBOL] and entity.is_alive()]
        buildings = self._board.get_buildings()
        enemies = [entity for entity in self._entities if entity.get_symbol() in [ENEMY_SYMBOL, SCORPION_SYMBOL, FIREFLY_SYMBOL] and entity.is_alive()]
        for enemy in enemies:
            enemy.update_objective(mechs, buildings)

    def move_enemies(self) -> None:
        """Moves each enemy to the valid movement position that minimizes 
            the distance of the shortest valid path between the position and 
            the enemy’s objective. If there is a tie for minimum shortest 
            distance, the enemy moves to the position in the bottom-most row. 
            If there is still a tie for minimum shortest distance, the enemy 
            moves to the position in the rightmost column. If there is no 
            valid path from an enemy to its objective, the enemy does not 
            move. Enemies move in descending priority order starting with the 
            highest priority enemy.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), Scorpion((8, 8), 3, 3, 2), 
        Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>model.entity_positions()
        {(1, 1): TankMech((1, 1), 5, 3, 3), (8, 8): Scorpion((8, 8), 3, 3, 2), 
        (7, 6): Firefly((7, 6), 1, 1, 1)}
        >>>model.move_enemies()
        >>>model.entity_positions()
        {(1, 1): TankMech((1, 1), 5, 3, 3), (8, 5): Scorpion((8, 5), 3, 3, 2), 
        (7, 5): Firefly((7, 5), 1, 1, 1)}
        """
        #REPEATED CODE, MAKE SURE TO FIX THAT
        self.assign_objectives()
        mechs = [entity for entity in self.get_entities() if entity.get_symbol() in [MECH_SYMBOL, TANK_SYMBOL, HEAL_SYMBOL] and entity.is_alive()]
        buildings = self._board.get_buildings()
        enemies = [entity for entity in self.get_entities() if entity.get_symbol() in [ENEMY_SYMBOL, SCORPION_SYMBOL, FIREFLY_SYMBOL] and entity.is_alive()]
        enemies_need_to_move = enemies.copy()
        prev_enemies = enemies.copy()
        for enemy in enemies:
            target = enemy.get_objective()
            distance = None
            #PROBABLY NOT OPTIMISED AND KIND OF MESSY, TRY TO DO WITH ONE FOR LOOP
            
            possible_moves = self.get_valid_movement_positions(enemy)
            best_move = None
            for possible_move in possible_moves:
                distance_check = get_distance(self, target, possible_move)
                if (distance == None or distance > distance_check) and distance_check > 0:
                    distance = distance_check
                    best_move = possible_move

                elif distance == distance_check:
                    if possible_move[0] > best_move[0] or possible_move[0] == best_move[0] and possible_move[1] > best_move[1]:
                        distance = distance_check
                        best_move = possible_move #REPEATED, ASK IF IT'S OKAY

                
            if distance != None:
                for possible_move in possible_moves:
                    if get_distance(self, target, possible_move) == distance:
                        enemy.set_position(possible_move)



    def make_attack(self, entity: Entity) -> None:
        """Makes given entity perform an attack against every tile that is 
            currently a target of the entity.

        Arguments:
            entity: The entity conducting an attack on all targeted tiles.

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', '5', ' ', ' ',]])
        >>>entities = [TankMech((0,0),4,1,1), Scopion((0,1),1,1,3)]
        >>>model = BreachModel(board, entities)
        >>>model.get_entities()[0].get_health()
        4
        >>>str(model.get_board().get_buildings()[(1, 1)])
        '5'
        >>>model.make_attack(model.get_entities()[1])
        >>>model.get_entities()[0].get_health()
        1
        >>>str(model.get_board().get_buildings()[(1, 1)])
        '2'
        """
        #THESE DICTIONARIES ARE REPEATED MULTIPLE TIMES, NEED TO FIX
        entity_dict = {ent.get_position(): ent for ent in self.get_entities() if ent.is_alive()} #ent is entity
        building_dict = self._board.get_buildings()
        targets = entity.get_targets()
        #Attack entities
        for target in targets:
            if target in entity_dict and entity.is_alive():
                entity.attack(entity_dict[target])
        entity_list = [entity_dict[entity_position] for entity_position in entity_dict if entity_dict[entity_position].is_alive()]
        self._entities = entity_list
        #Attack buildings
        for target in targets:
            if target in building_dict and entity.is_alive():
                building_dict[target].damage(entity.get_strength())

    def end_turn(self) -> None:
        """Executes the attack and enemy movement phases, then sets all mechs 
            to be active.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
        ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',
        ' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
        ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2'
        , ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ', ' ', ' ', 'M'
        , 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', 'M', 'M', 'M'
        ], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 'M', 'M', 
        'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
        HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
        Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>model.entity_positions()
        {(1, 1): TankMech((1, 1), 5, 3, 3), (1, 2): TankMech((1, 2), 3, 3, 3), 
        (1, 3): HealMech((1, 3), 2, 3, 2), (8, 8): Scorpion((8, 8), 3, 3, 2), 
        (8, 7): Firefly((8, 7), 2, 2, 1), (7, 6): Firefly((7, 6), 1, 1, 1)}
        >>>model.end_turn()
        >>>model.entity_positions()
        {(1, 1): TankMech((1, 1), 5, 3, 3), (8, 5): Scorpion((8, 5), 3, 3, 2), 
        (7, 5): Firefly((7, 5), 1, 1, 1)}
        """
        #REPEATED LIST CREATION, NEED TO FIX
        entities = self.get_entities()
        for entity in entities:
            self.make_attack(entity)
        enemies = [entity for entity in self.get_entities() if not entity.is_friendly() and entity.is_alive()]
        mechs = [entity for entity in self.get_entities() if entity.is_friendly()and entity.is_alive()]
        self.move_enemies()
        for mech in mechs:
            mech.enable()
            #REPEATED AGAIN, FIX THIS
        new_enemies = [entity for entity in enemies if not entity.is_friendly() and entity.is_alive()]
        new_mechs = [entity for entity in mechs if entity.is_friendly() and entity.is_alive()]
        self._entities = new_mechs + new_enemies


##################################### View #####################################

class GameGrid(AbstractGrid):
    """docstring for GameGrid"""
    def redraw(self, 
    board: Board, 
    entities: list[Entity], 
    highlighted: list[tuple[int, int]] = None, 
    movement: bool = False
    ) -> None:
        """docstring"""
        self.set_dimensions(board.get_dimensions())
        self._cell_size = self._get_cell_size()
        #self._entities = board.get_entities()
        #canvas = tk.Canvas(root, width=GRID_SIZE+SIDEBAR_WIDTH, height=GRID_SIZE+BANNER_HEIGHT+CONTROL_BAR_HEIGHT, bg='gray')
        self._entity_dict = {entity.get_position(): entity for entity in entities}
        self.clear()
        self.pack(side=tk.LEFT, anchor=tk.N)
        for row in range(board.get_dimensions()[0]):
            for column in range(board.get_dimensions()[1]):

                #Check for highlighted tiles
                if (row, column) in highlighted:
                    if movement:
                        self.color_cell((row, column), MOVE_COLOR)
                    else:
                        self.color_cell((row, column), ATTACK_COLOR)

                #Check for tiles and buildings
                elif str(board.get_tile((row, column))) == MOUNTAIN_SYMBOL:
                    self.color_cell((row, column), MOUNTAIN_COLOR)
                elif str(board.get_tile((row, column))) == GROUND_SYMBOL:
                    self.color_cell((row, column), GROUND_COLOR)
                elif str(board.get_tile((row, column))).isdigit():
                    if board.get_tile((row, column)).is_destroyed():
                        self.color_cell((row, column), DESTROYED_COLOR)
                    else:
                        self.color_cell((row, column), BUILDING_COLOR)
                        self.annotate_position((row, column), str(board.get_tile((row, column))), font=ENTITY_FONT)
                        

                

                #Check for entities
                if (row, column) in self._entity_dict:
                    if self._entity_dict[(row, column)].get_symbol() == TANK_SYMBOL:
                        self.annotate_position((row, column), TANK_DISPLAY, font=ENTITY_FONT)
                    elif self._entity_dict[(row, column)].get_symbol() == HEAL_SYMBOL:
                        self.annotate_position((row, column), HEAL_DISPLAY, font=ENTITY_FONT)
                    elif self._entity_dict[(row, column)].get_symbol() == SCORPION_SYMBOL:
                        self.annotate_position((row, column), SCORPION_DISPLAY, font=ENTITY_FONT)
                    elif self._entity_dict[(row, column)].get_symbol() == FIREFLY_SYMBOL:
                        self.annotate_position((row, column), FIREFLY_DISPLAY, font=ENTITY_FONT)
                
    def bind_click_callback(self, 
    click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """docstring"""
        position_action = lambda event, call_back=click_callback: call_back(self.pixel_to_cell(event.x, event.y))
        self.bind('<Button-1>', position_action)
        self.bind('<Button-2>', position_action)

class SideBar(AbstractGrid):
    """docstring for SideBar"""
    def __init__(self, 
    master: tk.Widget, 
    dimensions: tuple[int, int], 
    size: tuple[int, int]
    ) -> None:
        """docstring"""
        super().__init__(master, dimensions, size)
        #NEXT 2 LINES DECLARED IN ABSTRACT GRID, SO FIX THIS
        self._dimensions = dimensions
        self._size = size
    def display(self, entities: list[Entity]) -> None:
        """docstring"""
        self.set_dimensions((len(entities)+1, 4))
        self.pack(side=tk.LEFT, anchor=tk.N)
        self.clear()
        display = None
        for column, heading in enumerate(SIDEBAR_HEADINGS):
            self.annotate_position((0, column), heading, font=SIDEBAR_FONT)
        for row, entity in enumerate(entities):
            if entity.get_symbol() == TANK_SYMBOL:
                display = TANK_DISPLAY
            elif entity.get_symbol() == HEAL_SYMBOL:
                display = HEAL_DISPLAY
            elif entity.get_symbol() == SCORPION_SYMBOL:
                display = SCORPION_DISPLAY
            elif entity.get_symbol() == FIREFLY_SYMBOL:
                display = FIREFLY_DISPLAY
            self.annotate_position((row+1, 0), display, font=SIDEBAR_FONT)
            self.annotate_position((row+1, 1), f'({entity.get_position()[0]}, {entity.get_position()[1]})', font=SIDEBAR_FONT)
            self.annotate_position((row+1, 2), entity.get_health(), font=SIDEBAR_FONT)
            self.annotate_position((row+1, 3), entity.get_strength(), font=SIDEBAR_FONT)

class ControlBar(tk.Frame):
    def __init__(self, 
    master: tk.Widget, 
    save_callback: Optional[Callable[[], None]] = None, 
    load_callback: Optional[Callable[[], None]] = None, 
    turn_callback: Optional[Callable[[], None]] = None, 
    **kwargs
    ) -> None:
        """docstring"""
        super().__init__(master)
        self._save_callback = save_callback
        self._load_callback = load_callback
        self._turn_callback = turn_callback
        self.pack(side=tk.BOTTOM, fill=tk.X)
        # self.rowconfigure(1, weight=1)
        # self.columnconfigure(1, weight=1)
        padding = (GRID_SIZE+SIDEBAR_WIDTH)/7 #THIS IS WRONG METHOD OF DOING THIS, FIX
        self.grid_columnconfigure((0,1,2), weight=1, uniform="column", pad=padding)
        button_texts = [SAVE_TEXT, LOAD_TEXT, TURN_TEXT]
        button_commands = [save_callback, load_callback, turn_callback]
        for text, command in zip(button_texts, button_commands):
            button = tk.Button(self, text=text, command=command)
            button.pack(side=tk.LEFT, expand=tk.TRUE) #PADDING IS INCORRECT I THINK
        # button = tk.Button(self, text=TURN_TEXT, command=turn_callback)
        # button.pack(side=tk.LEFT, expand=tk.TRUE)
        # self._buttons = [tk.Button(self, text=button[0], command=button[1]) for button in zip(button_texts, button_commands)]
        # for i, button in enumerate(self._buttons):
        #     button.grid(column=i, row=0)



class BreachView():
    """docstring for BreachView"""
    def __init__(self, 
    root: tk.Tk, 
    board_dims: tuple[int, int], 
    save_callback: Optional[Callable[[], None]] = None, 
    load_callback: Optional[Callable[[], None]] = None, 
    turn_callback: Optional[Callable[[], None]] = None, 
    ) -> None:
        """docstring"""
        # if self._game_grid:
        #     self._game_grid.destroy()
        #     self._side_bar.destroy()
        self._root = root
        self._root.title(BANNER_TEXT)
        self._root.geometry(f'{GRID_SIZE+SIDEBAR_WIDTH}x{GRID_SIZE+BANNER_HEIGHT+CONTROL_BAR_HEIGHT}')
        # self._root.geometry('750x625')
        # self._root.geometry('625x750')
        self._banner = tk.Label(self._root, text=BANNER_TEXT, font=BANNER_FONT)
        self._banner.pack(fill=tk.X)
        self._game_grid = GameGrid(self._root, board_dims, (GRID_SIZE, GRID_SIZE))

        self._side_bar = SideBar(self._root, (0, 0), (SIDEBAR_WIDTH, GRID_SIZE))#2ND ARG SHOULD BE AMOUNT OF ENTITIES+1 instead of 7
        self._control_bar = ControlBar(self._root, save_callback, load_callback, turn_callback)
    def bind_click_callback(self, 
    click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """docstring"""
        self._game_grid.bind_click_callback(click_callback) #CHANGE CALLABLE FUNCTION

    def _clear_all(self):
        """docstring"""
        # self._banner.delete("all")
        
        # self._control_bar.delete("all")
        pass


    def redraw(self, 
    board: Board, 
    entities: list[Entity], 
    highlighted: list[tuple[int, int]] = None, 
    movement: bool = False
    ) -> None:
        """docstring"""
        # self._game_grid.destroy()
        # self._side_bar.destroy()
        self._game_grid.redraw(board, entities, highlighted=highlighted, movement=movement)
        self._side_bar.display(entities)





################################## Controller ##################################

class IntoTheBreach():
    """docstring for IntoTheBreach"""
    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """docstring"""


        self._root = root
        self._view = None
        self.load_model(game_file)
        
        
        

    def redraw(self) -> None:
        """docstring"""
        self._view.redraw(self._model.get_board(), self._model.get_entities(), highlighted=self._highlighted, movement=self._moving)
        # self._view.redraw(self._board, self._entities, highlighted=self._highlighted, movement=self._moving)

    def set_focused_entity(self, entity: Optional[Entity]) -> None:
        """docstring"""

        #NEED BELOW LINE FOR CLICK HANDLING PROBABLY
        #set_focused_entity(self._find_focused_entity)
        #self._view.bind_click_callback(self._find_focused_entity)
        if entity:
            self._focused_entity = entity
            if entity.is_friendly() and entity.is_active():
                self._moving = True
                self._highlighted = self._model.get_valid_movement_positions(entity)
            else:
                self._moving = False
                self._highlighted = entity.get_targets()
        else:
            self._focused_entity = None
            self._highlighted = []

    def make_move(self, position: tuple[int, int]) -> None:
        """docstring"""
        if position in self._highlighted:
            self._model.attempt_move(self._focused_entity, position)

    def load_model(self, file_path: str) -> None:
        """docstring"""
        # self._view.clear_all()
        self._current_file_path = file_path
        if self._current_file_path:
            file = open(self._current_file_path, 'r')
            self._game_file = file
            board = []
            entities = []
            is_on_board = True
            for line in file:
                if line == '\n':
                    is_on_board = False
                if is_on_board: #take board
                    board.append([char for char in line if char != '\n'])
                elif line != '\n': #take entities
                    stats_str = line[2:].split(',')
                    stats = [(int(stats_str[0]), int(stats_str[1])), int(stats_str[2]), int(stats_str[3]), int(stats_str[4].replace('\n', ''))]
                    if line[0] == TANK_SYMBOL:
                        entities.append(TankMech(stats[0], stats[1], stats[2], stats[3]))
                    elif line[0] == HEAL_SYMBOL:
                        entities.append(HealMech(stats[0], stats[1], stats[2], stats[3]))
                    elif line[0] == SCORPION_SYMBOL:
                        entities.append(Scorpion(stats[0], stats[1], stats[2], stats[3]))
                    elif line[0] == FIREFLY_SYMBOL:
                        entities.append(Firefly(stats[0], stats[1], stats[2], stats[3]))
            file.close()
        
            self._board = Board(board)
            self._entities = entities
            self._model = BreachModel(self._board, self._entities)
            if not self._view:
                self._view = BreachView(self._root, self._model.get_board().get_dimensions(), save_callback=self._save_game, load_callback=self._load_game, turn_callback=self._end_turn)
            self._focused_entity = 0
            self._highlighted = []
            self._moving = False
            self._view.bind_click_callback(click_callback=self._handle_click)
            self.redraw()
    def _save_game(self) -> None:
        """docstring"""
        if self._model.ready_to_save():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("text file", "*.txt"), ("All Files", "*.*"))) #Parameters gotten from https://stackoverflow.com/questions/16089674/restricting-the-file-extension-saved-when-using-tkfiledialog-asksaveasfile
            if file_path:
                save_board = str(self._board)
                #IN THIS LINE, SET ENTITIES SAVE THING
                save_entities = [str(entity) for entity in self._entities if entity.is_alive()]
                save_file = open(file_path, 'w')
                save_file.write(f'{save_board}\n')
                for save_entity in save_entities:
                    save_file.write(f'\n{save_entity}')
                save_file.close()
        else:
            tk.messagebox.showerror(title=INVALID_SAVE_TITLE, message=INVALID_SAVE_MESSAGE)


    def _load_game(self) -> None:
        """docstring"""
        file_path = filedialog.askopenfilename(initialdir='')
        self.load_model(file_path)

    def _end_turn(self) -> None:
        """docstring"""
        self._model.end_turn()
        self._focused_entity = None
        self._highlighted = []
        self.redraw()
        #NEED TO CHECK FOR WIN OR LOSS
        play_again = self._game_over_box()
        if play_again != None:
            if play_again:
                self.load_model(self._current_file_path)
            else:
                self._root.destroy()

    def _game_over_box(self):
        """docstring"""
        if self._model.has_lost():
            return tk.messagebox.askyesno(title='You Lost!', message=f'You Lost! {PLAY_AGAIN_TEXT}')
        elif self._model.has_won():
            return tk.messagebox.askyesno(title='You Win!', message=f'You Win! {PLAY_AGAIN_TEXT}')
        else:
            return None


    def _handle_click(self, position: tuple[int, int]) -> None:
        """docstring"""
        entity_dict = {entity.get_position(): entity for entity in self._model.get_entities()} #MADE ENTITY DICT AGAIN, NEED BETTER WAY
        if position in entity_dict:
            self.set_focused_entity(entity_dict[position])
        else:
            if position in self._highlighted:
                self.make_move(position)
            self.set_focused_entity(None)
        self.redraw()









def play_game(root: tk.Tk, file_path: str) -> None:
    """The function that runs the game"""
    #while True:
    controller = IntoTheBreach(root, file_path)
    #controller.redraw()






    root.mainloop()

def main() -> None:
    """The main function"""
    root = tk.Tk()
    play_game(root, 'levels/level1.txt')

if __name__ == "__main__":
    main()


#NEED TO FIX:
    #LEVEL 2 NOT LOADING CORRECTLY
    #LOAD I/O ERROR STUFF

    #ENEMIES ATTACKING THROUGH WALLS? ALLOWED OR NOT?
    #REMOVE HEALTH CAP FROM ENTITIES?

#REFACTORING
    #ALL RANDOM COMMENTS
    #ALL PARTS WHERE str() IS USED INSTEAD OF get_symbol()