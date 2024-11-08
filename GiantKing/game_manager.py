from enum import Enum


class GameState(Enum):
    MENU = 0
    GAME = 1
    LOSE_SCREEN = 2
    PAUSE = 3
    HOW_TO_PLAY = 4

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value: {value}")

class GameManager:
    _instance = None
    game_state = GameState.MENU
    how_page = 0
    popup = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass