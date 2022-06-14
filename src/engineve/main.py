import logging
import time
from .mainfactory import factory

def main(debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    engine = factory(spawn=True)
    test_frames = 300
    i = 0
    while i < test_frames:  # and engine.game_state.combat.winning_team is None:
        engine.periodic()
        i+=1
    # engine.periodic()
    
    for line in engine.game_state.log.history:
        print(line)
    
    # for aid in engine.game_state.combat.order.values():
    #     hp = engine.game_state.actors[aid].hp
    #     name = engine.game_state.actors[aid].name
    #     team = engine.game_state.actors[aid].team
    #     print(f"[{team}] hp = {hp} {name}")
    print(f"completed in {i} frames")
    
if __name__ == "__main__":
    main(debug=False)
    # main(debug=False)