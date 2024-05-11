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
    """Tile Class"""
    def __init__(self) -> None:
        """Initialises the attributes of the base tile class' objects"""
        self._tile_repr = f'{TILE_NAME}()'
        self._tile_str = TILE_SYMBOL
        self._tile_name = TILE_NAME
        self._can_block = False
    def __repr__(self) -> str:
        """Returns a machine readable string that could be used to construct an identical instance of the tile.

        >>>tile = Tile()
        >>>tile
        Tile()

        >>>mountain = Mountain()
        >>>mountain
        Mountain()
        """
        return self._tile_repr
    def __str__(self) -> str:
        """Returns the character representing the type of the tile.

        >>>tile = Tile()
        >>>str(tile)
        'T'

        >>>ground = Ground()
        >>>str(ground)
        ' '
        """
        return self._tile_str
    def get_tile_name(self) -> str:
        """Returns the name of the type of the tile.

        >>>tile = Tile()
        >>>tile.get_tile_name()
        'Tile'

        >>>mountain = Mountain()
        >>>mountain.get_tile_name()
        'Mountain'
        """
        return self._tile_name
    def is_blocking(self) -> bool:
        """Returns True only when the tile is blocking.

        >>>tile = Tile()
        >>>tile.is_blocking()
        False

        >>>building = Building(5)
        >>>building.is_blocking()
        True
        """
        return self._can_block

class Ground(Tile):
    """Ground Class"""
    def __init__(self) -> None:
        """Initialises the attributes for a ground object"""
        self._tile_repr = f'{GROUND_NAME}()'
        self._tile_str = GROUND_SYMBOL
        self._tile_name = GROUND_NAME
        self._can_block = False

class Mountain(Tile):
    """Mountain Class"""
    def __init__(self) -> None:
        """Initialises the attributes for a Mountain object"""
        self._tile_repr = f'{MOUNTAIN_NAME}()'
        self._tile_str = MOUNTAIN_SYMBOL
        self._tile_name = MOUNTAIN_NAME
        self._can_block = True
   
class Building(Tile):
    """Building Class"""
    def __init__(self, initial_health: int) -> None:
        """Initialises the attributes for a Building object

        Arguments: 
            The building's initial health when the game starts.
        """
        self._tile_repr = f'{BUILDING_NAME}({initial_health})'
        self._tile_name = BUILDING_NAME
        self._health = initial_health
        self._can_block = self._health > 1 #can block if not destroyed
        self._tile_str = str(self._health)
    def is_destroyed(self) -> bool:
        """Returns True only when the building is destroyed, and False if not.

        >>>building = Building(5)
        >>>building.is_destroyed()
        False

        >>>building = Building(0)
        >>>building.is_destroyed()
        True
        """
        self._can_block = self._health > 1 
        return self._health < 1 #building is destroyed when health is below 1
    def damage(self, damage: int) -> None:
        """Reduces the health of the building by the amount specified. Do nothing is the building is already destroyed.

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
        self._tile_str = str(self._health)
        self._tile_repr = f'{BUILDING_NAME}({self._health})'

class Board():
    """Board Class"""
    def __init__(self, board: list[list[str]]) -> None:
        """Initialises the attributes for a Board object
        
        Arguments:
            The board state through a 2d list with strings.
        Preconditions:
            Each row on the board will have the same length.
            Board array will have at least one row.
            Each character on the board will be a string representation provided by the previous classes.
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
    def __repr__(self):
        """Returns a machine readable string that could be used to construct an identical instance of the board.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board
        Board([[' ', '4'], ['6', 'M']])
        """
        return self._board_repr
    def __str__(self) -> str:
        """Returns a string representation of the board.
        
        Returns:
            The board, with a new line when the next row on the board is reached.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>str(board)
        ' 4\n6M'
        """
        self._board_str = ""
        #FIX BAD ITERATOR VARIABLE NAMES
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
        """Returns the (#rows, #columns) dimensions of the board.
        Preconditions:
            Each row on the board will have the same length.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board.get_dimensions()
        (2, 2)
        """
        return len(self._board), len(self._board[0])
    def get_tile(self, position: tuple[int, int]) -> Tile:
        """Returns the Tile instance located at the given position.
        Arguments:
            The position of the desired tile in a tuple: (row, column).
        Preconditions:
            The provided position will not be out of bounds.

        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board.get_tile((0, 1))
        Building(4)
        """
        
        return self._object_board[position[0]][position[1]]
    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """Returns a dictionary mapping the positions of buildings to the building instances at those positions.
        
        >>>tiles = [[" ", "4"], ["6", "M"]]
        >>>board = Board(tiles)
        >>>board.get_buildings()
        {(0, 1): Building(4), (1, 0): Building(6)}
        """
        self._building_dictionary = dict()
        for row_i, row in enumerate(self._board):
            for column_i, column in enumerate(row):
                if column.isdigit():
                    self._building_dictionary[(row_i, column_i)] = self.get_tile((row_i, column_i))
        return self._building_dictionary

