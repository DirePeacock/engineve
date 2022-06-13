# VeGameEngine

## This Game Engine Shall have the Following Capabilities
* observable state and changes via command & observer SW patterns
* pause-able & variable speed main loop 
* state of engine and game can be saved/loaded
* game rules like in the 5e SRD can be defined and loaded from json/yaml
* character sheets allow for decoration of actors with class levels
* black formatted
* runs headless
* observer hooks for a hypothetical Graphics Engine
* "runs fast"
* "good unit test coverage"
* "design is understandable to a junior dev & has pictures"
* "well documented"
* "modern CI/CD"

* bonus: undo-able command effects
* bonus: statistics collection
* bonus: machine learning
* bonus: Graphics engine has a way for graphics data to be associated with a game object?
* bonus: bonus: MULTIPLAYER???




## NEEDS 4 GAME DEMO
integrate into thing
    actor observer
    command tags
premade_statblock
load game
save game
bruh unit tests

## REFACTORS
notifications, what needs to be in the notification thing
complex meta info on observables
animation lock integration
gridmap & locs
state passing vs state/engine reference


## todos
actual pathfinding, maybe refactor
Crits and resistances
where should command log strs be created?

where does the weighing of game moves happen
    basicai.weighmoveoptions()
    GameMove.GetTargetWeights()
    
how does a game_cmd reduce_resource
game_clock_tick thing
complete observer tests

game state generation
abstract: load obj from dict
abstract: dump obj to dict

game moves
actor.take_turn

test reaction stack ordering