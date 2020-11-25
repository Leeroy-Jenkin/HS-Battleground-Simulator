 
# 酒馆战棋模拟器
这是一个基于Python的酒馆战棋对战模拟器！它可以模拟对战并计算有趣的数据，例如某个流派的极限伤害。

## 用法
命令行输入 

```shell
python3 src/simplify_pirate
```

输出数据及随从变化情况。

如果需要自行更改随从：在 src/battle_info.py 中增加/移除随从。数据格式：

(<随从名称>, <攻击力buff值>, <血量buff值>)

## 说明
目前仅支持：海盗无赖，亡灵舰长伊利扎，卡德加，瑞文戴尔男爵。（跳操海盗的阵容）

其它随从随后加入 ...


# HS-Battleground-Simulator
This is a Simulator for Hearthstone Battleground mode based on Python. It calculates interesting statistics, e.g. extreme damage. 

## Usage
Type this in the shell: 

```shell
python3 src/simplify_pirate.py
```

And see the outputs for statistics and minion changes. 

If you would like to change minions: go to src/battle_info.py and add/remove minions. Data format: 

(<minion_name>, <attack_buff>, <health_buff>)

## Notes
Currently only support minions: Scallywag, Dread_Admiral_Eliza, Khadgar, Baron_Rivendare. 

Other minions to be continued ...
