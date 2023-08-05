"""The PyRPG Lib, Written By Nirudium"""
__version__ = '1.4.0'
import random


# Defines and stores Enemy Stats
class Enemy:

    def __init__(self, **kwargs):
        self.name_opts = ["Thot", "Alpha Thot", "Thot with Pumkin Spice", 'Erika Costell'] or kwargs.get('namelist')
        self.level = kwargs.get("level") or random.randint(1, 10)
        self.name = kwargs.get("name") or random.choice(self.name_opts)
        self.health = kwargs.get("health") or self.level * 3
        self.attack = kwargs.get("attack") or self.level * 2
        self.gold = self.level * 3 or kwargs.get('gold')
        self.xp = kwargs.get("xp") or self.level * random.randint(1, 5)
        self.e_data = "Level {} {} [HEALTH: {} | ATK: {} | XP: {}] ENCOUNTERED".format(
                self.level, self.name, self.health, self.attack, self.xp)

    def __repr__(self):
        return "<Enemy(name={}, health={}, attack={},, level={}) xp={}>".format(
                self.name, self.health, self.attack, self.level, self.xp)

    def __str__(self):
        return "Level {} {} [HEALTH: {} | ATK: {} | XP: {}] ENCOUNTERED".format(
                self.level, self.name, self.health, self.attack, self.xp)


# Defines and stores Player Stats and handles leveling Logic
class Player:
    player_name_opts = ('Makar', 'Joker', 'Gumball The SJW Destroyer', 'Inigo The Brave', 'Noor The Thot/Furry/SJW Hunter', 'Keemstar The Thot Obliterator', 'Hito')

    def __init__(self, **kwargs):
        self.name = kwargs.get("name") or random.choice(self.player_name_opts)
        self.level = kwargs.get("level") or 1
        self.health = self.level * 3
        if self.health == 0:
            self.health = 30 * self.level
        self.attack = kwargs.get("attack") or self.level * 2
        self.xp = 1
        self.gold = 0
        self.death = 0
        self.maxhp = self.level * 3
        self.inventory = []

    def __repr__(self):
        return "<player(name={}, health={}, attack={}, level={})>".format(
                self.name, self.health, self.attack, self.level)

    def __str__(self):
        return "Level {} {} [HEALTH: {} | ATK: {} | Level = {}]".format(
                self.level, self.name, self.health, self.attack)

    def leveling(self):
        if self.xp == (self.xp + 1) * 1.5:
            self.level = self.level + 1
            self.xp = 0


p = Player()


# Handles All Battle Logic
class Battle:
    def __init__(self, **kwargs):
        global p
        self.foelvl = kwargs.get('foelvl')
        self.turn = kwargs.get('turn') or random.randint(0, 1)
        self.magic_damage = p.level * 2 or kwargs.get('Magic_Damage')
        self.spell_one = {'name': 'heal', 'damage': self.magic_damage / 2, 'cost': 3} or kwargs.get('spell_one')
        self.spell_two = {'name': 'fireball', 'damage': self.magic_damage, 'cost': 5} or kwargs.get('spell_two')
        self.spell_three = {'name': 'freeze', 'damage': self.magic_damage * 2, 'cost': 6} or kwargs.get('spell_two')
        self.mana = p.level * 2
        self.namelist = ["Thot", "Alpha Thot", "Thot with Pumkin Spice", 'Erika Costell'] or kwargs.get('namelist')
        self.name = kwargs.get('name') or random.choice(self.namelist)
        self.gold = kwargs.get('gold')
        self.xp = kwargs.get('xp')
        self.e = Enemy(level=self.foelvl, name=self.name, xp=self.xp, gold=self.gold)
        p.mana = self.mana

    def spell_choice(self):
        if self.mana <= 0:
            print('you have no mana left!')
        elif self.mana > 0:
            print('Type 1 to cast {}'.format(self.spell_one.get('name')))
            print('2 to cast {} at your foe,'.format(self.spell_two.get('name')))
            choice = input('or type 3 in order to cast {}: '.format(self.spell_three.get('name')))
            if choice == '1':
                p.health = p.health + self.spell_one
                print(f'You healed yourself to {p.health} health!')
                self.mana = self.mana - self.spell_list[0]['cost']
                print(f'You now have {self.mana} mana left!')
            elif choice == '2':
                self.e.health = self.e.health - self.spell_list[1]['fireball']
                print(f'The Enemy now has {self.e.health} Health left!')
                self.mana = self.mana - self.spell_list[1]['cost']
                print(f'You have {self.mana} mana left!')
            elif choice == '3':
                self.e.health = self.e.health - self.spell_list[2]['freeze']
                print(f'The Enemy now has {self.e.health} health left!')
                self.mana = self.mana - self.spell_list[2]['cost']
                print(f'You now have {self.mana} mana left!')

    def battle(self, foelvl):
        roll = random.randint(1, 100)
        print(self.e.e_data)
        self.turn = 1
        while p.health > 0 or self.e.health > 0:
            if self.turn == 1:
                choice = input('Do you wish to carry out the battle? "1" for yes, "2" for no, or "3" to cast an ability (W/o quotes): ')
                if choice == '1':
                    if roll == 69:
                        print('You missed!')
                        self.turn = 0
                        roll = random.randint(1, 100)
                    elif roll != 69:
                        print('You Hit!')
                        self.e.health = self.e.health - p.attack
                        print(f'The foe has {self.e.health} Health Left')
                        self.turn = 0
                        roll = random.randint(1, 100)
                    elif choice == '2':
                        self.turn = 0
                if choice == '3':
                    self.spell_choice()
                    self.turn = 0
            elif self.turn == 0:
                print('The Enemy has the turn now!')
                if roll == 69:
                    print('The Enemy Missed!')
                    self.turn = 1
                    roll = random.randint(1, 100)
                elif roll != 61:
                    print('The Enemy Hit!')
                    p.health = p.health - self.e.attack
                    print(f'You have {p.health} Health Left!')
                    self.turn = 1
                    roll == random.randint(1, 100)
                    if p.health <= 0:
                        p.death = 1
                        return p.death
                        print('Battle Lost!')
                        break
                    elif self.e.health <= 0:
                        print('The enemy died!')
                        p.gold = self.e.gold + p.gold
                        print(f'You have earned {self.e.gold} and now have {p.gold}')
                        break


def enemy_encounter(level, **kwargs):
    name = kwargs.get('name')
    xp = kwargs.get('xp')
    gold = kwargs.get('gold')
    b = Battle(foelvl=level, name=name, xp=xp, gold=gold)
    b.battle(level)


def genfoe(level, **kwargs):
    e = Enemy(name=kwargs.get('name'), level=level, gold=kwargs.get('gold'), xp=kwargs.get('xp'), health=kwargs.get('health'), attack=kwargs.get('attack'))
    global ename, elvl, ehp, egold, exp, eattack, ehealth
    ename = e.name
    elvl = e.level
    ehp = e.health
    egold = e.gold
    exp = e.xp
    eattack = e.attack
    ehealth = e.health

# Test
if __name__ == "__main__":
    enemy_encounter(1, name='gay', xp=1000, gold=10000)
