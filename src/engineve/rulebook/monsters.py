monsters = {
    "skeleton": {
        "stats": [8, 14, 10, 10, 8],
        "ac": 15,
        "hp_dice": "2d6",
        "hearts": 2,
        "heart_size": 6,
        "speed": {"land": 6},
        "sprites": {"game_piece": "skeleton64.png"},
        "exp_mod": 0.25,
        "languages": "common",
        "game_moves": {
            "scimitar": {
                "parent_move": "AttackAction",
                "dmg_dice": "1d6",
                "stat": "agi",
                "animtation_frames": 5,
            }
        },
    }
}
