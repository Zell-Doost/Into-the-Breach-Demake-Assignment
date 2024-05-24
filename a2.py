# DO NOT modify or add any import statements
from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable

# Name: Fazell Dost
# Student Number: 48838830
# ----------------

# Write your classes and functions here

###############################################################################
#################################### MODEL ####################################
###############################################################################

class Tile():
    """A class that creates the attributes and methods for all tiles"""

    def __init__(self) -> None:
        """Initialises the attributes of the base tile class' objects"""
        self._tile_instance = f'{TILE_NAME}()'
        self._tile_symbol = TILE_SYMBOL
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
        return self._tile_instance
    
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
        return self._tile_symbol
    
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
        self._tile_instance = f'{GROUND_NAME}()'
        self._tile_symbol = GROUND_SYMBOL
        self._tile_name = GROUND_NAME
        self._can_block = False


class Mountain(Tile):
    """A class that creates the mountain object

    Inherits:
        Tile
    """

    def __init__(self) -> None:
        """Initialises the attributes for a Mountain object"""
        self._tile_instance = f'{MOUNTAIN_NAME}()'
        self._tile_symbol = MOUNTAIN_SYMBOL
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
        self._tile_instance = f'{BUILDING_NAME}({initial_health})'
        self._tile_name = BUILDING_NAME
        self._health = initial_health
        self._can_block = not self.is_destroyed() #can block if not destroyed
        self._tile_symbol = str(self._health)
    
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
        self._tile_symbol = str(self._health)
        self._tile_instance = f'{BUILDING_NAME}({self._health})'


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
        self._board_symbol_to_object = {TILE_SYMBOL: Tile(), 
            GROUND_SYMBOL: Ground(), MOUNTAIN_SYMBOL: Mountain()}
        self._object_board = []
        for row_index, row in enumerate(self._board):
            self._object_board.append([])
            for tile in row:
                if tile.isdigit():
                    self._object_board[row_index].append(Building(int(tile)))
                else:
                    self._object_board[row_index].append(
                        self._board_symbol_to_object[tile])
        self._board_instance = f'Board({self._board})'
    
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
        return self._board_instance
    
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
        self._board_elements = ""
        for row_i, row in enumerate(self._board):
            for column_i, tile in enumerate(row):
                if (row_i, column_i) in self.get_buildings():
                    self._board[row_i][column_i] = (str(
                        self.get_buildings()[(row_i, column_i)]))
                    self._board_elements += (str(
                        self.get_buildings()[(row_i, column_i)]))
                else:
                    self._board_elements += tile
            if row_i < len(self._board)-1:
                self._board_elements += "\n"
        return self._board_elements
    
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
        buildings = dict()
        for row_i, row in enumerate(self._board):
            buildings.update({(row_i, column_i): 
                              self.get_tile((row_i, column_i)) 
                              for column_i, column in enumerate(row) 
                              if column.isdigit()})
        return buildings


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
        self._symbol_instance_updater()

    def __repr__(self) -> str:
        """Gets a machine readable string that could be used to construct an 
            identical instance of the entity.

        Returns:
            An object declaration of the class in its current state.
        
        >>>e1 = Entity((0,0),1,1,1)
        >>>e1
        Entity((0, 0), 1, 1, 1)
        """
        return self._entity_instance

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
        return self._entity_stats

    def _symbol_instance_updater(self) -> None:
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
        self._entity_stats = (self._entity_symbol + ',' +
                              str(self._position[0]) + ',' +
                              str(self._position[1]) + ',' +
                              str(self._health) + ',' +
                              str(self._speed) + ',' +
                              str(self._strength))
        self._entity_instance = (f'{self._entity_name}((' +
                                 f'{str(self._position[0])}, ' +
                                 f'{str(self._position[0])}), ' +
                                 f'{str(self._health)}, ' +
                                 f'{str(self._speed)}, ' +
                                 f'{str(self._strength)})')

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
        self._symbol_instance_updater()

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
        if self.is_alive():
            self._health -= damage
            if self._health < 0:
                self._health = 0
            self._symbol_instance_updater()
    
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
        targets = [(self._position[0]-1, self._position[1]), 
                   (self._position[0]+1, self._position[1]), 
                   (self._position[0], self._position[1]-1), 
                   (self._position[0], self._position[1]+1)]

        #Tank mech targets, 5 spaces in each direction horizontally
        if self.get_symbol() == TANK_SYMBOL:
            targets = [(self._position[0], self._position[1]+tile_index) 
                       for tile_index in range(-5, 6) 
                       if tile_index != 0]

        #Scorpion targets, 2 spaces in 4 cardinal directions
        elif self.get_symbol() == SCORPION_SYMBOL:
            hori_targets = [(self._position[0], self._position[1]+tile_index) 
                            for tile_index in range(-2, 3) 
                            if tile_index != 0] #horizontal
            vert_targets = [(self._position[0]+tile_index, self._position[1]) 
                            for tile_index in range(-2, 3) 
                            if tile_index != 0] #vertical
            targets = hori_targets + vert_targets

        #Firefly targets, 5 spaces in each direction vertcally
        elif self.get_symbol() == FIREFLY_SYMBOL:
            targets = [(self._position[0]+tile_index, self._position[1]) 
                       for tile_index in range(-5, 6) 
                       if tile_index != 0]
                
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
        if self.get_strength() > 0 or entity.is_friendly():
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
        self._symbol_instance_updater()
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
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = TANK_NAME
        self._entity_symbol = TANK_SYMBOL
        self._symbol_instance_updater()


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
        self._symbol_instance_updater()


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
        self._symbol_instance_updater()
        self._active_state = True
        self._objective = self._position

    def get_objective(self) -> tuple[int, int]:
        """Gets the current objective of the enemy.

        Returns:
            A tuple, being the position of the enemy's objective.

        Example of use in update_objective function.
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
            possible_objective_healths = [entity.get_health() 
                                          for entity in entities 
                                          if entity.is_friendly()]
            if possible_objective_healths:
                #gets the index of the highest priority entity with the most 
                #   health and and sets objective to its position
                #No other way to fit the below line
                objective = (entities[possible_objective_healths.index(
                    max(possible_objective_healths))].get_position())
        #Firefly targets, being the lowest health building, if there is a tie, 
        #   target the right most, bottom most.
        elif self.get_symbol() == FIREFLY_SYMBOL:
            possible_objectives = [(building_position, 
                                   buildings[building_position]) 
                                   for building_position in buildings 
                                   if not (
                                   buildings[building_position].is_destroyed()
                                   )]
            possible_objective_healths = [int(str(healths[1])) 
                for healths in possible_objectives]
            possible_objectives = [objective[0] for objective 
                in possible_objectives 
                if int(str(objective[1])) == min(possible_objective_healths)]
            objective = possible_objectives[0]
            for possible_objective in possible_objectives:
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
        self._symbol_instance_updater()
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
        self._symbol_instance_updater()
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
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
            HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
            Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>str(model)
        'MMMMMMMMMM\nM        M\nM    3   M\nM   3M   M\nM        M\nM2       M
            \nM2   MMMMM\nM2     MMM\nM        M\nMMMMMMMMMM\n\nT,1,1,5,3,3\n
            T,1,2,3,3,3\nH,1,3,2,3,2\nS,8,8,3,3,2\nF,8,7,2,2,1\nF,7,6,1,1,1'
        """
        model_elements = f'{str(self._board)}\n'
        for entity in self._entities:
            model_elements += "\n"
            model_elements += str(entity)
        return model_elements

    def get_board(self) -> Board:
        """Gets the board object of the model

        Returns:
            The current board instance.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
            HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
            Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>model.get_board()
        Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], ['M', ' ', 
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ',' ', 
            '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M', ' ', ' ', 
            ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], 
            ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', '2', ' ',
            ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', ' ', ' ', 
            ' ', 'M', 'M', 'M'],  ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            'M'], ['M', 'M', 'M',  'M', 'M', 'M', 'M', 'M', 'M', 'M']])
        """
        return self._board

    def get_entities(self) -> list[Entity]:
        """Gets a list of all of the entities
        
        Returns:
            The list of all entities in descending priority order, with the 
                highest priority entity being the first element of the list.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
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

    def _building_alive_check(self) -> bool:
        """Checks if there are any living buildings.

        Returns:
            A boolean stating whether or not there are any living buildings

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),9,9,9), Scopion((0,1),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model._building_alive_check()
        True

        >>>board = Board([[' ', ' ', ' ', ' ',], [' ', ' ', ' ', ' ',]])
        >>>entities = [TankMech((0,0),9,9,9), Scopion((0,1),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model._building_alive_check()
        False
        """
        buildings = [self.get_board().get_buildings()[building_position] 
                     for building_position in self.get_board().get_buildings() 
                     if not (self.get_board().get_buildings()[
                                            building_position].is_destroyed())]
        return bool(len(buildings) > 0)

    def _get_entity_symbols(self) -> list[str]:
        """Gets a list of all of the symbols for the currently living entities

        Returns:
            A list of symbols corresponding to which entities are 
                currently alive.
        """
        return [entity.get_symbol() 
                for entity in self._entities 
                if entity.is_alive()]

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
        entities = self._get_entity_symbols()
        mech_alive_check = bool(TANK_SYMBOL in entities or 
                                HEAL_SYMBOL in entities)
        enemy_dead_check = bool(SCORPION_SYMBOL not in entities and 
                                FIREFLY_SYMBOL not in entities)
        return (self._building_alive_check() and 
                mech_alive_check and 
                enemy_dead_check)

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
        entities = self._get_entity_symbols()
        mech_dead_check = bool(TANK_SYMBOL not in entities and 
                               HEAL_SYMBOL not in entities)
        return not self._building_alive_check() or mech_dead_check

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
        entity_positions = {entity.get_position(): entity 
                            for entity in self._entities}
        return entity_positions

    def get_valid_movement_positions(
        self, 
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
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
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
            for j in range(-abs(entity.get_speed()-abs(i)), 
                           abs(entity.get_speed()-abs(i))+1):
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
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
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
        if (entity.is_friendly() and entity.is_active() and 
            position in self.get_valid_movement_positions(entity)):
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

    def _separate_mech_and_enemies(self) -> tuple[list[Mech], list[Enemy]]:
        """Gets a list of the mech and enemies from the list of entities.

        Returns:
            A tuple containing 2 lists. The first list contains all of the 
                living mechs, while the second list contains all of 
                the living enemies.

        >>>board = Board([[' ', ' ', '4', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),1,1,1), TankMech((1,3),5,1,1), 
            Scopion((0,1),1,1,1), Firefly((0, 3),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model._separate_mech_and_enemies()
        ([TankMech((0,1),1,1,1), TankMech((1,3),5,1,1)], 
            [Scopion((0,1),1,1,1), Firefly((0, 3),1,1,1)])
        """
        mechs = [entity for entity in self._entities if (entity.is_friendly()
                 and entity.is_alive())]
        enemies = [entity for entity in self._entities 
                   if not entity.is_friendly() and entity.is_alive()]
        return mechs, enemies
        
    def assign_objectives(self) -> None:
        """Updates the objectives of all enemies based on the current 
            game state.

        >>>board = Board([[' ', ' ', '4', ' ',], [' ', '2', ' ', ' ',]])
        >>>entities = [TankMech((0,0),1,1,1), TankMech((1,3),5,1,1), 
            Scopion((0,1),1,1,1), Firefly((0, 3),1,1,1)]
        >>>model = BreachModel(board, entities)
        >>>model.assign_objectives()
        >>>scorpion = model.entity_positions()[(0,1)]
        >>>scorpion.get_objective()
        (1, 3)
        >>>firefly = model.entity_positions()[(0,3)]
        >>>firefly.get_objective()
        (0, 2)
        """
        mechs, enemies = self._separate_mech_and_enemies()
        for enemy in enemies:
            enemy.update_objective(mechs, self._board.get_buildings())

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
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
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
        self.assign_objectives()
        mechs, enemies = self._separate_mech_and_enemies()
        enemies_need_to_move = enemies.copy()
        prev_enemies = enemies.copy()
        for enemy in enemies:
            target = enemy.get_objective()
            distance = None
            possible_moves = self.get_valid_movement_positions(enemy)
            best_move = None
            for possible_move in possible_moves:
                distance_check = get_distance(self, target, possible_move)
                if ((distance == None or distance > distance_check) and 
                    distance_check > 0):
                    distance = distance_check
                    best_move = possible_move

                elif distance == distance_check:
                    if (possible_move[0] > best_move[0] or 
                        possible_move[0] == best_move[0] and 
                        possible_move[1] > best_move[1]):
                        distance = distance_check
                        best_move = possible_move

                
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
        entity_positions = self.entity_positions()
        buildings = self._board.get_buildings()
        targets = entity.get_targets()
        #Attack entities
        for target in targets:
            if target in entity_positions and entity.is_alive():
                entity.attack(entity_positions[target])
        #Update the list of entities after attacking
        entities = [entity_positions[entity_position] 
                    for entity_position in entity_positions 
                    if entity_positions[entity_position].is_alive()]
        self._entities = entities
        #Attack buildings
        for target in targets:
            if target in buildings and entity.is_alive():
                buildings[target].damage(entity.get_strength())

    def end_turn(self) -> None:
        """Executes the attack and enemy movement phases, then sets all mechs 
            to be active.

        >>>board = Board([['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'], 
            ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', ' ', ' '
            , ' ',' ', '3', ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', '3', 'M'
            , ' ', ' ', ' ', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
            , 'M'], ['M', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M'], ['M', 
            '2', ' ', ' ', ' ', 'M', 'M', 'M', 'M', 'M'], ['M', '2', ' ', ' ', 
            ' ', ' ', ' ', 'M', 'M', 'M'], ['M', ' ', ' ', ' ', ' ', ' ', ' ', 
            ' ', ' ', 'M'], ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
            ])
        >>>entities = [TankMech((1, 1), 5, 3, 3), TankMech((1, 2), 3, 3, 3), 
            HealMech((1, 3), 2, 3, 2), Scorpion((8, 8), 3, 3, 2), 
            Firefly((8, 7), 2, 2, 1), Firefly((7, 6), 1, 1, 1)]
        >>>model = BreachModel(board, entities)
        >>>model.entity_positions()
        {(1, 1): TankMech((1, 1), 5, 3, 3), (1, 2): TankMech((1, 2), 3, 3, 3), 
            (1, 3): HealMech((1, 3), 2, 3, 2),(8, 8): Scorpion((8, 8), 3, 3, 2)
            ,(8, 7): Firefly((8, 7), 2, 2, 1),(7, 6): Firefly((7, 6), 1, 1, 1)}
        >>>model.end_turn()
        >>>model.entity_positions()
        {(1, 1): TankMech((1, 1), 5, 3, 3), (8, 5): Scorpion((8, 5), 3, 3, 2), 
            (7, 5): Firefly((7, 5), 1, 1, 1)}
        """
        entities = self.get_entities()
        for entity in entities:
            self.make_attack(entity)
        mechs, enemies = self._separate_mech_and_enemies()
        self.move_enemies()
        for mech in mechs:
            mech.enable()
        self._is_move_made = False

###############################################################################
##################################### View ####################################
###############################################################################

class GameGrid(AbstractGrid):
    """The class that creates the object for the grid that the game will be 
        played on. The grid will have squares of a certain colour, denoting 
        what type of tile it is, with entities overlayed on top of them.

    Inherits:
        tk.Canvas
        AbstractGrid
    """

    _TILE_TO_COLOUR = {MOUNTAIN_SYMBOL: MOUNTAIN_COLOR, 
                       GROUND_SYMBOL: GROUND_COLOR}
    _ENTITY_TO_DISPLAY = {TANK_SYMBOL: TANK_DISPLAY, 
                          HEAL_SYMBOL: HEAL_DISPLAY,
                          SCORPION_SYMBOL: SCORPION_DISPLAY, 
                          FIREFLY_SYMBOL: FIREFLY_DISPLAY}

    def _draw_tile(self, board: Board, position: tuple[int, int]) -> None:
        """Draws the display colour for the tile from the board on the grid in 
            the given position.
        
        Arguments:
            board: The board of the current game state.
            position: The position of the tile in the grid.
        """
        if str(board.get_tile(position)).isdigit():
            if board.get_tile(position).is_destroyed():
                self.color_cell(position, DESTROYED_COLOR)
            else:
                self.color_cell(position, BUILDING_COLOR)
        else:
            self.color_cell(position, self._TILE_TO_COLOUR[
                str(board.get_tile(position))])

    def _draw_entity(self, entity: Entity, position: tuple[int, int]) -> None:
        """Draws the display symbol for the entity from the entity's object on 
            the grid in the given position.

        Arguments:
            entity: The entity that needs to be dsiplayed in the GameGrid.
            position: The position of the entity in the grid.
        """
        self.annotate_position(position, 
                               self._ENTITY_TO_DISPLAY[entity.get_symbol()],
                               font=ENTITY_FONT)

    def redraw(
        self,
        board: Board, 
        entities: list[Entity], 
        highlighted: list[tuple[int, int]] = None, 
        movement: bool = False
    ) -> None:
        """Clears the game grid, then redraws it according to the provided 
            information. The grid is drawn on the GameGrid instance itself. 
            Destroyed buildings are colored diferently from buildings that are 
            not destroyed. If a list of highlighted cells are provided, then 
            the color of those cells are overridden to be one of two highlight 
            colors based on if movement is True or False. If highlighted is 
            None, then the movement parameter is ignored. The health of each 
            non-destroyed building is annotated as well as any entity. All 
            annotations are located in the centre of their cell.

        Arguments:
            board: The current model's board object, used to draw all 
                tiles in the grid, as well as any building health values.
            entities: A list of the current entities in play from the 
                model. These entities will be drawn on to the grid.
            highlighted: The positions where the grid should be 
                highlighted, coloured and positioned depending on the 
                state of movement, as well as the stats of the entity. 
                None by default.
            movement: Whether or not the focudes entity has moved of not, 
                which determines the highlighted positions as well as the 
                colour of the highlighting. False by default.
        """
        self.set_dimensions(board.get_dimensions())
        self._cell_size = self._get_cell_size()
        self._entity_positions = {entity.get_position(): entity 
                                  for entity in entities}
        self.clear()
        self.pack(side=tk.LEFT, anchor=tk.N)
        for row in range(board.get_dimensions()[0]):
            for column in range(board.get_dimensions()[1]):
                position = (row, column)
                #Check for highlighted tiles
                if position in highlighted:
                    if movement:
                        self.color_cell(position, MOVE_COLOR)
                    else:
                        self.color_cell(position, ATTACK_COLOR)
                else:
                    self._draw_tile(board, position)
                #Need to check for building again so annotation can be outside 
                #   the last if statement and be drawn along with highlighted 
                #   squares.
                if (str(board.get_tile(position)).isdigit() and 
                    not board.get_tile(position).is_destroyed()):
                    self.annotate_position(position, 
                                           str(board.get_tile(position)),
                                           font=ENTITY_FONT)
                        
                #Check for entities
                if position in self._entity_positions:
                    entity = self._entity_positions[position]
                    self._draw_entity(entity, position)
                
    def bind_click_callback(
        self, 
        click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """Binds the <Button-1> and <Button-2> events on itself to a function 
            that calls the provided click handler at the correct position. 
            These callbacks exits in the controller. The only path this 
            function handles is the input and converting the pixel position of 
            the mouse to a grid position.

        Arguments:
            click_callback: The click handler function that is within the 
                controller. This function will set the focussed entity as well 
                as set the highlighted grid spaces.
        """
        position_action = (lambda event, call_back=click_callback: 
            call_back(self.pixel_to_cell(event.x, event.y)))
        self.bind('<Button-1>', position_action)
        self.bind('<Button-2>', position_action)


class SideBar(AbstractGrid):
    """The class that creates the object for the section of the screen on the 
        right, where all of the statistics of each living entity is displayed. 
        The spacing of the information will be dynamic depending on how many 
        entities are currently alive. There are 4 columns, for the entity's 
        symbol, its position, its health and its strength respectively.

    Inherits:
        tk.Canvas
        AbstractGrid
    """

    _ENTITY_TO_DISPLAY = {TANK_SYMBOL: TANK_DISPLAY, 
                          HEAL_SYMBOL: HEAL_DISPLAY, 
                          SCORPION_SYMBOL: SCORPION_DISPLAY, 
                          FIREFLY_SYMBOL: FIREFLY_DISPLAY}
    
    def _get_entity_display(self, entity: Entity) -> str:
        """Gets the display symbol for the entity from the entity's object.

        Arguments:
            entity: The entity that needs to be dsiplayed in the SideBar.
        Returns:
            The entity's display symbol.
        """
        return self._ENTITY_TO_DISPLAY[entity.get_symbol()]

    def display(self, entities: list[Entity]) -> None:
        """Clears the side bar, then redraws the header followed by the 
            relevant properties of the given entities on the SideBar instance 
            itself. Each entity in the given list should receive a row on the 
            side bar containing the entity's display symbol, their position, 
            their health, and their strength. Entities appear in descending 
            priority order, with the highest priority entity appearing at the 
            top of the sidebar, and the lowest priority entity appearing at 
            the bottom of the sidebar.

        Arguments:
            entities: The list of entities that are currently alive that need 
                their statistics displayed.
        Preconditions:
            The given list of entities will be sorted in descending priority 
                order.
        """
        self.pack(side=tk.RIGHT, anchor=tk.N)
        self.set_dimensions((len(entities)+1, 4))
        self.clear()
        display = None
        for column, heading in enumerate(SIDEBAR_HEADINGS):
            self.annotate_position((0, column), heading, font=SIDEBAR_FONT)
        for row, entity in enumerate(entities):
            display = self._get_entity_display(entity)
            self.annotate_position((row+1, 0), display, font=SIDEBAR_FONT)
            position = entity.get_position()
            display_position = f'({position[0]}, {position[1]})'
            self.annotate_position((row+1, 1), 
                                    display_position, 
                                    font=SIDEBAR_FONT)
            self.annotate_position((row+1, 2), 
                                    entity.get_health(), 
                                    font=SIDEBAR_FONT)
            self.annotate_position((row+1, 3), 
                                    entity.get_strength(), 
                                    font=SIDEBAR_FONT)


class ControlBar(tk.Frame):
    """The class that creates the control bar object. This object will be on 
        the bottom of the screen and only contains three buttons, which are 
        'Save Game', 'Load Game', and 'End Turn' from left to right. Each 
        button calls to a corresponding method in the controller class.

    Inherits:
        tk.Frame
    """

    def __init__(
        self, 
        master: tk.Widget, 
        save_callback: Optional[Callable[[], None]] = None, 
        load_callback: Optional[Callable[[], None]] = None, 
        turn_callback: Optional[Callable[[], None]] = None, 
        **kwargs
    ) -> None:
        """Instantiates a ControlBar as a special kind of frame with the 
            desired button layout. Each button will call one of the three 
            functions given in the parameters.

        Arguments: 
            save_callback: A method from the controller class that will save 
                the current state of the game's board and entities to a file 
                to be loaded later.
            load_callback: A method from the controller class that will load a 
                previously saved state of the game's board and entities, 
                overwriting the current state of the game.
            turn_callback: A method from the controller class that will run 
                the end turn method from the model section, allowing the 
                attacks to take place, as well as enemy movement. 
        """
        super().__init__(master, height=CONTROL_BAR_HEIGHT)
        self._save_callback = save_callback
        self._load_callback = load_callback
        self._turn_callback = turn_callback
        self.pack(side=tk.BOTTOM, fill=tk.X)
        button_texts = [SAVE_TEXT, LOAD_TEXT, TURN_TEXT]
        button_commands = [save_callback, load_callback, turn_callback]
        for text, command in zip(button_texts, button_commands):
            button = tk.Button(self, text=text, command=command)
            button.pack(side=tk.LEFT, expand=tk.TRUE)


class BreachView():
    """The class that creates the breach view object. This object provides a 
        wrapper for all of the other GUI elements from the view. The top is 
        the banner with the title of the game. On the left under the banner is 
        the GameGrid, and to it's left is the SideBar. Under those is the 
        ControlBar, which spans the width of the GameGrid and the SideBar put 
        together.
    """

    def __init__(
        self, 
        root: tk.Tk, 
        board_dims: tuple[int, int], 
        save_callback: Optional[Callable[[], None]] = None, 
        load_callback: Optional[Callable[[], None]] = None, 
        turn_callback: Optional[Callable[[], None]] = None, 
    ) -> None:
        """Instantiates view. Sets title of the given root window, and 
            instantiates all child components. The buttons on the instantiated 
            CommandBar receive the given callbacks as their respective 
            commands.

        Arguements:
            root: The root window that holds all of the GUI.
            board_dims: The dimensions of the game's board's grid.
            save_callback: The method that saves the game state to a file.
            load_callback: The method that loads a previously saved game.
            turn_callback: The method that ends the current turn.
        """
        self._root = root
        self._root.title(BANNER_TEXT)
        self._banner = tk.Label(self._root, text=BANNER_TEXT, font=BANNER_FONT)
        self._banner.pack(fill=tk.X)
        self._game_grid = GameGrid(self._root, 
                                   board_dims, 
                                   (GRID_SIZE, GRID_SIZE))
        self._side_bar = SideBar(self._root, 
                                 (0, 0), 
                                 (SIDEBAR_WIDTH, GRID_SIZE))
        self._control_bar = ControlBar(self._root, 
                                       save_callback=save_callback, 
                                       load_callback=load_callback, 
                                       turn_callback=turn_callback)

    def bind_click_callback(
        self, 
        click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """Binds a click event handler to the instantiated GameGrid based on 
            click callback.

        Arguments:
            click_callback: the function that highlights relevant grid squares 
                and moves entities when input is given.
        """
        self._game_grid.bind_click_callback(click_callback)

    def redraw(
        self, 
        board: Board, 
        entities: list[Entity], 
        highlighted: list[tuple[int, int]] = None, 
        movement: bool = False
    ) -> None:
        """Redraws the instantiated GameGrid and SideBar based on the given 
            board, list of entities, and tile highlight information.

        Arguments:
            board: The current board object which reflects the current state 
                of the game's tiles.
            entities: The currently alive list of entities.
            highlighted: The squares that are highlighted as a result of 
                clicking on the grid.
            movement: Whether or not the focussed entity's highlighted squared 
                show where it is moving or show its targets.
        """
        self._game_grid.redraw(board, 
                               entities, 
                               highlighted=highlighted, 
                               movement=movement)
        self._side_bar.display(entities)

###############################################################################
################################## Controller #################################
###############################################################################

class IntoTheBreach():
    """The controller class for the overall game. Responsible for creating and 
        maintaining instances of the model and view classes, event handling, 
        and facilitating communi- cation between the model and view classes."""

    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """Instantiates the controller. Creates instances of BreachModel and 
            BreachView, and redraws display to show the initial game state.

        Arguments:
            root: The main tkinter window the game is running on.
            game_file: The file path for the initial game state that should be 
                loaded when first opening the game.

        Preconditions:
            IO errors will not occur when loading a board from game file 
                during this method.
        """
        self._root = root
        self._view = None
        self.load_model(game_file)
        
    def redraw(self) -> None:
        """Redraws the view based on the state of the model and the current 
            focussed entity.
        """
        self._view.redraw(self._model.get_board(), 
                          self._model.get_entities(), 
                          highlighted=self._highlighted, 
                          movement=self._moving)

    def set_focussed_entity(self, entity: Optional[Entity]) -> None:
        """Sets the given entity to be the one on which to base highlighting. 
            Or clears the focussed entity if None is given.

        Arguments:
            entity: The entity that should be set to the focussed one.
        """
        if entity:
            self._focussed_entity = entity
            self._moving = entity.is_friendly() and entity.is_active()
            if self._moving:
                self._highlighted = (self._model.get_valid_movement_positions(
                    entity))
            else:
                self._highlighted = entity.get_targets()
        else:
            self._focussed_entity = None
            self._highlighted = []

    def make_move(self, position: tuple[int, int]) -> None:
        """Attempts to move the focussed entity to the given position, and 
            then clears the focussed entity.

        Arguments:
            position: The position that the focused entity will move to.
        """
        self._model.attempt_move(self._focussed_entity, position)

    def load_model(self, file_path: str) -> None:
        """Replaces the current game state with a new state based on the 
            provided file. If an IOError occurs when opening the given file, 
            an error messagebox should be displayed to the user explaining the 
            error that occurred, and the game state should not change.

        Arguments: 
            file_path: The path to the file that contains the string 
                representation of the game state that needs to be loaded.
        Preconditions: 
            If the file opens, then it will contain exactly the string 
                representation of a BreachModel.
        """
        try:
            
            if file_path:
                file = open(file_path, 'r')
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
                        raw_stat_data = line[2:].split(',')
                        stats = [
                            (int(raw_stat_data[0]), int(raw_stat_data[1])), 
                            int(raw_stat_data[2]), 
                            int(raw_stat_data[3]), 
                            int(raw_stat_data[4].replace('\n', ''))]
                        if line[0] == TANK_SYMBOL:
                            entities.append(TankMech(stats[0], 
                                                     stats[1], 
                                                     stats[2], 
                                                     stats[3]))
                        elif line[0] == HEAL_SYMBOL:
                            entities.append(HealMech(stats[0], 
                                                     stats[1], 
                                                     stats[2], 
                                                     stats[3]))
                        elif line[0] == SCORPION_SYMBOL:
                            entities.append(Scorpion(stats[0], 
                                                     stats[1], 
                                                     stats[2], 
                                                     stats[3]))
                        elif line[0] == FIREFLY_SYMBOL:
                            entities.append(Firefly(stats[0], 
                                                    stats[1], 
                                                    stats[2], 
                                                    stats[3]))
                file.close()
            
                self._board = Board(board)
                self._entities = entities
                self._model = BreachModel(self._board, self._entities)
                if not self._view:
                    board_dims = self._model.get_board().get_dimensions()
                    self._view = BreachView(self._root, 
                                            board_dims, 
                                            save_callback=self._save_game, 
                                            load_callback=self._load_game, 
                                            turn_callback=self._end_turn)
                self._focussed_entity = 0
                self._highlighted = []
                self._moving = False
                self._view.bind_click_callback(click_callback=
                                               (self._handle_click))
                self.redraw()
                self._current_file_path = file_path
        except IOError as error:
            tk.messagebox.showerror(title=IO_ERROR_TITLE, 
                                    message=f'{IO_ERROR_MESSAGE}{str(error)}')
            self._root.destroy()
            
    def _save_game(self) -> None:
        """If the the user has made no moves since the last time they clicked 
            the end turn button, opens a asksaveasfilename file dialog to ask 
            the user to specify a file, and then saves the current game state 
            to that file. If the user has made at least one move since the 
            last time they clicked the end turn button, shows an error message 
            box explaining to the user that they can only save at the 
            beginning of their turn.

        Preconditions:
            IO errors do not need to be handled within this method.
        """
        if self._model.ready_to_save():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                     initialdir='levels', 
                                                     filetypes=(("text file", 
                                                                 "*.txt"), 
                                                                ("All Files", 
                                                                 "*.*")))
            if file_path:
                save_board = str(self._board)
                save_entities = [str(entity) 
                                 for entity in self._entities 
                                 if entity.is_alive()]
                save_file = open(file_path, 'w')
                save_file.write(f'{save_board}\n')
                for save_entity in save_entities:
                    save_file.write(f'\n{save_entity}')
                save_file.close()
        else:
            tk.messagebox.showerror(title=INVALID_SAVE_TITLE, 
                                    message=INVALID_SAVE_MESSAGE)


    def _load_game(self) -> None:
        """Opens a askopenfilename file dialog to ask the user to specify a 
            file, and then loads in a new game state from that file. If an IO 
            error occurs when loading in a new game state, then a messagebox 
            should be shown to the user explaining the error.
        """
        file_path = filedialog.askopenfilename(initialdir='levels')
        self.load_model(file_path)

    def _end_turn(self) -> None:
        """Executes the attack phase, enemy movement phase, and termination 
            checking. If the player wins or loses, display a messagebox with 
            the relevant message, then give the user an option to play again. 
            If the player chooses to play again, start from the last loaded 
            game state. If the player chooses not to, then exit gracefully.
        """
        self._model.end_turn()
        self._focussed_entity = None
        self._highlighted = []
        self.redraw()
        play_again = self._game_over_box()
        if play_again != None:
            if play_again:
                self.load_model(self._current_file_path)
            else:
                self._root.destroy()

    def _game_over_box(self):
        """If the player wins or loses, display the relevant messagebox with 
            an option to play again or not. Do nothing if the player has not 
            yet won or lost.
        """
        if self._model.has_lost():
            return tk.messagebox.askyesno(title='You Lost!', 
                                          message='You Lost! ' + 
                                                  PLAY_AGAIN_TEXT)
        elif self._model.has_won():
            return tk.messagebox.askyesno(title='You Win!', 
                                          message='You Win! ' +
                                                  PLAY_AGAIN_TEXT)
        else:
            return None

    def _handle_click(self, position: tuple[int, int]) -> None:
        """Handler for a click from the user at the given (row, column) 
            position.

        Arguments:
            position: The position of the grid that the user has clicked on.
        """
        entity_positions = self._model.entity_positions()
        if position in entity_positions:
            self.set_focussed_entity(entity_positions[position])
        else:
            if position in self._highlighted:
                self.make_move(position)
            self.set_focussed_entity(None)
        self.redraw()


def play_game(root: tk.Tk, file_path: str) -> None:
    """The function that runs the game. It should construct the controller 
        instance and ensure the root window stays open listening for events.

    Arguments:
        file_path: The path for the initial game state that will be loaded 
            upon starting the game.
    """
    IntoTheBreach(root, file_path)
    
    root.mainloop()


def main() -> None:
    """The main function. Runs the code. Constructs the root tk.TK instance 
        and calls the play_game function with the initial loaded game state.
    """
    root = tk.Tk()
    play_game(root, 'levels/level1.txt')


if __name__ == "__main__":
    main()


