import logging

from ..basecommands.compositecommand import CompositeCommand
from ..effectcommands.modifyresources import ModifyResources
from .attackrollcommand import AttackRollCommand
from .damagerollcommand import DamageRollCommand


class AttackCommand(CompositeCommand):
    def __init__(self, attacker_id, target_id, log=None, *args, **kwargs):
        """make attackRoll and damage roll command children"""
        super().__init__(*args, **kwargs)
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.children["attack_roll"] = AttackRollCommand(self.attacker_id, self.target_id)
        self.children["damage_roll"] = DamageRollCommand(self.attacker_id, self.target_id)
        self.log = "" if log is None else log
        self.add_tag("log")
        # self.add_tag("actor_ids", {"attacker_id": self.attacker_id, "target_id": self.target_id})
        self.add_tag("attacker_id", self.attacker_id)
        self.add_tag("attack")
        self.add_tag("target_id", self.target_id)
        # self.resources= [] if resources is None else ModifyResources(actor_id=attacker_id, changes={'turn_action': -1})

    def evaluate(self, state, invoker=None):
        # TODO resistance may want to change the log somewhere
        # TODO crits, crit tags
        self.evaluated = True

        self.children["attack_roll"].evaluate(state, invoker)

        attack_hits = self.children["attack_roll"].value
        if attack_hits:
            self.add_tag("hit")

            self.children["damage_roll"].evaluate(state, invoker)
            # name attacks tgt_name
            self.log = f"{state.actors[self.attacker_id].name}@{state.actors[self.attacker_id].loc} hits {state.actors[self.target_id].name}@{state.actors[self.target_id].loc} {self.children['attack_roll'].log} for {self.children['damage_roll'].log}"
        else:
            self.log = f"{state.actors[self.attacker_id].name}@{state.actors[self.attacker_id].loc} misses {state.actors[self.target_id].name}@{state.actors[self.target_id].loc} {self.children['attack_roll'].log}"

    # def apply_effects(self, state):
    #     super().apply_effects(state)
    # for resource in self.resources:
    #     self.effects.append(resource)
