"""
This file contains code for the game "Gemini CLI Tactics".
Author: GlobalCreativeApkDev
"""

# Game version: 1


# Importing necessary libraries


import sys
import time
import uuid
import pickle
import copy
import google.generativeai as gemini
import random
from datetime import datetime
import os
from dotenv import load_dotenv
from functools import reduce

from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True


# Creating static variables to be used throughout the game.


LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
ELEMENT_CHART: list = [
    ["ATTACKING\nELEMENT", "TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
     "PURE",
     "LEGEND", "PRIMAL", "WIND"],
    ["DOUBLE\nDAMAGE", "ELECTRIC\nDARK", "NATURE\nICE", "FLAME\nWAR", "SEA\nLIGHT", "SEA\nMETAL", "NATURE\nWAR",
     "TERRA\nICE", "METAL\nLIGHT", "ELECTRIC\nDARK", "TERRA\nFLAME", "LEGEND", "PRIMAL", "PURE", "WIND"],
    ["HALF\nDAMAGE", "METAL\nWAR", "SEA\nWAR", "NATURE\nELECTRIC", "FLAME\nICE", "TERRA\nLIGHT", "FLAME\nMETAL",
     "ELECTRIC\nDARK", "TERRA", "NATURE", "SEA\nICE", "PRIMAL", "PURE", "LEGEND", "N/A"],
    ["NORMAL\nDAMAGE", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER",
     "OTHER",
     "OTHER", "OTHER", "OTHER"]
]


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def list_to_string(a_list: list) -> str:
    res: str = "["  # initial value
    for i in range(len(a_list)):
        if i == len(a_list) - 1:
            res += str(a_list[i])
        else:
            res += str(a_list[i]) + ", "

    return res + "]"


def tabulate_element_chart() -> str:
    return str(tabulate(ELEMENT_CHART, headers='firstrow', tablefmt='fancy_grid'))


def generate_random_name() -> str:
    res: str = ""  # initial value
    name_length: int = random.randint(3, 25)
    for i in range(name_length):
        res += LETTERS[random.randint(0, len(LETTERS) - 1)]

    return res.capitalize()


def generate_random_legendary_creature(element):
    # type: (str) -> LegendaryCreature
    name: str = generate_random_name()
    # TODO: implement function


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


def get_elemental_damage_multiplier(element1: str, element2: str) -> mpf:
    if element1 == "TERRA":
        return mpf("2") if element2 in ["ELECTRIC, DARK"] else mpf("0.5") if element2 in ["METAL", "WAR"] else mpf("1")
    elif element1 == "FLAME":
        return mpf("2") if element2 in ["NATURE", "ICE"] else mpf("0.5") if element2 in ["SEA", "WAR"] else mpf("1")
    elif element1 == "SEA":
        return mpf("2") if element2 in ["FLAME", "WAR"] else mpf("0.5") if element2 in ["NATURE", "ELECTRIC"] else \
            mpf("1")
    elif element1 == "NATURE":
        return mpf("2") if element2 in ["SEA", "LIGHT"] else mpf("0.5") if element2 in ["FLAME", "ICE"] else mpf("1")
    elif element1 == "ELECTRIC":
        return mpf("2") if element2 in ["SEA", "METAL"] else mpf("0.5") if element2 in ["TERRA", "LIGHT"] else mpf("1")
    elif element1 == "ICE":
        return mpf("2") if element2 in ["NATURE", "WAR"] else mpf("0.5") if element2 in ["FLAME", "METAL"] else mpf("1")
    elif element1 == "METAL":
        return mpf("2") if element2 in ["TERRA", "ICE"] else mpf("0.5") if element2 in ["ELECTRIC", "DARK"] else \
            mpf("1")
    elif element1 == "DARK":
        return mpf("2") if element2 in ["METAL", "LIGHT"] else mpf("0.5") if element2 == "TERRA" else mpf("1")
    elif element1 == "LIGHT":
        return mpf("2") if element2 in ["ELECTRIC", "DARK"] else mpf("0.5") if element2 == "NATURE" else mpf("1")
    elif element1 == "WAR":
        return mpf("2") if element2 in ["TERRA", "FLAME"] else mpf("0.5") if element2 in ["SEA", "ICE"] else mpf("1")
    elif element1 == "PURE":
        return mpf("2") if element2 == "LEGEND" else mpf("0.5") if element2 == "PRIMAL" else mpf("1")
    elif element1 == "LEGEND":
        return mpf("2") if element2 == "PRIMAL" else mpf("0.5") if element2 == "PURE" else mpf("1")
    elif element1 == "PRIMAL":
        return mpf("2") if element2 == "PURE" else mpf("0.5") if element2 == "LEGEND" else mpf("1")
    elif element1 == "WIND":
        return mpf("2") if element2 == "WIND" else mpf("1")
    else:
        return mpf("1")


