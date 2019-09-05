# Game Class
import json
import os

from Class_Party import *
from random import *
from Class_Hero import *
from helper_functions import *
from battle import *

project_path = os.getcwd()
save_file_extention = '.json'
save_folder = 'saves'


class Game:
    def __init__(self):
        self.party = Party.generate(self)
        self.Mode = ''
        self.difficulty = ''

    @staticmethod
    def create_character(name='Jeb', profession='Astronaut', level=1):
        """
         Create new character
         Allows selection of char and reroll of stats
         """
        return Hero.generate(name, profession, level)

    @property
    def create_random_character(self):
        """
         Create new random character the same level as the party leader
         """
        return NPC.generate_random(randint(1, self.party.hero.level))

    def create_hero(self):

        def roll_hero():
            hero_name = input('What is your name, hero?:\n').title()
            if len(hero_name) > 10:
                hero_name = input('That\'s too long! (Max 10). What is your name, hero?:\n').title()
            if len(hero_name) > 0:
                print(f'{hero_name}, ah yes. That name carries great respect!')

            else:
                print('Ah, the quiet type huh? I\'ll just call you Steve.')
                hero_name = 'Steve'

            hero_profession = select_from_list(['Warrior', 'Archer', 'Mage', 'Blacksmith', 'Thief', 'Bard'],
                                               q=f'Now, {hero_name}, What is your profession?:\n')
            print(f'You look like a great {hero_profession}, {hero_name}. I should have guessed.')
            our_hero = self.create_character(hero_name, hero_profession)
            print(our_hero.show_stats())
            return our_hero

        while True:
            our_hero = roll_hero()
            keep_hero = input('Do you want to keep this Hero? \n[Y]es or [R]eroll Hero\n').lower()
            if keep_hero == '':
                our_hero.hero = True

                return our_hero
            elif keep_hero == 'y':
                our_hero.hero = True

                return our_hero
            else:
                continue

    def adventure(self):
        event = randrange(5)
        print(event)
        if event == 0:
            print(f'You found another traveler You talk for a while and have a great time!')
            choice = select_from_list(['Yes', 'No'],
                                      'The traveler offers to join your party, what do you say?', False, True)
            if choice == 'Yes':
                self.party.add_member_with_print(self.create_random_character)
            elif choice == 'No':
                print('You bid the traveler farewell and continue on your way.\n')
        elif event == 1:
            # Battle
            enemy_party = Party.generate(self)
            x = 0
            for x in range(randrange(max(1, len(self.party.members) - 1), len(self.party.members) + 1)):
                enemy_party.add_member(
                    NPC.generate_random(randint(self.party.hero.level - 1, self.party.hero.level)))
                x += 1
            clock_tick_battle(self.party, enemy_party)
        elif event == 2:
            # Battle
            enemy_party = Party.generate(self)
            x = 0
            for x in range(randrange(max(1, len(self.party.members) - 1), len(self.party.members) + 1)):
                enemy_party.add_member(
                    NPC.generate_random(randint(max([1, self.party.hero.level - 1]), self.party.hero.level)))
                x += 1
            clock_tick_battle(self.party, enemy_party)
        elif event == 3:
            p1 = create_random_item(2)
            self.party.display_single_item_card(p1)
            self.party.inventory.append(p1)
            print(f'You find an item and toss it in your bag and keep moving.')
        elif event == 4:
            p1 = create_random_item(1)
            self.party.display_single_item_card(p1)
            self.party.inventory.append(p1)
            print(f'You find an item and toss it in your bag and keep moving.')

        else:
            print('\nA tree falls on the party!')
            for member in self.party.members:
                member.set_hp(-20)

    def inventory(self):
        self.party.inventory_menu()

    def camp(self):
        camp_input = select_from_list(['Inventory', 'Rest', 'Craft', 'Continue Adventuring', 'Save', 'Title Screen', 'Exit'],
                                      f'What would you like to do:\n', False, True)
        if camp_input == 'Rest':
            for member in self.party.members:
                while member.hp < member.max_hp:
                    member.set_hp(member.max_hp)
                while member.mana < member.max_mana:
                    member.set_mana(member.max_mana)
        elif camp_input == 'Inventory':
            self.party.inventory_menu()
        elif camp_input == 'Craft':
            print('You need a craftsman.')
            self.camp()
        elif camp_input == 'Exit':
            print('You Head back out into the wilds..')
        elif camp_input == 'Save':
            self.save()
        elif camp_input == 'Title Screen':
            restart = select_from_list(['Yes', 'No'], q='All unsaved progress will be lost. Are you sure?', horizontal=True)
            if restart == 'Yes':
                self.start()
            else:
                self.camp()

    def main_options(self):
        """
        Contains Choices after new game and settings
        """
        print('*' * 100)
        choice = select_from_list(['Adventure', 'Camp', 'Party Info'], f'\nWhat would you like to do\n ', True, True)
        if choice == 0:
            self.adventure()
        elif choice == 1:
            print('\n' * 20)
            print("""    
                 )
                (\033[1;33m
               /`/\\
              (% \033[1;31m%)\033[1;33m)\033[0;0m
            .-'....`-.
            `--'.'`--' """'\n')
            print('  You build a beautiful camp fire.\n')
            self.camp()
        elif choice == 2:
            self.party.print_members_info_cards()

    def game_over(self):
        print('Game Over, Thanks for playing!')

        quit()

    def gameloop(self):
        while self.party.has_units_left:
            self.main_options()

        self.game_over()

    def serialize(self):
        dummy = self.__dict__.copy()
        dummy['party'] = dummy['party'].serialize()
        return dummy

    @classmethod
    def deserialize(cls, save_data):
        dummy = cls()
        dummy.__dict__ = save_data['game'].copy()
        dummy.party = Party.deserialize(dummy.party.copy())
        dummy.party.game = dummy
        return dummy

    def save(self):
        file_name = self.choose_save_name()
        file = os.path.join(project_path, 'saves', file_name)
        with open(file, 'w') as f:
            json.dump({'game': self.serialize()}, f, indent=4)

    def choose_save_name(self):
        file_name = input(f'Choose a name for the save file:') + save_file_extention
        if file_name in os.listdir(save_folder):
            overwrite = select_from_list(['Yes', 'No'], q='File already exists. Overwrite?')
            if overwrite == 'No':
                file_name = self.choose_save_name()
        return file_name

    @classmethod
    def load(cls):
        fn = os.path.join(project_path, save_folder, cls.choose_load_game())
        with open(fn, 'r') as f:
            load_data = json.load(f)
        load_game = cls.deserialize(load_data)
        return load_game

    @classmethod
    def choose_load_game(cls):
        save_games = [f[:-len(save_file_extention)] for f in os.listdir(save_folder) if f[-len(save_file_extention):] == save_file_extention]
        return select_from_list(save_games, q='Which game do you want to load?') + save_file_extention

    @classmethod
    def new_game(cls):
        game = cls()
        game.party = Party.generate(game)
        game.Mode = select_from_list(['Normal', 'AutoCombat'],
                                     'What mode would you like? ** Recommended: Normal **', False, True)
        game.difficulty = select_from_list(['Easy', 'Medium', 'Hard'], 'Choose your difficulty:')
        print(f'You selected: {game.difficulty}!')
        game.party.add_member(game.create_hero())
        print(f'You are all set! Danger is that way, Good Luck, {game.party.member().name}!\n')
        return game

    @classmethod
    def start(cls):
        options = ['New Game']
        if len(os.listdir(save_folder)) > 0:
            options.append('Load Game')
        game_choice = select_from_list(options, horizontal=True)
        if game_choice == 'New Game':
            game = cls.new_game()
        else:
            game = cls.load()
        game.gameloop()


if __name__ == '__main__':
    Game.start()
