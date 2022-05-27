def get_target(attacker_id, state):
    for key, state_actor in state.actors.items():
        if state_actor.team != state.actors[attacker_id].team:
            return key