def resistance_accuracy_rule(accuracy: mpf, resistance: mpf) -> mpf:
    if resistance - accuracy <= mpf("0.15"):
        return mpf("0.15")
    else:
        return resistance - accuracy


def load_game_data(file_name):
    # type: (str) -> SavedGameData
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (SavedGameData, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes.


###########################################
# ADVENTURE MODE
###########################################


class Action:
    """
    This class contains attributes of an action which can take place during battles.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]

    # TODO: implement methods

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class AwakenBonus:
    """
    This class contains attributes of the bonus gained for awakening a legendary creature.
    """

    # TODO: implement methods in this class


class Battle:
    """
    This class contains attributes of a battle which takes place in this game.
    """

    def __init__(self, team1, team2):
        # type: (Team, Team) -> None
        self.team1: Team = team1
        self.team2: Team = team2
        self.reward: Reward

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Battle
        return copy.deepcopy(self)


class BattleArea:
    """
    This class contains attributes of areas used for single player battles.
    """

    def __init__(self, name, levels, clear_reward):
        # type: (str, list, Reward) -> None
        self.name: str = name
        self.__levels: list = levels
        self.clear_reward: Reward = clear_reward

    def get_levels(self):
        # type: () -> list
        return self.__levels

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> BattleArea
        return copy.deepcopy(self)


class MapArea(BattleArea):
    """
    This class contains attributes of a map area in this game.
    """

    POSSIBLE_MODES: list = ["EASY", "NORMAL", "HARD", "HELL"]

    def __init__(self, name, levels, clear_reward, mode):
        # type: (str, list, Reward, str) -> None
        BattleArea.__init__(self, name, levels, clear_reward)
        self.mode: str = mode if mode in self.POSSIBLE_MODES else self.POSSIBLE_MODES[0]


class Dungeon(BattleArea):
    """
    This class contains attributes of a dungeon in this game.
    """

    POSSIBLE_TYPES: list = ["RESOURCE", "ITEM"]

    def __init__(self, name, levels, clear_reward, dungeon_type):
        # type: (str, list, Reward, str) -> None
        BattleArea.__init__(self, name, levels, clear_reward)
        self.dungeon_type: str = dungeon_type if dungeon_type in self.POSSIBLE_TYPES else self.POSSIBLE_TYPES[0]


class Level:
    """
    This class contains attributes of a level where battles take place.
    """

    def __init__(self, name, stages, clear_reward):
        # type: (str, list, Reward) -> None
        self.name: str = name
        self.__stages: list = stages
        self.is_cleared: bool = False
        self.clear_reward: Reward = clear_reward

    def curr_stage(self, stage_number):
        # type: (int) -> Stage or None
        if stage_number < 0 or stage_number >= len(self.__stages):
            return None
        return self.__stages[stage_number]

    def next_stage(self, stage_number):
        # type: (int) -> Stage or None
        if stage_number < -1 or stage_number >= len(self.__stages) - 1:
            return None
        return self.__stages[stage_number + 1]

    def get_stages(self):
        # type: () -> list
        return self.__stages

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Level
        return copy.deepcopy(self)


class Stage:
    """
    This class contains attributes of a stage in a level.
    """

    def __init__(self, enemies_list):
        # type: (list) -> None
        self.__enemies_list: list = enemies_list
        self.is_cleared: bool = False

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_enemies_list(self):
        # type: () -> list
        return self.__enemies_list

    def clone(self):
        # type: () -> Stage
        return copy.deepcopy(self)


###########################################
# ADVENTURE MODE
###########################################


###########################################
# INVENTORY
###########################################


class LegendaryCreatureInventory:
    """
    This class contains attributes of an inventory containing legendary creatures.
    """

    def __init__(self):
        # type: () -> None
        self.__legendary_creatures: list = []  # initial value

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> None
        self.__legendary_creatures.append(legendary_creature)

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

    def clone(self):
        # type: () -> LegendaryCreatureInventory
        return copy.deepcopy(self)


class ItemInventory:
    """
    This class contains attributes of an inventory containing items.
    """

    def __init__(self):
        # type: () -> None
        self.__items: list = []  # initial value

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def add_item(self, item):
        # type: (Item) -> None
        self.__items.append(item)

    def remove_item(self, item):
        # type: (Item) -> bool
        if item in self.__items:
            self.__items.remove(item)
            return True
        return False

    def get_items(self):
        # type: () -> list
        return self.__items

    def clone(self):
        # type: () -> ItemInventory
        return copy.deepcopy(self)


###########################################
# INVENTORY
###########################################


###########################################
# LEGENDARY CREATURE
###########################################


class Team:
    """
    This class contains attributes of a team brought to battles.
    """

    MAX_LEGENDARY_CREATURES: int = 5

    def __init__(self, legendary_creatures=None):
        # type: (list) -> None
        if legendary_creatures is None:
            legendary_creatures = []
        self.__legendary_creatures: list = legendary_creatures if len(legendary_creatures) <= \
                                                                  self.MAX_LEGENDARY_CREATURES else []

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Team
        return copy.deepcopy(self)


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in this game.
    """

    MIN_RATING: int = 1
    MAX_RATING: int = 6
    MIN_CRIT_RATE: mpf = mpf("0.15")
    MIN_CRIT_DAMAGE: mpf = mpf("1.5")
    MIN_RESISTANCE: mpf = mpf("0.15")
    MAX_RESISTANCE: mpf = mpf("1")
    MIN_ACCURACY: mpf = mpf("0")
    MAX_ACCURACY: mpf = mpf("1")
    MIN_ATTACK_GAUGE: mpf = mpf("0")
    FULL_ATTACK_GAUGE: mpf = mpf("1")
    MIN_EXTRA_TURN_CHANCE: mpf = mpf("0")
    MAX_EXTRA_TURN_CHANCE: mpf = mpf("0.5")
    MIN_COUNTERATTACK_CHANCE: mpf = mpf("0")
    MAX_COUNTERATTACK_CHANCE: mpf = mpf("1")
    MIN_REFLECTED_DAMAGE_PERCENTAGE: mpf = mpf("0")
    MIN_LIFE_DRAIN_PERCENTAGE: mpf = mpf("0")
    MIN_CRIT_RESIST: mpf = mpf("0")
    MAX_CRIT_RESIST: mpf = mpf("1")
    MIN_BENEFICIAL_EFFECTS: int = 0
    MAX_BENEFICIAL_EFFECTS: int = 10
    MIN_HARMFUL_EFFECTS: int = 0
    MAX_HARMFUL_EFFECTS: int = 10
    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]
    DEFAULT_MAX_HP_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_MAX_MAGIC_POINTS_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_ATTACK_POWER_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_ATTACK_SPEED_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_DEFENSE_PERCENTAGE_UP: mpf = mpf("0")
    DEFAULT_CRIT_DAMAGE_UP: mpf = mpf("0")

    def __init__(self, name, element, rating, max_hp, max_magic_points, attack_power, defense, attack_speed,
                 skills, awaken_bonus):
        # type: (str, str, int, mpf, mpf, mpf, mpf, mpf, list, AwakenBonus) -> None
        self.legendary_creature_id: str = str(uuid.uuid1())  # generating random legendary creature ID
        self.name: str = name
        self.element: str = element if element in self.POTENTIAL_ELEMENTS else self.POTENTIAL_ELEMENTS[0]
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else self.MIN_RATING
        self.level: int = 1  # initial value
        self.max_level: int = 10 * triangular(self.rating) if self.rating < self.MAX_RATING else float('inf')
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.curr_hp: mpf = max_hp
        self.max_hp: mpf = max_hp
        self.curr_magic_points: mpf = max_magic_points
        self.max_magic_points: mpf = max_magic_points
        self.attack_power: mpf = attack_power
        self.defense: mpf = defense
        self.attack_speed: mpf = attack_speed
        self.__skills: list = skills
        self.awaken_bonus: AwakenBonus = awaken_bonus

    def get_skills(self):
        # type: () -> list
        return self.__skills

    # TODO: implement methods

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> LegendaryCreature
        return copy.deepcopy(self)


