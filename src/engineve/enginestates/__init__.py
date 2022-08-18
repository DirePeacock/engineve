from .combatstate import CombatState
from .landingstate import LandingState
from .menustate import MenuState
from .overworldstate import OverworldState

# do this janky thing to try and get around the circular dependencies
CombatState._post_combat_state = OverworldState
LandingState._combat_state = CombatState
MenuState._combat_state = CombatState
MenuState._overworld_state = OverworldState
OverworldState._combat_state = CombatState
