monsters = {
    "skeleton": {
        "stats": [-1, 2, 0, 0, -1],
        "evasion": 15,
        "hearts": 2,
        "heart_size": 6,
        "speed": {"land": 6},
        "sprites": {"game_piece": "skeleton64.png"},
        "exp_mod": 0.25,
        "languages": "common",
        "game_moves": {
            "scimitar": {
                "parent_move": "AttackAction",
                "dmg_range": (1, 6),
                "stat": "agi",
                "animtation_frames": 5,
            }
        },
    }
}
