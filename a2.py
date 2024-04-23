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
        for row_i, row in enumerate(self._board):
            self._object_board.append([])
            for j in row:
                if j.isdigit():
                    self._object_board[row_i].append(Building(int(j)))
                else:
                    self._object_board[row_i].append(self._board_object_dictionary[j])
        self._board_repr = f'Board({board})'
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
        for k, i in enumerate(self._board):
            for j in i:
                self._board_str += j
            if k < len(self._board)-1:
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
        """Initialises an object from the entity class as well as all of it's children"""
        self._position = position
        self._health = initial_health
        self._speed = speed
        self._strength = strength
        self._friendly = False
        self._entity_name = ENTITY_NAME
        self._entity_symbol = ENTITY_SYMBOL
        self._entity_repr = f'{ENTITY_NAME}({position}, {initial_health}, {speed}, {strength})'
        self._entity_str = f'{ENTITY_SYMBOL},{self._position[0]},{self._position[1]},{self._health},{speed},{strength}'
    def __repr__(self) -> str:
        """docstring"""
        return self._entity_repr
    def __str__(self) -> str:
        """docstring"""
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
        self._entity_str = f'{ENTITY_SYMBOL}, {self._position[0]}, {self._position[1]} {self._health}, {self._speed}, {self._strength}'
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
        self._health -= damage
        if self.is_alive():
            if self._health < 0:
                self._health = 0
            self._entity_str = f'{ENTITY_SYMBOL}, {self._position[0]}, {self._position[1]} {self._health}, {speed}, {strength}'
    def is_alive(self) -> bool:
        """docstring"""
        return self._health > 0
    def is_friendly(self) -> bool:
        """docstring"""
        return self._friendly
    def get_targets(self) -> list[tuple[int, int]]:
        """docstring"""
        targets = [(self._position[0]-1, self.position[1]), (self._position[0]+1, self.position[1]), (self._position[0], self.position[1]-1), (self._position[0], self.position[1]+1)]
        return targets
    def attack(self, entity: "Entity") -> None:
        """docstring"""
        entity.damage(self._strength)

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
    #super().__init__(self, position, initial_health, speed, strength)

    def enable(self) -> None:
        """docstring"""
        pass
    def disable(self) -> None:
        """docstring"""
        pass
    def is_active(self) -> bool:
        """docstring"""
        pass

class TankMech(Mech):
    """docstring for TankMech"""

class HealMech(Mech):
    """docstring for TankMech"""

class Enemy(Entity):
    """docstring for Enemy"""
    def get_objective(self) -> tuple[int, int]:
        """docstring"""
        pass
    def update_objective(
    self, 
    entities: list[Entity], 
    buildings: dict[tuple[int, int], Building]
    ) -> None:
        """docstring"""
        pass

class Scorpion(Enemy):
    """docstring for Scorpion"""

class Firefly(Enemy):
    """docstring for FireFly"""

class BreachModel():
    """docstring for BreachModel"""
    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """docstring"""
        pass
    def __str__(self) -> str:
        """docstring"""
        pass
    def get_board(self) -> Board:
        """docstring"""
        pass
    def get_entities(self) -> list[Entity]:
        """docstring"""
        pass
    def has_won(self) -> bool:
        """docstring"""
        pass
    def has_lost(self) -> bool:
        """docstring"""
        pass
    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """docstring"""
        pass
    def get_valid_movement_positions(self, 
    entity: Entity
    ) -> list[tuple[int, int]]:
        """docstring"""
        pass
    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """docstring"""
        pass
    def ready_to_save(self) -> bool:
        """docstring"""
        pass
    def assign_objectives(self) -> None:
        """docstring"""
        pass
    def move_enemies(self) -> None:
        """docstring"""
        pass
    def make_attack(self, entity: Entity) -> None:
        """docstring"""
        pass
    def end_turn(self) -> None:
        """docstring"""
        pass


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
        pass
    def bind_click_callback(self, 
    click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """docstring"""
        pass
class SideBar(AbstractGrid):
    """docstring for SideBar"""
    def __init__(self, 
    master: tk.Widget, 
    dimensions: tuple[int, int], 
    size: tuple[int, int]
    ) -> None:
        """docstring"""
        pass
    def display(self, entities: list[Entity]) -> None:
        """docstring"""
        pass

class ControlBar(tk.Frame):
    def __init__(self, 
    master: tk.Widget, 
    save_callback: Optional[Callable[[], None]] = None, 
    load_callback: Optional[Callable[[], None]] = None, 
    turn_callback: Optional[Callable[[], None]] = None, 
    **kwargs
    ) -> None:
        """docstring"""
        pass

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
        pass
    def bind_click_callback(self, 
    click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """docstring"""
        pass
    def redraw(self, 
    board: Board, 
    entites: list[Entity], 
    highlighted: list[tuple[int, int]] = None, 
    movement: bool = False
    ) -> None:
        """docstring"""
        pass





################################## Controller ##################################

class IntoTheBreach():
    """docstring for IntoTheBreach"""
    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """docstring"""
        pass
    def redraw(self) -> None:
        """docstring"""
        pass
    def set_focused_entity(self, entity: Optional[Entity]) -> None:
        """docstring"""
        pass
    def make_move(self, position: tuple[int, int]) -> None:
        """docstring"""
        pass
    def load_model(self, file_path: str) -> None:
        """docstring"""
        pass
    def _save_game(self) -> None:
        """docstring"""
        pass
    def _load_game(self) -> None:
        """docstring"""
        pass
    def _end_turn(self) -> None:
        """docstring"""
        pass
    def _handle_click(self, position: tuple[int, int]) -> None:
        """docstring"""
        pass


def play_game(root: tk.Tk, file_path: str) -> None:
    """The function that runs the game"""
    pass

def main() -> None:
    """The main function"""
    pass

if __name__ == "__main__":
    main()
