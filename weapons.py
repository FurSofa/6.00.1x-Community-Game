import random

class Weapon:
    def __init__(self, dmg, defence):
        self.attack_dmg = dmg
        self.defence = defence
        self.holder = None

    def deal_dmg(self, target):
        dmg_dealt = self.holder.calculate_dmg()
        dmg_enemy_received = target.take_dmg(dmg_dealt)
        print(self.holder, 'deals', dmg_enemy_received, 'dmg to', target)
        return dmg_enemy_received


class Sword(Weapon):
    def __init__(self, dmg, defence):
        super().__init__(dmg, defence)
        self.attack_dmg = dmg
        self.defence = defence


class Axe(Weapon):
    def __init__(self, dmg, defence):
        super().__init__(dmg, defence)
        self.attack_dmg = dmg
        self.defence = defence

    # TODO: test axe members list, test if this removes target from party
    def deal_dmg(self, target):
        dmg_dealt = self.holder.calculate_dmg()
        dmg_received = target.take_dmg(dmg_dealt)
        print(self.holder, 'deals', dmg_received, 'dmg to', target)
        if len(target.party.members) > 1:
            members_list = target.party.members
            members_list.remove(target)
            target2 = random.choice(members_list)
            dmg_received2 = target2.take_dmg(self.holder.calculate_dmg()//2)
            print('and', dmg_received2, 'dmg to', target2)
            dmg_received += dmg_received2
        return dmg_received
