from .gamestatemanager import GameStateManager
from .enginecommands.invoker import Invoker
from .gameengine import GameEngine
def factory():
    GAMESTATE = GameStateManager.instantiate()
    INVOKER = Invoker()
    GAMEENGINE = GameEngine(INVOKER, GAMESTATE)
    return GAMEENGINE
