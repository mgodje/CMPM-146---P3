def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def is_under_threat(state):
    # Implement a check to see if any planets are under immediate threat

    # go through all my planets
    for planet in state.my_planets():
        # go through all enemy fleets
        for enemy in state.enemy_fleets():
            # if enemy is headed to a planet, check if it's mine
            if enemy.destination_planet == planet.ID:
                # if the enemy has more ships than the planet, return true; else, return false
                if enemy.num_ships > planet.num_ships:
                    return True
                else:
                    return False
    pass

def if_beneficial_neutral_planet_available(state):
    # Implement a check for beneficial neutral planets

    # go through all neutral planets
    for planet in state.neutral_planets():
        # if a planet has over 20 num_ships, it's beneficial
        if planet.num_ships > 20:
            return True
        # if a planet is a short distance away (< 10), it's beneficial
        elif planet.distance(planet, state.my_planets()) < 10: # wanna do distance from my planet to neutral? because it is currently the other way around
            return True
        else:
            return False

def have_advantage(state):
    # Implement a check to determine if attacking now is advantageous

    # go through all my planets
    for planet in state.my_planets():
        # go through all enemy planets
        for enemy_planet in state.enemy_planets():
            # if my planet has more ships than the enemy planet, return true; else, return false
            if planet.num_ships > enemy_planet.num_ships:
                return True
            else:
                return False