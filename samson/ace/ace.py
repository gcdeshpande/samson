from samson.utilities.runtime import RUNTIME
from samson.ace.constraints import IdentityConstraint
from samson.ace.consequence import Consequence
from samson.ace.exploit import IdentityExploit
from samson.ace.state import State
from enum import Enum

import logging
log = logging.getLogger(__name__)


class Requirement(Enum):
    EVENTUALLY_DECRYPTS = 0



def get_runtime_exploits(primitive):
    all_exploits = []
    for cls in [primitive] + [_ for _ in primitive.__bases__]:
        if cls in RUNTIME.exploit_mappings:
            attack  = RUNTIME.exploit_mappings[cls]
            exploit = RUNTIME.exploits[attack]
            all_exploits.append(exploit)

    return all_exploits


def get_runtime_constraints(primitive):
    all_constraints = []
    for cls in [primitive] + [_ for _ in primitive.__bases__]:
        if cls in RUNTIME.constraints:
            constraint  = RUNTIME.constraints[cls]
            all_constraints.append(constraint)

    return all_constraints



class SymEnc(object):
    def __init__(self, alg, mode, key):
        self.alg = alg
        self.mode = mode
        self.key = key


    def __eq__(self, other):
        key = self.key
        if issubclass(type(key), State):
            key = key.exposed_state

        other_key = other.key
        if issubclass(type(other_key), State):
            other_key = other_key.exposed_state

        return (self.alg, self.mode, key) == (other.alg, other.mode, other_key)


    def encrypt(self, state):
        all_constraints = []
        all_exploits = []

        # Get from RUNTIME
        for primitive in [self.alg, self.mode]:
            all_exploits.extend(get_runtime_exploits(primitive))
            all_constraints.extend(get_runtime_constraints(primitive))

        new_state = State(state, self, all_constraints, all_exploits)
        return new_state


    def decrypt(self, state):
        if state.exposed_state.owner == self:
            state.exposed_state.requirements_satisfied.append(Requirement.EVENTUALLY_DECRYPTS)
        else:
            log.warning(f'{self} cannot decrypt state due to not being owner on {state.exposed_state}')

        state.exposed_state = state.exposed_state.child

        return state



class MAC(object):
    def __init__(self, alg, key):
        self.alg = alg
        self.key = key


    def __eq__(self, other):
        key = self.key
        if issubclass(type(key), State):
            key = key.exposed_state

        other_key = other.key
        if issubclass(type(other_key), State):
            other_key = other_key.exposed_state

        return (self.alg, key) == (other.alg, other_key)


    def generate(self, state):
        # Get from RUNTIME
        all_exploits    = get_runtime_exploits(self.alg)
        all_constraints = get_runtime_constraints(self.alg)

        new_state = State(state, self, all_constraints, all_exploits)
        return new_state


    def validate(self, state):
        from samson.ace.constraints import MACConstraint

        current_state = state.exposed_state

        if current_state.owner != self:
            log.warning(f'{self} cannot validate state due to not being owner on {state.exposed_state}. ACE will just pretend they are equivalent.')

        # Propagate the MACConstraint
        while current_state != None:
            current_state.constraints.append(MACConstraint())
            current_state = current_state.child

        state.exposed_state = state.exposed_state.child

        return state



class ACE(object):
    def execute(self, func):
        func(self)


    def goal(self, state, consequence):
        self.final_state = state
        current_state = state

        while current_state.child != None:
            current_state = current_state.child

        # Add an IdentityConstraint to the base state
        constraint = IdentityConstraint()
        constraint.needed_consequence = consequence
        current_state.constraints.append(constraint)

        self.goal_consequence = consequence



    @RUNTIME.report
    def solve(self):
        current_state = self.final_state
        exploit_chain = []

        while current_state != None:
            has_exploit   = False
            return_to_top = False
            constraint    = None

            for exploit in current_state.exploits:
                return_to_top = False

                # See if there are any outstanding constraints that we can solve
                while True:
                    needed_consequences = [other_constraint.needed_consequence for other_constraint in current_state.constraints if other_constraint.prevents_consequence in exploit.requirements and not other_constraint.needed_consequence in current_state.requirements_satisfied]
                    if needed_consequences:

                        # So far, we only know how to solve KEY_RECOVERY
                        # TODO: If we solve this, why not just early exit?
                        if needed_consequences[0] == Consequence.KEY_RECOVERY:
                            log.debug('Cannot continue without key. Attempting key recovery.')
                            new_solver = ACE()

                            original_key = current_state.owner.key
                            while original_key.parent:
                                original_key = original_key.parent

                            new_solver.goal(original_key, Consequence.PLAINTEXT_RECOVERY)
                            exploit_chain.append(new_solver.solve())
                            current_state.requirements_satisfied.append(Consequence.KEY_RECOVERY)

                            # Let's restart
                            current_state = self.final_state
                            return_to_top = True
                            break
                    else:
                        break

                if return_to_top:
                    log.debug('Returning to top')
                    break


                # Check to make sure we satisfy requirements

                # Exploit suitability logic:
                # 1.a) The exploit directly fulfills the breaking consequence for the constraint
                # OR
                # 1.b) The exploit is not prevented by the constraint AND there does not exist a constraint that prevents any of the exploits requirements
                # 2  ) The exploit's consequence is not prevented by any other constraint
                # 3  ) This is not the goal consequence
                if all([requirement in current_state.requirements_satisfied for requirement in exploit.requirements]) and not needed_consequences:
                    for constraint in current_state.constraints:

                        # See if the attack will work
                        if (exploit.consequence == constraint.needed_consequence \
                                or (exploit.consequence != constraint.prevents_consequence)) \
                            and not any([constraint.needed_consequence == other_constraint.prevents_consequence for other_constraint in current_state.constraints if other_constraint != constraint]) \
                            and not (current_state.child is None and exploit.consequence != self.goal_consequence):

                            log.debug(f'{constraint.needed_consequence} reachable with {exploit}')
                            has_exploit = True
                            break
                else:
                    # For debugging purposes
                    constraint = None

                # Break out of exploit loop if we're already satisfied
                if has_exploit:
                    break

            # Did we find _any_ exploits for this state?
            if not return_to_top:
                if has_exploit:
                    current_state = current_state.child
                    exploit_chain.append(exploit)
                else:
                    raise Exception(f'No suitable exploit found. Last consequence not fulfilled: {constraint.needed_consequence if constraint else "None (no constraint evaluated due to requirements)"}')


        exploit_chain = [exploit for exploit in exploit_chain if not issubclass(type(exploit), IdentityExploit)]
        return exploit_chain
