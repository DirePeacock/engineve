import logging
from .factory import factory


def do_main():
    client = factory()
    client.main()

def COMMANDMAIN():
    do_main()

# def GAMESTATEMAIN():
#     GAME_STATE = GameStateManager.instantiate()
#     for actor_id in CombatActorIter([id for id in GAME_STATE.actors.keys()]):
#         GAME_STATE.actors[actor_id].hp -= 1
#         print(f"{GAME_STATE.actors[actor_id].name}@{GAME_STATE.actors[actor_id].hp}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    COMMANDMAIN()