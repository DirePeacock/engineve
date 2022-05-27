from .combatstate import CombatState
from .landingstate import LandingState

# do this kinda jank thing to try and get around the circular dependencies
CombatState._post_combat_state = LandingState
LandingState._combat_state = CombatState

