def get_target(attacker_id, state):
    for key, state_actor in state.actors.items():
        if state_actor.team != state.actors[attacker_id].team:
            return key


def is_actor_alive(actor_id, state):
    return not state.actors[actor_id].is_dead()


def get_enemy_ids(actor_id, state):
    return [key for key, state_actor in state.actors.items() if state_actor.team != state.actors[actor_id].team]
