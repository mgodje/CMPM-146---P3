import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

# Attack the weakest enemy planet
# Use in bt_bot: Action(attack_weakest_enemy_planet)
def attack_weakest_enemy_planet(state):
    """
    Attempts to attack the weakest enemy planet using the strongest of the bot's planets.
    Sends half the ships from the strongest planet to the weakest enemy planet.
    
    :param state: The current state of the game from planet_wars
    :return: Boolean indicating if the order was successfully issued
    """
    if len(state.my_fleets()) > 1:
        return False
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    if not strongest_planet or not weakest_planet:
        return False
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 2)

# Spread to the weakest neutral planet
# Use in bt_bot: Action(spread_to_weakest_neutral_planet)
def spread_to_weakest_neutral_planet(state):
    """
    Attempts to capture the weakest neutral planet using the strongest of the bot's planets.
    Sends half the ships from the strongest planet to the weakest neutral planet.
    
    :param state: The current state of the game from planet_wars
    :return: Boolean indicating if the order was successfully issued
    """
    if len(state.my_fleets()) > 1:
        return False
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet or not weakest_planet:
        return False
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 2)

# Reinforce a planet under threat
# Use in bt_bot: Action(reinforce_planet)
def reinforce_planet(state):
    """
    Reinforces planets under threat by sending ships from the nearest allied planet with a surplus.
    Only reinforces if a planet has less than 20 ships and another planet can spare ships.
    
    :param state: The current state of the game from planet_wars
    :return: Boolean indicating if the reinforcement order was successfully issued
    """
    for planet in state.my_planets():
        if planet.num_ships < 20:
            source_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
            if source_planet and source_planet.ID != planet.ID:
                num_ships_to_send = source_planet.num_ships // 4
                return issue_order(state, source_planet.ID, planet.ID, num_ships_to_send)
    return False

# Attack an enemy planet strategically
# Use in bt_bot: Action(attack_strategically)
def attack_strategically(state):
    """
    Identifies strategic enemy targets based on the enemy fleet size and planet growth rate.
    Attacks an enemy planet chosen based on a heuristic of growth rate and fleet size.
    
    :param state: The current state of the game from planet_wars
    :return: Boolean indicating if the attack order was successfully issued
    """
    target_planet = None
    min_strength_ratio = float('inf')
    for planet in state.enemy_planets():
        strength_ratio = planet.num_ships / (planet.growth_rate + 1)
        if strength_ratio < min_strength_ratio:
            min_strength_ratio = strength_ratio
            target_planet = planet

    if target_planet:
        source_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
        if source_planet and source_planet.num_ships > 50:
            num_ships_to_send = source_planet.num_ships // 2
            return issue_order(state, source_planet.ID, target_planet.ID, num_ships_to_send)
    return False

# Expand to a strategic neutral planet
# Use in bt_bot: Action(expand_to_strategic_neutral)
def expand_to_strategic_neutral(state):
    """
    Expands control to neutral planets based on strategic value such as location and growth rate.
    Chooses the neutral planet with the highest growth rate that can be realistically captured.
    
    :param state: The current state of the game from planet_wars
    :return: Boolean indicating if the expansion order was successfully issued
    """
    target_planet = None
    max_growth_rate = 0
    for planet in state.neutral_planets():
        if planet.growth_rate > max_growth_rate:
            max_growth_rate = planet.growth_rate
            target_planet = planet

    if target_planet:
        source_planet = min((p for p in state.my_planets() if p.num_ships > 20),
                            key=lambda p: state.distance(p.ID, target_planet.ID),
                            default=None)
        if source_planet:
            num_ships_to_send = source_planet.num_ships // 3
            return issue_order(state, source_planet.ID, target_planet.ID, num_ships_to_send)
    return False