class Entity():
    """Entity Class"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """Initialises an object from the entity class as well as all of it's children
        Arguments:
            position: a tuple with 2 ints that determines the starting row and column of the entity.
            initial_health: the starting health of the entity.
            speed: NEED TO DO THIS PART!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            strength: the damage or healing power of the entity

        """
        self._position = position
        self._health = initial_health
        self._speed = speed
        self._strength = strength
        self._friendly = False
        self._entity_name = ENTITY_NAME
        self._entity_symbol = ENTITY_SYMBOL
        #REPEATED CODE, FIX THIS
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        print(self._position)
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
    def __repr__(self) -> str:
        """Returns a machine readable string that could be used to construct an identical instance of the entity.
        
        >>>e1 = Entity((0,0),1,1,1)
        >>>e1
        Entity((0, 0), 1, 1, 1)
        """
        return self._entity_repr
    def __str__(self) -> str:
        """Returns the string representation of the entity, with all of its attributes.
        
        >>>e1 = Entity((0,0),1,1,1)
        >>>str(e1)
        'E,0,0,1,1,1'
        """
        return self._entity_str
    def get_symbol(self) -> str:
        """docstring"""
        return self._entity_symbol
    def get_name(self) -> str:
        """docstring"""
        return self._entity_name
    def get_position(self) -> tuple[int, int]:
        """docstring"""
        return self._position
    def set_position(self, position: tuple[int, int]) -> None:
        """docstring"""
        self._position = position
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._entity_repr = f'{self._entity_name}({position}, {self._health}, {self._speed}, {self._strength})'
    def get_health(self) -> int:
        """docstring"""
        return self._health
    def get_speed(self) -> int:
        """docstring"""
        return self._speed
    def get_strength(self) -> int:
        """docstring"""
        return self._strength
    def damage(self, damage: int) -> None:
        """docstring"""
        if self.is_alive():
            self._health -= damage
            if self._health < 0:
                self._health = 0
            elif self._health > 9:
                self._health = 9
            self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
            self._entity_repr = f'{self._entity_name}({self._position}, {self._health}, {self._speed}, {self._strength})'
    def is_alive(self) -> bool:
        """docstring"""
        return self._health > 0
    def is_friendly(self) -> bool:
        """docstring"""
        return self._friendly
    def get_targets(self) -> list[tuple[int, int]]:
        """docstring"""
        targets = [(self._position[0]-1, self._position[1]), (self._position[0]+1, self._position[1]), (self._position[0], self._position[1]-1), (self._position[0], self._position[1]+1)] #This sucks but I'll fix it later
        return targets
    def attack(self, entity: "Entity") -> None:
        """docstring"""
        if self.get_strength() < 0 and not entity.is_friendly(): #MIGHT BE A BETTER WAY OF DOING THIS (maybe self.get_strength() > 0 or entity.is_friendly(): leads to damage???)
            return
        entity.damage(self.get_strength())

class Mech(Entity):
    """docstring for Mech"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        super().__init__(position, initial_health, speed, strength)
        self._friendly = True
        self._entity_name = MECH_NAME
        self._entity_symbol = MECH_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True

    def enable(self) -> None:
        """docstring"""
        self._active_state = True
    def disable(self) -> None:
        """docstring"""
        self._active_state = False
    def is_active(self) -> bool:
        """docstring"""
        return self._active_state