class Skill:
    """
    This class contains attributes of a skill legendary creatures have.
    """

    def __init__(self, name, description, magic_points_cost):
        # type: (str, str, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.magic_points_cost: mpf = magic_points_cost
        self.level: int = 1
        self.is_active: bool = True

    def level_up(self):
        # type: () -> None
        pass

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> LegendaryCreature
        return copy.deepcopy(self)


class BeneficialEffect:
    """
    This class contains attributes of a beneficial effect a legendary creature has.
    """


class HarmfulEffect:
    """
    This class contains attributes of a harmful effect a legendary creature has.
    """


###########################################
# LEGENDARY CREATURE
###########################################


###########################################
# ITEM
###########################################


class Item:
    """
    This class contains attributes of an item in this game.
    """

    def __init__(self, name, description, gold_cost, gem_cost):
        # type: (str, str, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.gold_cost: mpf = gold_cost
        self.gem_cost: mpf = gem_cost
        self.sell_gold_gain: mpf = gold_cost / 5
        self.sell_gem_gain: mpf = gem_cost / 5

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"
    def clone(self):
        # type: () -> Item
        return copy.deepcopy(self)


class Rune(Item):
    """
    This class contains attributes of a rune used to strengthen legendary creatures.
    """

    MIN_SLOT_NUMBER: int = 1
    MAX_SLOT_NUMBER: int = 6
    MIN_RATING: int = 1
    MAX_RATING: int = 6
    MAX_CRIT_RATE_UP: mpf = mpf("0.85")


