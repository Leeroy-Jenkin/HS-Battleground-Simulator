#!usr/bin/python3.7

from os import name
from random import choice
from prettytable import PrettyTable
from minion_info import minion_info
from battle_info import battle_info

class Minion:
    def __init__(self, atk=1, dfs=1, race=None, name='', flags=None):
        """
        Base minion class
        """
        if flags is None:
            flags = []
        self.atk, self.dfs, self.race, self.name = atk, dfs, race, name
        self.hurt, self.dead = False, False
        self.divine_shield, self.poison, self.deathrattle = False, False, False
        for flag in flags:
            setattr(self, flag, True)

    def attack(self, target, friendly):
        """
        Total procedure for a minion attacking
        """
        self.on_attack(target, friendly)
        dmg = self.on_deal_dmg(target, friendly)
        self.death_remove(friendly)
        # May remove other minions in special cases
        # ... 

        return dmg
    
    def on_attack(self, target, friendly):
        """
        Upon attacking. Not considering divine shield, poisonous, etc yet. 
        """
        # Get buff from Dread Admiral Eliza
        if self.race == 'pirate' or self.race == 'all':
            eliza_buff_atk, eliza_buff_dfs = friendly.friendly_eliza_buff
            for each in friendly.minions:
                each.get_buff(eliza_buff_atk, eliza_buff_dfs)

        # If divine shield, not getting hurt
        if not self.divine_shield:
            self.hurt = True
        if not target.divine_shield:
            target.hurt = True
        
    def on_deal_dmg(self, target, friendly):
        """
        Deal the dmg to both sides. Return the dmg dealt to enemy, 
        """
        if self.hurt:
            self.dfs -= target.atk
            if self.dfs <= 0 or target.poison:
                self.dead = True
        if target.hurt:
            target.dfs -= self.atk
            if target.dfs <= 0 or self.poison:
                target.dead = True

        # some special events may take place here
        # ... 
        return self.atk

    def death_remove(self, friendly):
        """
        Minion dies and gets removed
        """
        if self.dead:
            friendly.minions.remove(self)
            # Should trigger deathrattle accordingly
            if hasattr(self, self.name + '_deathrattle'):
                friendly.event_list.append(self.name + '_deathrattle')

    def get_buff(self, amt_atk, amt_dfs):
        self.atk += amt_atk
        self.dfs += amt_dfs


class MinionSequence:
    def __init__(self, minion_list):
        """
        Register every minion in this sequence
        """
        self.minions = minion_list
        self.should_attack_pos = 0
        self.event_list = []

    def register(self, atk=1, dfs=1, race=None, name='', flags=None, atk_buff=0, dfs_buff=0, pos=-1):
        """
        Register one minion into the sequence
        """
        if len(self.minions) < 7:
            new_minion = Minion(atk, dfs, race, name, flags)
            new_minion.get_buff(atk_buff, dfs_buff)
            self.minions.insert(pos, new_minion)

    # def update_next_attack_pos(self, prev_minion_attack):
    #     """
    #     Update the should_attack_pos
    #     """
    #     idx = self.minions.index(prev_minion_attack) + 1
    #     if idx >= len(self.minions):
    #         idx = 0
    #     self.should_attack_pos = idx
    
    def assign_next_attack(self, target, attacking_minion=None):
        """
        Assign nexReturn the Minion who should attack next (ignoring Fly_Pirates)
        """
        # assign the minion attacking this time
        if attacking_minion is None:
            attacking_minion = self.minions[0]
            
        # assign the minion attacking next time
        event_happen_pos = self.minions.index(attacking_minion)
        idx = event_happen_pos + 1
        if idx >= len(self.minions):
            idx = 0
        self.should_attack_pos = idx
        if len(self.minions):
            next_minion = self.minions[self.should_attack_pos]
        else:
            next_minion = None

        # Pick up a random target to do the attack
        tgt = target.legal_target
        temp_dmg = attacking_minion.attack(tgt, self)
        dmg = [temp_dmg]
        tgt.death_remove(target)

        # Settle all of the events
        while self.event_list:
            event = self.event_list.pop(0)

            # Deathrattle events
            if 'Scallywag_deathrattle' in event:
                riven_list = [each.name for each in self.minions if 'Rivendare' in each.name]
                if 'Golden_Baron_Rivendare' in riven_list:
                    riven_trigger = 3
                elif 'Baron_Rivendare' in riven_list:
                    riven_trigger = 2
                else:
                    riven_trigger = 1

                translate_event = 'Golden_Fly_Pirate_summon' if 'Golden' in event else 'Fly_Pirate_summon'
                for _ in range(riven_trigger):
                    self.event_list.insert(0, translate_event)

            elif event == 'Fly_Pirate_summon' or event == 'Golden_Fly_Pirate_summon':
                if len(self.minions) < 7:
                    name = 'Fly_Pirate' if not 'Golden' in event else 'Golden_Fly_Pirate'
                    info = minion_info[name]
                    self.register(atk=info['atk'], dfs=info['dfs'], race=info['race'], name=name, flags=info['flags'], pos=event_happen_pos)
                    fly_pirate = self.minions[event_happen_pos]
                    
                    target.print_seq()
                    self.print_seq()
                    print('\n')

                    khadgar_list = [each for each in self.minions if 'Khadgar' in each.name]
                    num_to_repeat = 1
                    while len(khadgar_list):
                        khadgar = khadgar_list.pop(0)
                        if 'Golden' in khadgar.name:
                            num_iter = num_to_repeat * 2
                        else:
                            num_iter = num_to_repeat
                        for _ in range(num_iter):
                            if len(self.minions) < 7:
                                name = 'Fly_Pirate' if not 'Golden' in event else 'Golden_Fly_Pirate'
                                info = minion_info[name]
                                self.register(atk=info['atk'], dfs=info['dfs'], race=info['race'], name=name, flags=info['flags'], pos=event_happen_pos+1)
                                khadgar_fly_pirate = self.minions[event_happen_pos+1]
                                
                                target.print_seq()
                                self.print_seq()
                                print('\n')

                                # assume target still lives
                                tgt = target.legal_target
                                temp_dmg = khadgar_fly_pirate.attack(tgt, self)
                                dmg.append(temp_dmg)
                                tgt.death_remove(target)

                                target.print_seq()
                                self.print_seq()
                                print('\n')
                                if not khadgar_fly_pirate.dead:
                                    event_happen_pos += 1

                        num_to_repeat += num_iter

                        # delete non-exist khadgar
                        for each in khadgar_list:
                            if each not in self.minions:
                                khadgar_list.remove(each)

                    # assume target still lives
                    tgt = target.legal_target
                    temp_dmg = fly_pirate.attack(tgt, self)
                    dmg.append(temp_dmg)
                    tgt.death_remove(target)

                    target.print_seq()
                    self.print_seq()
                    print('\n')
                    if not fly_pirate.dead:
                        event_happen_pos += 1
            
            # Khadgar summon events
            elif 'summon' in event and 'Khadgar' not in event:
                pass
        return dmg, next_minion

    def print_seq(self):
        """
        Print the minion sequence
        """
        names, values = [], []
        for each in self.minions:
            names.append(each.name)
            values.append(f'{each.atk}/{each.dfs}')
        t = PrettyTable()
        t.add_row(names)
        t.add_row(values)
        print(t)
    
    @property
    def legal_target(self):
        """
        Collect a list of all friendly minions that can be a target of opponents
        """
        return choice([each for each in self.minions if not hasattr(each, 'taunt')])
    
    @property
    def friendly_eliza_buff(self):
        """
        Get friendly_eliza_buff amount according to # of friendly Eliza
        """
        count = 0
        for each in self.minions:
            if each.name == 'Dread_Admiral_Eliza':
                count += 1
            elif each.name == 'Golden_Dread_Admiral_Eliza':
                count += 2
        return [count * minion_info['Dread_Admiral_Eliza_buff_atk'],
                count * minion_info['Dread_Admiral_Eliza_buff_dfs']]


def main_battle():
    """
    Main process
    """
    friendly, opponent = MinionSequence([]), MinionSequence([])
    for idx, (name, atk_buff, dfs_buff) in enumerate(battle_info['friendly']):
        info = minion_info[name]
        friendly.register(atk=info['atk'], dfs=info['dfs'], race=info['race'], name=name, flags=info['flags'], atk_buff=atk_buff, dfs_buff=dfs_buff, pos=idx)

    for idx, (name, atk_buff, dfs_buff) in enumerate(battle_info['opponent']):
        info = minion_info[name]
        opponent.register(atk=info['atk'], dfs=info['dfs'], race=info['race'], name=name, flags=info['flags'], atk_buff=atk_buff, dfs_buff=dfs_buff, pos=idx)

    # To simplify, assume the opponent doesn't attack
    damages, prior_attack_list, attacking_minion = [], [], None
    while len(friendly.minions) and len(opponent.minions):
        opponent.print_seq()
        friendly.print_seq()
        print('\n')
        # target_opponent = opponent.legal_target
        if prior_attack_list:
            attacking_minion = prior_attack_list.pop()
            # TODO: attack here
        else:
            dmg , attacking_minion = friendly.assign_next_attack(opponent, attacking_minion)
        
        # dmg = attacking_minion.attack(target_opponent, friendly)
        damages += dmg
        
    
    print(f'Damages are: {damages}, total dmg dealt: {sum(damages)}, average dmg on 7 opponents: {sum(damages)/7}')
    if len(friendly.minions):
        print('We win! ')
    else:
        if len(opponent.minions):
            print('We lose...TAT')
        else:
            print("Tie! ")

if __name__ == "__main__":
    main_battle()