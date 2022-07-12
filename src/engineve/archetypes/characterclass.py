from ..gametypes.actor import Actor
import logging
from ..tags import check_tags
# to gametypes
class Effect():
    '''
    i know what to do whan an applicable thing happens to me on the stack
    - probably exists in some kind of list based on the character effect
    - this 

    - how would an something like hold person or a DoT like poison work?
    - needs to be able to cross reference tags and state
    - might need to be an observer some times - some sort of thing that happens every time a targets turn starts/ends 
    '''
    def __init__(self, value_func, applicable_func, duration=0,  *args, **kwargs):
        self.duration_turns = None
        self.value_func = value_func
        self.applicable_func = applicable_func
    
    def is_applicable(self, tags):
        return self.applicable_func(tags)
    
    def get_value(self, tags=None):
        # rename to modifiers?
        return self.value_func(tags)

EFFECTS = {}

# class DuelingFightingStlye(Effect):
#     '''
#     can add something like a game_move or a persistant effect to a character
#     '''

class Feature():
    '''
    can add something like a game_move or a persistant effect to a character
    '''
    def __init__(self, name, source=None, text=None, effects=None, game_moves=None, changes=None):
        self.name = name
        
        self.source = '' if source is None else source
        # 'idk flavor text'
        self.text = '' if text is None else text
        # persistent effects applying to the character
        self.effects = {} if effects is None else effects
        # new game moves open to the AI
        self.game_moves = {} if game_moves is None else game_moves
        # immediate changes, like added proficencies
        self.changes = {} if changes is None else changes

    def apply(self, actor_id, state, invoker):
        self.apply_effects(actor_id, state, invoker)
        self.apply_game_moves(actor_id, state, invoker)
        self.apply_changes(actor_id, state, invoker)
    
    def apply_effects(self, actor_id, state, invoker):
        #TODO check for dupes or something probly
        # maybe track things by sources or count how many sources are giving them to you
        for name, effect in self.effects.items():
            state.actors[actor_id].effects[name] = EFFECTS[name]
    
    def apply_game_moves(self, actor_id, state, invoker):
        for game_move in self.game_moves:
            pass
    
    def apply_changes(self, actor_id, state, invoker):
        for change in self.changes:
            pass


fighting_style_dueling = Effect(value_func=(lambda x: 2),
                                applicable_func=(lambda tags: (check_tags(tags, 'one_handed') and not check_tags(tags, 'dual_wielding'))),
                                duration=0)


class CharacterClass():
    '''
        I should be able to decorate actor objects to increase their stuff
        I can be inherited from through subclasses
        knows what kind of hero to make
    '''
    def __init__(self, hit_dice_size=8, *args, **kwargs):
        self.hit_dice_size = hit_dice_size
        fighting_style = Feature(name='fighting_style',
                                 source='fighter_1',
                                 effects={'dueling_fighting_style': fighting_style_dueling})
        self.features = {1: [fighting_style]}  # ['fighting_style', 'fighter_proficiencies', 'fighter_saving_throws']}

    def load_feature(self, feature, level):
        pass
        # self.features = 
    
    def add_level_to_actor(self, actor_id, level, state, invoker):
        if level not in self.features.keys():
            return
        for feature in self.features[level]:
            state.actors[actor_id].effects[feature.name] = feature


class ClassActor(Actor):
    '''
    what all needs to go into this
    '''
    @property
    def class_levels(self):
        return self._class_levels
    
    @class_levels.setter
    def class_levels(self, levels_dict):
        self._class_levels = levels_dict


Fighter = CharacterClass(hit_dice_size=10)
# Q where do i define effects
# A in their own library if they are ubiquitous enough

# Q where do I define features
# A near the class probably

def new_player_character(*args, **kwargs):
    pass