class TankMech(Mech):
    """docstring for TankMech"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        super().__init__(position, initial_health, speed, strength) # there is probably a better way of doing the below lines, but hell if I know right now
        self._entity_name = TANK_NAME
        self._entity_symbol = TANK_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
    def get_targets(self) -> list[tuple[int, int]]: #might be able to do this better. maybe remove this func and make Mech's GT work for all.
        """docstring"""
        targets = [(self._position[0], self._position[1]+tile_index) for tile_index in range(-5, 6) if tile_index != 0] #Source: w3schools
        return targets

class HealMech(Mech):
    """docstring for TankMech"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = HEAL_NAME
        self._entity_symbol = HEAL_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
    def get_strength(self) -> int:
        """docstring"""
        return -self._strength


class Enemy(Entity):
    """docstring for Enemy"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        super().__init__(position, initial_health, speed, strength)
        self._friendly = False
        self._entity_name = ENEMY_NAME
        self._entity_symbol = ENEMY_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True
        self._objective = self._position

    def get_objective(self) -> tuple[int, int]:
        """docstring"""
        return self._objective
    def update_objective(
    self, 
    entities: list[Entity], 
    buildings: dict[tuple[int, int], Building]
    ) -> None:
        """docstring"""
        self._objective = self._position

class Scorpion(Enemy):
    """docstring for Scorpion"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = SCORPION_NAME
        self._entity_symbol = SCORPION_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True
    def get_targets(self) -> list[tuple[int, int]]:
        """doctring"""
        targets1 = [(self._position[0], self._position[1]+tile_index) for tile_index in range(-2, 3) if tile_index != 0]
        targets2 = [(self._position[0]+tile_index, self._position[1]) for tile_index in range(-2, 3) if tile_index != 0]
        return targets1 + targets2 #think of better names or improves otherwise
        
    def update_objective(
    self, 
    entities: list[Entity], 
    buildings: dict[tuple[int, int], Building]
    ) -> None:
        """docstring"""
        #could do whole function in 1 line, but would probably be unreadable
        possible_objective_healths = [entity.get_health() for entity in entities if entity.is_friendly()]
        self._objective = entities[possible_objective_healths.index(max(possible_objective_healths))].get_position() #gets the index of the highest priority entity with the most health and and sets objective to its position

