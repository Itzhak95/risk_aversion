import math
from scipy.optimize import fsolve

epsilon = 10 ** -9
decimals = 3

# INPUTS

# Specify bid discretisation

d = 1

# Specify risk aversion parameter

a = 1

# EQUILIBRIUM CONSTRUCTION

# Specify the value space

values = list(range(101))

# Let's define a function which gives the difference in payoffs between jumping to a new bid and sticking with the old one

def payoff_diff(new_jump, old_jump, new_bid):
    return ((math.floor(new_jump) - new_bid)**a)*(1 + new_jump/101) - ((math.floor(new_jump) - new_bid + d)**a) * (1 + old_jump/101)

# We can now compute the next jump as a function of the previous one j (and the bid)

def next_jump(old_jump, new_bid):
    # Let's evaluate the payoff difference at every integer.
    integer_evaluations = [payoff_diff(new_jump, old_jump, new_bid) for new_jump in values]
    # Let's check if we can see a solution immediately.
    for element in integer_evaluations:
        if abs(element - 0) <= epsilon and integer_evaluations.index(element) > math.floor(old_jump) and integer_evaluations.index(element) <= 100:
            return integer_evaluations.index(element)
    # Let's find the largest integer v that leads to a negative payoff difference:
    negative_evaluations = [integer_evaluations[value] for value in values if value <= math.floor(old_jump) or integer_evaluations[value] < 0]
    v = len(negative_evaluations) - 1
    # Now we check whether there is a non-integer solution:
    def h(j):
        return ((v - new_bid)**a) * (1 + j/101) - ((v - new_bid + d)**a) * (1 + old_jump/101)
    candidate_sol = float(fsolve(h, v))
    if abs(payoff_diff(candidate_sol, old_jump, new_bid)) <= epsilon and candidate_sol < 101:
        return candidate_sol
    else:
        if v + 1 <= 100:
            return v + 1

# Now let's compute the jump vector iteratively

jump_vector = []
j = 0
new_bid = d
while True:
    jump_vector.append(j)
    if next_jump(j, new_bid) is None:
        break
    else:
        j = next_jump(j, new_bid)
        new_bid += d

print(f'The jump vector is \n {jump_vector}')
