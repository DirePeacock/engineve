from .gamemoves.attackaction import AttackAction

move_type_map = {"AttackAction": AttackAction}
# for movetype in [AttackAction]:
#     move_type_map[type(movetype).__name__] = movetype


# dmg_dice, dmg_flat, to_hit,
def load_game_move(parent_move, *args, **kwargs):
    new_move = move_type_map[parent_move](*args, **kwargs)
    return new_move
