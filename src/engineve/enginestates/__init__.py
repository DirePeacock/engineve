from .combatstate import CombatState
from .landingstate import LandingState
from .menustate import MenuState

# do this janky thing to try and get around the circular dependencies
CombatState._post_combat_state = MenuState
LandingState._combat_state = CombatState
MenuState._combat_state = CombatState

