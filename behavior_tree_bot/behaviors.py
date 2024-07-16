#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

# Attack the weakest enemy planet
def attack_weakest_enemy_planet(state):
    if len(state.my_fleets()) > 1:
        return False
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    if not strongest_planet or not weakest_planet:
        return False
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 2)

# Spread to the weakest neutral planet
def spread_to_weakest_neutral_planet(state):
    if len(state.my_fleets()) > 1:
        return False
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet or not weakest_planet:
        return False
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 2)

# Reinforce a planet under threat
def reinforce_planet(state):
    for planet in state.my_planets():
        if planet.num_ships < 20:
            source_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
            if source_planet and source_planet.ID != planet.ID:
                num_ships_to_send = source_planet.num_ships // 4
                return issue_order(state, source_planet.ID, planet.ID, num_ships_to_send)
    return False

# Attack an enemy planet strategically
def attack_strategically(state):
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
def expand_to_strategic_neutral(state):
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

# Counter attack when under threat
def counter_attack(state):
    for planet in state.my_planets():
        for enemy_fleet in state.enemy_fleets():
            if enemy_fleet.destination_planet == planet.ID and enemy_fleet.num_ships > planet.num_ships:
                source_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
                if source_planet and source_planet.ID != planet.ID:
                    num_ships_to_send = source_planet.num_ships // 2
                    return issue_order(state, source_planet.ID, enemy_fleet.source_planet, num_ships_to_send)
    return False

# Reinforce strong planets
def reinforce_strong_planets(state):
    strong_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if strong_planet and strong_planet.num_ships < 100:
        source_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)
        if source_planet and source_planet.ID != strong_planet.ID:
            num_ships_to_send = source_planet.num_ships // 4
            return issue_order(state, source_planet.ID, strong_planet.ID, num_ships_to_send)
    return False

# Aggressive expansion
def aggressive_expansion(state):
    if len(state.my_fleets()) > 3:
        return False
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet:
        return False
    for planet in state.not_my_planets():
        if planet.num_ships < strongest_planet.num_ships:
            return issue_order(state, strongest_planet.ID, planet.ID, strongest_planet.num_ships // 2)
    return False

# Early aggressive attack
def early_aggressive_attack(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.not_my_planets(), key=lambda p: p.num_ships, default=None)
    if strongest_planet and weakest_planet:
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 3)
    return False

# Focused attack on newly acquired enemy planets
def focused_attack_on_new_enemy_planets(state):
    newly_acquired_planet = min(
        (planet for planet in state.enemy_planets() if planet.turns_owned < 5),
        key=lambda p: p.num_ships,
        default=None
    )
    if newly_acquired_planet:
        source_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
        if source_planet:
            num_ships_to_send = source_planet.num_ships // 2
            return issue_order(state, source_planet.ID, newly_acquired_planet.ID, num_ships_to_send)
    return False
