import random
import json
from x_Attack_Setups import *

class NPC:

    def __init__(self, name='Mr. Lazy', profession='warrior', level=1):
        """
        Create new person """
        test_weapon = {
            'base_stats': {
                'vit': 5,
                'dex': 2,
                'str': 0,
                'int': 0,
                'agility': 1,
                'toughness': 3,
            },
            'stats': {
                'max_hp': 13,
                'max_mana': 10,
                'armor': 53,
                'magic_resistance': 10,
                'speed': 4,
                'dodge': 4,
                'crit_chance': 50,
                'crit_dmg': 100,
                'elemental_resistance': 10
            },
            'attack_name': 'single_attack_setup',
            'attack_setup': weapon_setups['single_attack_setup'],
        }


        self.hero = False
        self.name = name
        self.profession = profession
        self.party = None  # Only one party at a time

        self.level = level
        self.xp = 0
        self.next_level = 20
        self.worth_xp = 5

        self.base_stats = {
                            'vit': 4,
                            'dex': 4,
                            'str': 4,
                            'int': 4,
                            'agility': 8,
                            'toughness': 9,
                        }

        self.stats = {
            # 'vit': self.base_stats.get('vit'),
            # 'dex': self.base_stats.get('dex'),
            # 'str': self.base_stats.get('str'),
            # 'int': self.base_stats.get('int'),
            # 'agility': self.base_stats.get('agility'),
            # 'toughness': self.base_stats.get('toughness'),

            'max_hp': 0,
            'max_mana': 0,
            'armor': 0,
            'magic_resistance': 0,
            'speed': 0,
            'dodge': 0,
            'crit_chance': 0,
            'crit_dmg': 0,
            'elemental_resistance': 0,  # from items (and toughness?)
        }

        self.equip_slots = {'Main Hand': test_weapon,
                            'Off Hand': None,
                            'Head': None,
                            'Chest': None,
                            'Legs': None,
                            'Feet': None,
                            'Ring': None,
                            'Necklace': None,
                            }
        self.calculate_stats_with_equipment()

        self.tracked_values = {
                                'ct': 1000,  # when c reaches this, unit gets a turn
                                'c': 0,  # holds current charge value - +speed each clock tick in battle
                                'status_effects': [],

                                'hp': self.stats.get('max_hp'),
                                'mana': self.stats.get('max_mana'),
                            }

    def combine_base_stats_with_equipment(self):
        # base_stats = {
        #     'str': self.base_stats['str'],
        #     'dex': self.base_stats['dex'],
        #     'int': self.base_stats['int'],
        #     'vit': self.base_stats['vit'],
        #     'agility': self.base_stats['agility'],
        #     'toughness': self.base_stats['toughness'],
        # }
        #
        gear = [value for value in self.equip_slots.values() if value]
        for key in self.base_stats.keys():
            self.stats[key] = self.base_stats[key] + sum([item['base_stats'].get(key, 0) for item in gear])

    def derive_stats(self):
        with open('char_creation_setup.json', 'r') as f:
            growth_ratios = json.load(f)['growth_ratios']

        #  armor
        # armor_per_str = 2
        # armor_per_lvl = 2
        # armor_per_toughness = 4

        armor_per_str = growth_ratios['str_to_armor']['armor_per_str']
        armor_per_lvl = growth_ratios['str_to_armor']['armor_per_level']
        armor_per_toughness = growth_ratios['toughness_to_armor']['armor_per_toughness']

        #  speed
        # speed_per_dex = 0.03
        # speed_per_agility = 0.2
        # speed_factor = 0.1
        # speed_start = 9

        speed_per_dex = growth_ratios['dex_to_speed']['speed_per_dex']
        speed_per_agility = growth_ratios['dex_to_speed']['speed_per_agility']
        speed_factor = growth_ratios['dex_to_speed']['speed_factor']
        speed_start = growth_ratios['dex_to_speed']['speed_start']

        #  dodge
        dodge_start = 3
        dodge_per_speed = 0.3
        dodge_per_dex = 0.2

        dodge_start = growth_ratios['dex_speed_to_dodge']['start']
        dodge_per_speed = growth_ratios['dex_speed_to_dodge']['dodge_per_speed']
        dodge_per_dex = growth_ratios['dex_speed_to_dodge']['dodge_per_dex']

        #  crit
        # crit_chance_start = 5
        # crit_chan_per_level = 0.25
        # crit_chan_per_dex = 0.25
        #
        # crit_dmg_start = 125
        # crit_dmg_per_level = 1
        # crit_dmg_per_dex = 3

        crit_chance_start = growth_ratios['dex_to_crit']['chance_start']
        crit_chan_per_level = growth_ratios['dex_to_crit']['crit_chan_per_level']
        crit_chan_per_dex =growth_ratios['dex_to_crit']['crit_chan_per_dex']

        crit_dmg_start = growth_ratios['dex_to_crit']['dmg_start']
        crit_dmg_per_level = growth_ratios['dex_to_crit']['crit_dmg_per_level']
        crit_dmg_per_dex = growth_ratios['dex_to_crit']['crit_dmg_per_dex']

        #  hp
        # hp_start = 800
        # hp_per_vit = 40
        # hp_per_lvl = 15

        hp_start = growth_ratios['vit_to_hp']['start']
        hp_per_vit = growth_ratios['vit_to_hp']['hp_per_vit']
        hp_per_lvl = growth_ratios['vit_to_hp']['hp_per_lvl']

        # speed calculation
        speed_from_dex = self.stats['dex'] * speed_per_dex
        speed_from_agility = self.stats['agility'] * speed_per_agility
        self.stats['speed'] = (speed_from_dex + speed_from_agility) * speed_factor + speed_start

        #  dodge calculation
        dodge_from_dex = self.stats['dex'] * dodge_per_dex
        dodge_from_speed = self.stats['speed'] * dodge_per_speed
        self.stats['dodge'] = dodge_from_dex + dodge_from_speed + dodge_start

        #  armor calculation
        armor_from_str = (self.stats['str'] * armor_per_str) + (self.level * armor_per_lvl)
        armor_from_toughness = self.stats['toughness'] * armor_per_toughness
        self.stats['armor'] = armor_from_str + armor_from_toughness

        #  crit calculation
        crit_chance_from_dex = self.stats['dex'] * crit_chan_per_dex
        crit_chance_from_lvl = self.level * crit_chan_per_level
        self.stats['crit_chance'] = crit_chance_from_dex + crit_chance_from_lvl + crit_chance_start

        crit_dmg_from_dex = self.stats['dex'] * crit_dmg_per_dex
        crit_dmg_from_level = self.level * crit_dmg_per_level
        self.stats['crit_dmg'] = crit_dmg_from_dex + crit_dmg_from_level + crit_dmg_start

        #  hp calculation
        self.stats['max_hp'] = self.stats['vit'] * hp_per_vit + self.level * hp_per_lvl + hp_start

    def combine_derived_stats_with_equipment(self):
        keys_to_combine = ['max_hp', 'max_mana', 'armor', 'magic_resistance', 'speed', 'dodge',
                           'crit_chance', 'crit_dmg', 'elemental_resistance']
        gear = [value for value in self.equip_slots.values() if value]
        for key in keys_to_combine:
            self.stats[key] = self.stats[key] + sum([item['stats'].get(key, 0) for item in gear])

    def calculate_stats_with_equipment(self):
        self.combine_base_stats_with_equipment()
        self.derive_stats()
        self.combine_derived_stats_with_equipment()

    def stat_growth(self):
        with open('char_creation_setup.json', 'r') as f:
            class_stats = json.load(f)['cl_base_stats']['classes']
        if self.profession.lower() == 'warrior':
            class_key = 'str_class'
        elif self.profession.lower() == 'mage':
            class_key = 'int_class'
        else:
            class_key = 'dex_class'

        for stat in class_stats[class_key].keys():
            if stat[-6:] == '_p_lvl':
                self.base_stats[stat[:-6]] += class_stats[class_key][stat]

    def level_up(self):
        self.level += 1
        self.xp -= self.next_level
        self.next_level = round(4 * (self.level ** 3) / 5) + 20
        print(f'{self.name} is now {self.level}!')
        self.stat_growth()
        self.calculate_stats_with_equipment()
        self.tracked_values['hp'] = self.stats['max_hp']
        self.tracked_values['mana'] = self.stats['max_mana']

    @property
    def is_alive(self) -> bool:
        return self.tracked_values['hp'] > 0

    def set_hp(self, amount):
        """
        set the hp safely
        :param amount: int: to change / can be positive or negative
        :return: amount
        """
        self.tracked_values['hp'] += amount
        if self.tracked_values['hp'] > self.stats['max_hp']:
            self.tracked_values['hp'] = self.stats['max_hp']
        if self.tracked_values['hp'] < 0:
            self.tracked_values['hp'] = 0
        return amount

    def choose_target(self, target_party):
        """
        picks random target from target_party.members
        :param target_party: party instance
        :return: person from party
        """
        if len(target_party) > 1:
            if self.party.has_hero() or self.party.game.difficulty == 'Medium':
                choice = random.randrange(len(target_party))
                target = target_party[choice]
            else:
                if self.party.game.difficulty == 'Hard':
                    target = min(target_party, key=lambda member: member.tracked_values['hp'])
                elif self.party.game.difficulty == 'Easy':
                    target = max(target_party, key=lambda member: member.tracked_values['hp'])
        else:
            target = target_party[0]
        return target


    def choose_battle_action(self, enemy_party):
        """
        ENDPOINT for battle
        npc will always choose basic attack
        :param enemy_party:
        :return: -
        """
        possible_actions = ['attack', ]
        if self.party.game.difficulty == 'Medium':
            heal_under = 0.2
        elif self.party.game.difficulty == 'Hard':
            heal_under = 0.3
        else:
            heal_under = 0.05
        if self.tracked_values['hp'] / self.stats['max_hp'] < heal_under:
            possible_actions.append('heal')
        action = random.choice(possible_actions)
        return action

    def show_gear(self):
        items = [self.equip_slot['Main Hand'],
                 self.equip_slot['Off Hand'],
                 self.equip_slot['Head'],
                 self.equip_slot['Chest'],
                 self.equip_slot['Legs'],
                 self.equip_slot['Feet'],
                 self.equip_slot['Ring'],
                 self.equip_slot['Necklace']]
        gear = [item for item in items if item]
        for i in gear:
            print(i.item)

    def get_equipped_items(self):
        """
        :return: list of currently equipped items
        """
        return [value for value in self.equip_slots.values() if value]

    def add_xp(self, xp):
        self.xp += xp
        print(f'{self.name} gained {xp} xp!')
        if self.xp > self.next_level:
            self.level_up()


    def info_card(self):

        name = f'{self.name}'
        prof = f'{self.profession}'

        hp = f'HP: {self.tracked_values["hp"]:>3}/{self.stats["max_hp"]:<3}'  # 10
        defense = f'Def: {self.stats["armor"]}'  # 8

        lvl = f'Lvl: {self.level}'
        xp = f'XP: {self.xp}/{self.next_level}'

        stats_str = f'Str: {self.stats["str"]}'  # Trying 3 probly 2
        stats_dex = f'Dex: {self.stats["dex"]}'
        stats_int = f'Int: {self.stats["int"]}'

        dmg_w = 'DMG: '
        # dmg_stat = f'{self.att_dmg_min}/{self.att_dmg_max}'  # 11  # TODO: get calculated dmg?
        crit_w = f'Crit %: '
        crit_stat = f'{self.stats["crit_chance"]:>2}/{self.stats["crit_dmg"]:<3}'  # 15

        # Combine L an R lines
        name = f'{name:<1}{prof:>{21 - len(name)}}'
        level_xp = f'{lvl}{xp:>{21 - len(lvl)}}'
        hp_def = f'{hp}{defense:>{21 - len(hp)}}'
        stats = f'{stats_str:<7}{stats_dex:<7}{stats_int:<7}'
        dmg = '' #  f'{dmg_w}{dmg_stat:>{21 - len(dmg_w)}}'
        crit = f'{crit_w}{crit_stat:>{21 - len(crit_w)}}'
        return [name, level_xp, hp_def, stats, dmg, crit]



    def show_stats(self):
        print(f'\n{self.name},the {self.profession}\n'
              f'Level:\t{self.level:>4}  XP: {self.xp:>6}/{self.next_level}\n'
              f'HP:\t   {self.tracked_values["hp"]}/{self.stats["max_hp"]:<4}\n'
              f'Str:\t   {self.stats["str"]:<3}Damage: ' # {self.att_dmg_min:>3}/{self.att_dmg_max:<3}\n' # TODO: get calculated stats?
              f'Dex:\t   {self.stats["dex"]:<3}Crit:  {self.stats["crit_chance"]}%/{self.stats["crit_dmg"]}%\n'
              f'Int:\t   {self.stats["int"]:<3}Defence: {self.stats["armor"]:>5}\n')

    def show_combat_stats(self):
        name = f'{self.name}, the {self.profession}'
        hp = f'Hp: {self.tracked_values["hp"]:>2}/{self.stats["max_hp"]:<2}'
        # dmg = f'Dmg: {self.att_dmg_min:>2}/{self.att_dmg_max:<2}'  # TODO: get calculated stats?
        return f'{name:^23} ' \
               f'{hp:<8} ' \
               # f'{dmg:<13}'




    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{self.name}, the {self.profession}'


dummy_game = {'difficulty': 'Hard'}