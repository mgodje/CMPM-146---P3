#!/usr/bin/env python

def if_neutral_planet_available(state):
    """
    Checks if any neutral planets are available for capture.
    :param state: The current game state
    :return: Boolean indicating if any neutral planets are available
    """
    return any(state.neutral_planets())

def have_largest_fleet(state):
    """
    Determines if the player's fleet is the largest compared to the enemy.
    :param state: The current game state
    :return: Boolean indicating if the player has the largest fleet
    """
    my_ships = sum(planet.num_ships for planet in state.my_planets()) + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_ships = sum(planet.num_ships for planet in state.enemy_planets()) + sum(fleet.num_ships for fleet in state.enemy_fleets())
    return my_ships > enemy_ships

def is_under_threat(state):
    """
    Evaluates if any of the player's planets are under immediate threat from enemy fleets.
    :param state: The current game state
    :return: Boolean indicating if any planet is under threat
    """
    for planet in state.my_planets():
        for enemy_fleet in state.enemy_fleets():
            if enemy_fleet.destination_planet == planet.ID and enemy_fleet.num_ships > planet.num_ships:
                return True
    return False

def if_beneficial_neutral_planet_available(state):
    """
    Checks for beneficial neutral planets based on ship count or proximity.
    :param state: The current game state
    :return: Boolean indicating if there is a beneficial neutral planet available
    """
    for planet in state.neutral_planets():
        if planet.num_ships > 20:
            return True
        for my_planet in state.my_planets():
            if state.distance(my_planet.ID, planet.ID) < 10:
                return True
    return False

def have_advantage(state):
    """
    Determines if attacking any enemy planet now is advantageous based on ship count.
    :param state: The current game state
    :return: Boolean indicating if there's an advantage in attacking
    """
    for my_planet in state.my_planets():
        for enemy_planet in state.enemy_planets():
            if my_planet.num_ships > enemy_planet.num_ships:
                return True
    return False

def enemy_planet_nearby(state):
    """
    Checks if there are enemy planets nearby that can be targeted.
    :param state: The current game state
    :return: Boolean indicating if there are nearby enemy planets
    """
    for my_planet in state.my_planets():
        for enemy_planet in state.enemy_planets():
            if state.distance(my_planet.ID, enemy_planet.ID) < 10:
                return True
    return False

def is_strong(state):
    """
    Determines if the player's strongest planet has a significant number of ships.
    :param state: The current game state
    :return: Boolean indicating if the strongest planet has many ships
    """
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    return strongest_planet and strongest_planet.num_ships > 50
