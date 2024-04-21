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
    """docstring for Tile"""
    def __init__(self) -> None:
        """docstring for __init__ method"""
        pass
    def __repr__(self) -> str:
        """docstring for __repr__ method"""
        pass
    def __str__(self) -> str:
        """docstring for __str__ method"""
        pass
    def get_tile_name(self) -> str:
        """docstring for get_tile_name method"""
        pass
    def is_blocking(self) -> bool:
        """docstring for is_blocking method"""
        pass

class Ground(Tile):
    """docstring for Ground"""
    
class Mountain(Tile):
    """docstring for Mountain"""
   
class Building(Tile):
    """docstring for Building"""
    def __init__(self, initial_health: int) -> None:
        """docstring for __init__ method"""
        pass
    def is_destroyed(self) -> bool:
        """docstring for is destroyed method"""
        pass
    def damage(self, damage: int) -> None:
        """docstring for damage method"""
        pass

class Board():
    """docstring for Board"""
    def __init__(self, board: list[list[str]]) -> None:
        """docstring for __init__ method"""
        pass
    def __repr__(self):
        """docstring for __repr__ method"""
    def __str__(self) -> str:
        """docstring for __str__ method"""
        pass
    def get_dimensions(self) -> tuple[int, int]:
        """docstring for get_dimensions method"""
        pass
    def get_tile(self, position: tuple[int, int]) -> Tile:
        """docstring"""
        pass
    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """docstring"""
        pass

class Entity():
    """docstring for Entity"""
    def __init__(
    self, 
    position: tuple[int, int], 
    initial_health: int, 
    speed: int, 
    strength: int
    ) -> None:
        """docstring"""
        pass
    def __repr__(self) -> str:
        """docstring"""
        pass
    def __str__(self) -> str:
        """docstring"""
        pass
    def get_symbol(self) -> str:
        """docstring"""
        pass
    def get_name(self) -> str:
        """docstring"""
        pass
    def get_position(self) -> tuple[int, int]:
        """docstring"""
        pass
    def set_position(self, position: tuple[int, int]) -> None:
        """docstring"""
        pass
    def get_health(self) -> int:
        """docstring"""
        pass
    def get_speed(self) -> int:
        """docstring"""
        pass
    def get_strength(self) -> int:
        """docstring"""
        pass
    def damage(self, daage: int) -> None:
        """docstring"""
        pass
    def is_alive(self) -> bool:
        """docstring"""
        pass
    def is_friendly(self) -> bool:
        """docstring"""
        pass
    def get_targets(self) -> list[tuple[int, int]]:
        """docstring"""
        pass
    def attack(self, entity: "Entity") -> None:
        """docstring"""
        pass

class Mech(Entity):
    """docstring for Mech"""
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

class FireFly(Enemy):
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