class Firefly(Enemy):
    """docstring for FireFly"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        super().__init__(position, initial_health, speed, strength)
        self._entity_name = FIREFLY_NAME
        self._entity_symbol = FIREFLY_SYMBOL
        self._entity_repr = f'{self._entity_name}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{self._entity_symbol},{self._position[0]},{self._position[1]},{self._health},{self._speed},{self._strength}'
        self._active_state = True
    def get_targets(self) -> list[tuple[int, int]]:
        """doctring"""
        targets = [(self._position[0]+tile_index, self._position[1]) for tile_index in range(-5, 6) if tile_index != 0]
        return targets
    def update_objective(
    self, 
    entities: list[Entity], 
    buildings: dict[tuple[int, int], Building]
    ) -> None:
        """docstring"""
        #could do whole function in 1 line, but would probably be unreadable
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
class BreachModel():
    """docstring for BreachModel"""
    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """docstring"""
        self._board = board
        self._entities = entities
        self._is_move_made = False
    #def update_building(self, board: Board, building: ) -> None:
     #   """docstring"""

    def __str__(self) -> str:
        """docstring"""
        string_representation = f'{str(self._board)}\n'
        for entity in self._entities:
            string_representation += "\n"
            string_representation += str(entity)
        return string_representation
    def get_board(self) -> Board:
        """docstring"""
        return self._board
    def get_entities(self) -> list[Entity]:
        """docstring"""
        return self._entities
    def has_won(self) -> bool:
        """docstring"""
        building_dict = [self.get_board().get_buildings()[building_position] for building_position in self.get_board().get_buildings() if not self.get_board().get_buildings()[building_position].is_destroyed()]
        building_check = bool(len(building_dict) > 0)
        entity_list = [str(entity)[0] for entity in self._entities if entity.is_alive()]
        mech_alive_check = bool(TANK_SYMBOL in entity_list or HEAL_SYMBOL in entity_list)
        enemy_dead_check = bool(SCORPION_SYMBOL not in entity_list and FIREFLY_SYMBOL not in entity_list)
        return building_check and mech_alive_check and enemy_dead_check
    def has_lost(self) -> bool:
        """docstring"""
        #REPEATED CODE, NEED TO FIX
        building_dict = [self._board.get_buildings()[building_position] for building_position in self._board.get_buildings() if not self._board.get_buildings()[building_position].is_destroyed()]
        building_check = bool(len(building_dict) == 0)
        entity_list = [str(entity)[0] for entity in self._entities if entity.is_alive()]
        mech_dead_check = bool(TANK_SYMBOL not in entity_list and HEAL_SYMBOL not in entity_list)
        print(entity_list)
        return building_check or mech_dead_check
    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """docstring"""
        # entity_position = {}
        # for entity in entities:
        #     entity_position[entity.get_position()] = entity
        entity_position_dict = {entity.get_position(): entity for entity in self._entities}
        return entity_position_dict
    def get_valid_movement_positions(self, 
    entity: Entity
    ) -> list[tuple[int, int]]:
        """docstring"""
        possible_moves = []
        pos = entity.get_position() #pos stands for the position of the mech
        for i in range(-entity.get_speed(), entity.get_speed()+1):
            for j in range(-abs(entity.get_speed()-abs(i)), abs(entity.get_speed()-abs(i))+1):
                distance = get_distance(self, pos, (pos[0]+i, pos[1]+j))
                if entity.get_speed() >= distance > 0:
                    possible_moves.append((pos[0]+i, pos[1]+j))
        return possible_moves
    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """docstring"""
        if entity.is_friendly() and entity.is_active() and position in self.get_valid_movement_positions(entity):
            entity.set_position(position)
            entity.disable()
            self._is_move_made = True
    def ready_to_save(self) -> bool:
        """docstring"""
        return not self._is_move_made

    def assign_objectives(self) -> None:
        """docstring"""
        mechs = [entity for entity in self._entities if str(entity)[0] in [MECH_SYMBOL, TANK_SYMBOL, HEAL_SYMBOL] and entity.is_alive()]
        buildings = self._board.get_buildings()
        enemies = [entity for entity in self._entities if str(entity)[0] in [ENEMY_SYMBOL, SCORPION_SYMBOL, FIREFLY_SYMBOL] and entity.is_alive()]
        for enemy in enemies:
            enemy.update_objective(mechs, buildings)

    def move_enemies(self) -> None:
        """docstring"""
        #REPEATED CODE, MAKE SURE TO FIX THAT
        self.assign_objectives()
        mechs = [entity for entity in self.get_entities() if str(entity)[0] in [MECH_SYMBOL, TANK_SYMBOL, HEAL_SYMBOL] and entity.is_alive()]
        buildings = self._board.get_buildings()
        enemies = [entity for entity in self.get_entities() if str(entity)[0] in [ENEMY_SYMBOL, SCORPION_SYMBOL, FIREFLY_SYMBOL] and entity.is_alive()]
        enemies_need_to_move = enemies.copy()
        prev_enemies = enemies.copy()
        # print(enemies)
        # while enemies_need_to_move:
        #     # print(enemies_need_to_move)
        #     for enemy in enemies_need_to_move:
        #         # print(enemy)
        #         possible_moves = self.get_valid_movement_positions(enemy)
        #         target = enemy.get_objective()
        #         distance = None
        #         #PROBABLY NOT OPTIMISED AND KIND OF MESSY, TRY TO DO WITH ONE FOR LOOP
        #         for possible_move in possible_moves:
        #             distance_check = get_distance(self, enemy.get_position(), possible_move)
        #             if (distance == None or distance < distance_check) and distance_check > 0:
        #                 distance = distance_check
        #         if distance != None:
        #             for possible_move in possible_moves:
        #                 if get_distance(self, enemy.get_position(), possible_move) == distance:
        #                     enemy.set_position(possible_move)
        #                     enemies_need_to_move.remove(enemy)
        #     # print(enemies_need_to_move)
        #     # print(enemies)
        #     # print(prev_enemies)
        #     # if enemies == prev_enemies:
        #     #     print("TEST")
        #     #     enemies_need_to_move = []
        #     prev_enemies = enemies.copy()



        for enemy in enemies:
            target = enemy.get_objective()
            distance = None
            #PROBABLY NOT OPTIMISED AND KIND OF MESSY, TRY TO DO WITH ONE FOR LOOP
            
            possible_moves = self.get_valid_movement_positions(enemy)
            for possible_move in possible_moves:
                distance_check = get_distance(self, target, possible_move)
                if str(enemy)[0] == 'S':
                    print(f'Scorpion Distance_Check: {distance_check}')
                if (distance == None or distance > distance_check) and distance_check > 0:
                    distance = distance_check
            if distance != None:
                for possible_move in possible_moves:
                    if get_distance(self, target, possible_move) == distance:
                        enemy.set_position(possible_move)
            if str(enemy)[0] == 'S':
                print(f'Scorpion Target: {target}')
                print(f'Scorpion distance to target: {distance}')



    def make_attack(self, entity: Entity) -> None:
        """docstring"""
        #THESE DICTIONARIES ARE REPEATED MULTIPLE TIMES, NEED TO FIX
        entity_dict = {ent.get_position(): ent for ent in self.get_entities() if ent.is_alive()} #ent is entity
        building_dict = self._board.get_buildings()
        targets = entity.get_targets()
        #Attack entities
        for target in targets:
            if target in entity_dict and entity.is_alive():
                # print(entity, target)
                entity.attack(entity_dict[target])
        entity_list = [entity_dict[entity_position] for entity_position in entity_dict if entity_dict[entity_position].is_alive()]
        # print(entity_list)
        self._entities = entity_list
        #Attack buildings
        for target in targets:
            if target in building_dict and entity.is_alive():
                building_dict[target].damage(entity.get_strength())

    def end_turn(self) -> None:
        """docstring"""
        #REPEATED LIST CREATION, NEED TO FIX
        entities = self.get_entities()
        for entity in entities:
            self.make_attack(entity)
        print(self.entity_positions())
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
                    if str(self._entity_dict[(row, column)])[0] == TANK_SYMBOL:
                        self.annotate_position((row, column), TANK_DISPLAY, font=ENTITY_FONT)
                    elif str(self._entity_dict[(row, column)])[0] == HEAL_SYMBOL:
                        self.annotate_position((row, column), HEAL_DISPLAY, font=ENTITY_FONT)
                    elif str(self._entity_dict[(row, column)])[0] == SCORPION_SYMBOL:
                        self.annotate_position((row, column), SCORPION_DISPLAY, font=ENTITY_FONT)
                    elif str(self._entity_dict[(row, column)])[0] == FIREFLY_SYMBOL:
                        self.annotate_position((row, column), FIREFLY_DISPLAY, font=ENTITY_FONT)
                
    def bind_click_callback(self, 
    click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """docstring"""
        position_action = lambda event, call_back=click_callback: call_back(self.pixel_to_cell(event.x, event.y))
        self.bind('<Button-1>', position_action)
        self.bind('<Button-2>', click_callback)



    #THIS FUNCTION IS FOR TESTING, REMOVE LATER
    def _mouse_position_to_entity(self, position: tuple[int, int]) -> Optional[Entity]:
        """docstring"""
        if position in self._entity_dict:
            return self._entity_dict[position]


    def _get_mouse_coord(self, event, pos):
        """docstring"""
        #REMOVE PRINT
        x, y = pos(event)
        grid_position = self.pixel_to_cell(x, y)
        print(grid_position)
        entity = self._mouse_position_to_entity(grid_position)
        print(entity)
        return entity


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
            if str(entity)[0] == TANK_SYMBOL:
                display = TANK_DISPLAY
            elif str(entity)[0] == HEAL_SYMBOL:
                display = HEAL_DISPLAY
            elif str(entity)[0] == SCORPION_SYMBOL:
                display = SCORPION_DISPLAY
            elif str(entity)[0] == FIREFLY_SYMBOL:
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
        self.pack(side=tk.BOTTOM)
        # self.rowconfigure(1, weight=1)
        # self.columnconfigure(1, weight=1)
        padding = (GRID_SIZE+SIDEBAR_WIDTH)/7 #THIS IS WRONG METHOD OF DOING THIS, FIX
        self.grid_columnconfigure((0,1,2), weight=1, uniform="column", pad=padding)
        button_texts = [SAVE_TEXT, LOAD_TEXT, TURN_TEXT]
        button_commands = [save_callback, load_callback, turn_callback]
        # for text, command in zip(button_texts, button_commands):
        #     button = tk.Button(self, text=text, command=command)
        #     button.pack(side=tk.LEFT, expand=tk.TRUE, padx=padding) #PADDING IS INCORRECT I THINK
        # button = tk.Button(self, text=TURN_TEXT, command=turn_callback)
        # button.pack(side=tk.LEFT, expand=tk.TRUE)
        self._buttons = [tk.Button(self, text=button[0], command=button[1]) for button in zip(button_texts, button_commands)]
        for i, button in enumerate(self._buttons):
            button.grid(column=i, row=0)



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
        self._root = root
        self._root.title(BANNER_TEXT)
        self._root.geometry(f'{GRID_SIZE+SIDEBAR_WIDTH}x{GRID_SIZE+BANNER_HEIGHT+CONTROL_BAR_HEIGHT}')
        #root.geometry('750x625')
        banner = tk.Label(self._root, text=BANNER_TEXT, font=BANNER_FONT)
        banner.pack(fill=tk.X)
        self._game_grid = GameGrid(self._root, board_dims, (GRID_SIZE, GRID_SIZE))

        self._side_bar = SideBar(self._root, (7, 4), (SIDEBAR_WIDTH, GRID_SIZE))#2ND ARG SHOULD BE AMOUNT OF ENTITIES+1 instead of 7
        self._control_bar = ControlBar(self._root, save_callback, load_callback, turn_callback)
    def bind_click_callback(self, 
    click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """docstring"""
        self._game_grid.bind_click_callback(click_callback) #CHANGE CALLABLE FUNCTION
    def redraw(self, 
    board: Board, 
    entities: list[Entity], 
    highlighted: list[tuple[int, int]] = None, 
    movement: bool = False
    ) -> None:
        """docstring"""
        self._game_grid.redraw(board, entities, highlighted=highlighted, movement=movement)
        self._side_bar.display(entities)





################################## Controller ##################################

class IntoTheBreach():
    """docstring for IntoTheBreach"""
    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """docstring"""


        self._root = root
        self.load_model(game_file)
        
        
        

    def redraw(self) -> None:
        """docstring"""
        #print('---------------------------------------------------------------')
        print(self._model.get_board())
        self._view.redraw(self._model.get_board(), self._model.get_entities(), highlighted=self._highlighted, movement=self._moving)
        print("TEST")
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
        self._current_file_path = file_path
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

                    #stats = [(int(line[2]), int(line[4])), int(line[6]), int(line[8]), int(line[10])]
                    #THIS IS REPEATED IN __INIT__, SO MAKE A HELPER FUNCTION
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
            self._view = BreachView(self._root, self._board.get_dimensions(), save_callback=self._save_game, load_callback=self._load_game, turn_callback=self._end_turn)
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




        #USED FOR TESTING, REMOVE LATER
        # self._model.get_board().get_buildings()[(2, 5)].damage(1)
        # print(self._model.get_board().get_buildings()[(2, 5)])
        # print(self._model._board)
        # #print(self._model.get_board())
        # self.redraw()


    def _load_game(self) -> None:
        """docstring"""
        file_path = filedialog.askopenfilename(initialdir='')
        #dir_files = 
        self.load_model(file_path)
        print('---------------------------------------------------------------')
        print(self._model.get_board())
        print(self._model.get_entities())
        print('---------------------------------------------------------------')
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
    #LOAD GAME AS WELL AS PLAY AGAIN NOT REDRAWING
    #LOAD I/O ERROR STUFF
    #CONTROL BAR WIDGET WIDTH IS 657 WHEN IT SHOULD BE 750
    #ENEMIES ATTACKING THROUGH WALLS? ALLOWED OR NOT?