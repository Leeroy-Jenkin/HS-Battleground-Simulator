

class Minion:
    def __init__(self, atk=1, dfs=1, race=None, name='', FLAGS=None):
        if FLAGS is None:
            FLAGS = []
        self.atk, self.dfs, self.race, self.name, self.FLAGS = atk, dfs, race, name, FLAGS
        self.hurt, self.dead = False, False
        for flag in self.FLAGS:
            if flag == "TAUNT":
                self.taunt = True
            # if flag is "OVERKILL_0": # Herald of flame
            #     self.overkill_type = 0
            #     self.overkill = False
            # if flag is "OVERKILL_1": # Ironhide direhorn
            #     self.overkill_type = 1
            #     self.overkill = False
            if "OVERKILL" in flag:
                self.overkill_type = int(flag.split("_")[1])
                self.overkill = False
            if flag == "DIVINE_SHIELD":
                self.divine_shield = True
                self.lose_divine_shield = False
            if flag == "POISON":
                self.poison = True
            if flag == "REBORN":
                self.reborn = True
            if "DEATH_RATTLE" in flag:
                self.death_rattle_type = int(flag.split("_")[1])
                self.death_rattle = True

            # if flag == "ON_ATTACKING":
            #     self.on_attacking = False
            # if flag == "ON_ATTACKED":
            #     self.on_attacked = False
            if "ON_DAMAGED" in flag:
                self.on_damaged_type = int(flag.split("_")[1])
                self.on_damaged = False
            if "ON_SUMMON" in flag:
                self.on_summon_type = int(flag.split("_")[1])
                # self.on_summon = False
            if "ON_FRIENDLY_DIVINE_SHIELD_DISAPPEAR" in flag:
                self.on_friendly_divine_shield_disappear_type = int(flag.split("_")[1])

        if not hasattr(self, "divine_shield"):
            self.divine_shield = False

    def attack(self, target):
        if hasattr(self, "overkill"):
            self.overkill = False
        # if (self.divine_shield is True) \
        #         or (target.divine_shield is True):
        if self.divine_shield == True:
            if target.atk == 0:
                self.hurt = False
            else:
                self.divine_shield, self.hurt = False, False
                self.lose_divine_shield = True
                # loses divine shield!
        else:
            self.hurt = True
        if target.divine_shield == True:
            if self.atk == 0:
                target.hurt = False
            else:
                target.divine_shield, target.hurt = False, False
                target.lose_divine_shield = True
                # loses divine shield!
        else:
            target.hurt = True

        if self.hurt:
            self.dfs -= target.atk
            if hasattr(target, "poison") or self.dfs <= 0:
                self.dead = True
                # death queue

        if target.hurt:
            target.dfs -= self.atk
            if hasattr(self, "poison") or target.dfs <= 0:
                target.dead = True
                # death queue

            if target.dfs < 0 and hasattr(self, "overkill"):
                self.overkill = True
                # overkill event

    def deal_damage(self, amt, target):
        if hasattr(self, "overkill"):
            self.overkill = False
        if target.divine_shield is True:
            if amt == 0:
                target.hurt = False
            else:
                target.divine_shield, target.hurt = False, False
                target.lose_divine_shield = True
                # loses divine shield!
        else:
            target.hurt = True

        if target.hurt:
            target.dfs -= amt
            if hasattr(self, "poison") or target.dfs <= 0:
                target.dead = True
                # death queue

            if target.dfs < 0 and hasattr(self, "overkill"):
                self.overkill = True
                # overkill event