class AwakenShard(Item):
    """
    This class contains attributes of an awaken shard to immediately awaken a legendary creature.
    """


class EXPShard(Item):
    """
    This class contains attributes of an EXP shard to increase the EXP of a legendary creature.
    """


class LevelUpShard(Item):
    """
    This class contains attributes of a shard used to immediately level up a legendary creature.
    """


class SkillLevelUpShard(Item):
    """
    This class contains attributes of a skill level up shard to immediately increase the level of a
    skill possessed by a legendary creature.
    """


###########################################
# ITEM
###########################################


###########################################
# PLAYER
###########################################


class Player:
    """
    This class contains attributes of a player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(uuid.uuid1())
        self.name: str = name
        self.level: int = 1
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.gold: mpf = mpf("5e6")
        self.gems: mpf = mpf("100")

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class PlayerBase:
    """
    This class contains attributes of the player's base.
    """


class Island:
    """
    This class contains attributes of an island in a player's base.
    """


class IslandTile:
    """
    This class contains attributes of a tile on an island.
    """


class Building:
    """
    This class contains attributes of a building to be built on an island tile.
    """


###########################################
# PLAYER
###########################################


###########################################
# GENERAL
###########################################


class ItemShop:
    """
    This class contains attributes of a shop selling items.
    """

    def __init__(self, items_sold):
        # type: (list) -> None
        self.name: str = "ITEM SHOP"
        self.__items_sold: list = items_sold

    def get_items_sold(self):
        # type: () -> list
        return self.__items_sold

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> ItemShop
        return copy.deepcopy(self)


class BuildingShop:
    """
    This class contains attributes of a shop selling buildings.
    """

    def __init__(self, buildings_sold):
        # type: (list) -> None
        self.name: str = "BUILDING SHOP"
        self.__buildings_sold: list = buildings_sold

    def get_buildings_sold(self):
        # type: () -> list
        return self.__buildings_sold

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> BuildingShop
        return copy.deepcopy(self)


class Reward:
    """
    This class contains attributes of a reward for accomplishing something in this game.
    """

    def __init__(self, player_reward_exp=mpf("0"), player_reward_gold=mpf("0"), player_reward_gems=mpf("0"),
                 legendary_creature_reward_exp=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf) -> None
        self.player_reward_exp: mpf = player_reward_exp
        self.player_reward_gold: mpf = player_reward_gold
        self.player_reward_gems: mpf = player_reward_gems
        self.legendary_creature_reward_exp: mpf = legendary_creature_reward_exp

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Reward
        return copy.deepcopy(self)


class SavedGameData:
    """
    This class contains attributes of the saved game data in this game.
    """

    def __init__(self, trainer_name, temperature, top_p, top_k, max_output_tokens, player_data):
        # type: (str, float, float, float, int, Trainer) -> None
        self.trainer_name: str = trainer_name
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.top_k: float = top_k
        self.max_output_tokens: int = max_output_tokens
        self.player_data: Player = player_data

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += str(self.trainer_name).upper() + "\n"
        res += "Temperature: " + str(self.temperature) + "\n"
        res += "Top P: " + str(self.top_p) + "\n"
        res += "Top K: " + str(self.top_k) + "\n"
        res += "Max output tokens: " + str(self.max_output_tokens) + "\n"
        return res

    def clone(self):
        # type: () -> SavedGameData
        return copy.deepcopy(self)


###########################################
# GENERAL
###########################################


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Gemini safety settings
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    # Saved game data
    saved_game_data: SavedGameData

    # The player's name
    player_name: str = ""  # initial value

    # Gemini Generative Model
    model = gemini.GenerativeModel(model_name="gemini-1.5-pro",
                                       generation_config={
                                           "temperature": 1,
                                           "top_p": 0.95,
                                           "top_k": 64,
                                           "max_output_tokens": 8192,
                                           "response_mime_type": "text/plain",
                                       },
                                       safety_settings=safety_settings)  # initial value

    print("Enter \"NEW GAME\" to create new saved game data.")
    print("Enter \"LOAD GAME\" to load existing saved game data.")
    action: str = input("What do you want to do? ")


if __name__ == "__main__":
    main()
