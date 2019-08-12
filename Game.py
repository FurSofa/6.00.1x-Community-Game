# Game Class
from party import *
from random import *
from Hero import *
from helper_functions import *
from battle import *


class Game:
    def __init__(self):
        self.party = Party.generate()
        self.autobattle = 0
        self.difficulty = select_from_list(['Easy', 'Medium', 'Hard'], q='Choose your difficulty: ')
        print(f'You selected: {self.difficulty}!')

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
        return Person.generate_random(randint(1, self.party.hero.level))

    def create_hero(self):

        def roll_hero():
            hero_name = input('What is your name, hero?:\n').title()
            if len(hero_name) >10:
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
            our_hero.hero_stat_buff()
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
        event = randrange(4)
        print(event)
        if event == 0:
            print(f'You found another traveler You talk for a while and have a great time!')
            choice = combat_select_from_list(['Yes', 'No'], False,
                                             'The traveler offers to join your party, what do you say?').lower()
            if choice == 'yes':
                self.party.add_member(self.create_random_character)
            elif choice == 'no':
                print('You bid the traveler farewell and continue on your way.\n')
        elif event == 1:
            # Battle
            enemy_party = Party.generate()
            x = 0
            for x in range(randrange(len(self.party.members) - 1, len(self.party.members) + 1)):
                enemy_party.add_member(
                    Person.generate_random(randint(self.party.hero.level - 1, self.party.hero.level)))
                x += 1
            alternating_turn_battle(self.party, enemy_party)
        elif event == 2:
            # Battle
            enemy_party = Party.generate()
            x = 0
            for x in range(randrange(len(self.party.members) - 1, len(self.party.members) + 1)):
                enemy_party.add_member(
                    Person.generate_random(randint(self.party.hero.level - 1, self.party.hero.level)))
                x += 1
            alternating_turn_battle(self.party, enemy_party)
        elif event == 3:
            print(f'You found another traveler You talk for a while and have a great time!')
            print('You bid the traveler farewell and continue on your way.\n')
        else:
            print('\nA tree falls on the party!')
            for member in self.party.members:
                member.take_dmg(20)

    def camp(self):
        print('\n'*10)
        print("""    
             )
            (\033[1;33m
           /`/\\
          (% \033[1;31m%)\033[1;33m)\033[0;0m
        .-'....`-.
        `--'.'`--' """)
        print('  You build a beautiful camp fire.\n')
        input = combat_select_from_list(['Rest', 'Inventory', '??', 'Continue Adventuring'],
                                        q=f'What would you like to do: ')
        if input == 'Rest':
            for member in self.party.members:
                member.heal(member.max_hp)
            bear_attack = randint(1, 100)
            if bear_attack < 3:
                print('A bear got into the camp and killed everyone!')
                self.party.kill_everyone()
        elif input == 'inventory':
            pass
        elif input == '':
            pass
        elif input == '':
            pass

    def main_options(self):
        """
        Contains Choices after new game and settings
        """

        choice = select_from_list(['Adventure', 'Camp', 'Party Info'], True, q=f'\nWhat would you like to do\n ')
        if choice == 0:
            self.adventure()
        elif choice == 1:
            self.camp()
        elif choice == 2:
            self.party.party_members_info()

    def game_over(self):
        print('Game Over, Thanks for playing!')

        quit()

    def gameloop(self):
        self.party.add_member(self.create_hero())
        print(f'You are all set! Danger is that way, Good Luck, {self.party.member().name}!\n')
        while self.party.has_units_left:
            self.main_options()

        self.game_over()


if __name__ == '__main__':
    g = Game()
    g.gameloop()
