from minion import Minion
from random import randint


class Board:
    def __init__(self, list1, list2):
        # self.player0_minion_num, self.player1_minion_num = len(list1), len(list2)
        self.chess_list0, self.chess_list1 = list1, list2
        self.death_list0,self.death_list1 = [], []
        self.death_rattle_list0, self.death_rattle_list1 = [], []
        self.winner = None

    def play_chess(self):
        first = randint(0,1)
        if first == 0:
            first_list, second_list = self.chess_list0, self.chess_list1
        else: # first == 1
            first_list, second_list = self.chess_list1, self.chess_list0

        atk_list, dfs_list = first_list, second_list
        while len(atk_list) and len(dfs_list):
            attacker = atk_list[0]
            taunt_list = [each for each in dfs_list if hasattr(each, "taunt")]
            taunt_list = dfs_list if not taunt_list else taunt_list
            defender = taunt_list[randint(0, len(taunt_list)-1)]

            # attack
            attacker.attack(defender)
            # overkill
            # divine shield
            # death removal
            atk_list = [each for each in atk_list if not each.dead]
            dfs_list = [each for each in dfs_list if not each.dead]
            # death rattle

            #
            atk_list, dfs_list = dfs_list, atk_list

        if len(atk_list):
            # print(f'Player {first} wins!')
            print([each.name for each in atk_list])
            # return first
        elif len(dfs_list):
            # print(f'Player {int(not first)} wins!')
            print([each.name for each in dfs_list])
            # return int(not first)
        else:
            print(f'Tie!')
            return None

    def summon_new(self, prev_list:list, pos, chess):
        if len(prev_list) == 7:
            return prev_list
        else:
            return prev_list.insert(pos, chess)


if __name__ == '__main__':
    list1 = [Chess(10,7,None,"Red",[]), Chess(11,11,None,"Untamed",[]), Chess(13,10,None,"Maexx",["POISON","DIVINE_SHIELD"])]
    list2 = [Chess(13,11,None,"Holy",["POISON"]), Chess(14,8,None,"bot",["DIVINE_SHIELD"]), Chess(12,16,None,"Sec",["DIVINE_SHIELD"])]
    board = Board(list1, list2)
    # for i in range(100):
    #     print(randint(0,100))
    for i in range(100):
        board.play_chess()