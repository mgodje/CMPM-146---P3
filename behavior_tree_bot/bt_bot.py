#!/usr/bin/env python

import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check
from planet_wars import PlanetWars, finish_turn

# Setup the behavior tree
def setup_behavior_tree():
    root = Selector(name='High Level Strategy')

    # Defensive strategy: Reinforce planets under threat
    defensive_plan = Sequence(name='Defensive Strategy')
    threat_check = Check(is_under_threat)
    reinforce_action = Action(reinforce_planet)
    defensive_plan.child_nodes = [threat_check, reinforce_action]

    # Offensive strategy: Attack weakest enemy if we have the largest fleet
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    # Spread strategy: Capture weakest neutral planet if available
    spread_plan = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_plan.child_nodes = [neutral_planet_check, spread_action]

    # Strategic attack: Attack strategically advantageous enemy planet
    strategic_attack_plan = Sequence(name='Strategic Attack Strategy')
    advantage_check = Check(have_advantage)
    strategic_attack_action = Action(attack_strategically)
    strategic_attack_plan.child_nodes = [advantage_check, strategic_attack_action]

    # Expansion strategy: Expand to the most strategic neutral planet
    expansion_plan = Sequence(name='Expansion Strategy')
    beneficial_neutral_check = Check(if_beneficial_neutral_planet_available)
    expand_action = Action(expand_to_strategic_neutral)
    expansion_plan.child_nodes = [beneficial_neutral_check, expand_action]

    # Counter attack strategy: Counter attack when under threat
    counter_attack_plan = Sequence(name='Counter Attack Strategy')
    under_threat_check = Check(is_under_threat)
    counter_action = Action(counter_attack)
    counter_attack_plan.child_nodes = [under_threat_check, counter_action]

    # Reinforce strong planets strategy: Ensure strong planets stay strong
    reinforce_strong_plan = Sequence(name='Reinforce Strong Planets Strategy')
    strong_planet_check = Check(is_strong)
    reinforce_strong_action = Action(reinforce_strong_planets)
    reinforce_strong_plan.child_nodes = [strong_planet_check, reinforce_strong_action]

    # Aggressive expansion strategy: Expand aggressively when we have a significant advantage
    aggressive_expansion_plan = Sequence(name='Aggressive Expansion Strategy')
    enemy_nearby_check = Check(enemy_planet_nearby)
    aggressive_expansion_action = Action(aggressive_expansion)
    aggressive_expansion_plan.child_nodes = [enemy_nearby_check, aggressive_expansion_action]

    # Early aggressive attack strategy
    early_aggressive_plan = Sequence(name='Early Aggressive Attack Strategy')
    early_aggressive_action = Action(early_aggressive_attack)
    early_aggressive_plan.child_nodes = [early_aggressive_action]

    # Focused attack on newly acquired enemy planets strategy
    focused_attack_plan = Sequence(name='Focused Attack Strategy')
    focused_attack_action = Action(focused_attack_on_new_enemy_planets)
    focused_attack_plan.child_nodes = [focused_attack_action]

    root.child_nodes = [
        defensive_plan,
        offensive_plan,
        spread_plan,
        strategic_attack_plan,
        expansion_plan,
        counter_attack_plan,
        reinforce_strong_plan,
        aggressive_expansion_plan,
        early_aggressive_plan,
        focused_attack_plan
    ]

    logging.info('\n' + root.tree_to_string())
    return root

def do_turn(state):
    try:
        behavior_tree.execute(state)
    except Exception as e:
        logging.error(f"Error executing behavior tree: {str(e)}")
        logging.error(traceback.format_exc())

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception as e:
        logging.error(f"Error in main loop: {str(e)}")
        logging.error(traceback.format_exc())
