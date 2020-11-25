from minion import Minion

# Register the specific minions

class Scallywag(Minion):
    def __init__(self, *args, **kwargs):
        """
        Minion, 2/1, pirate, Deathrattle: summon a 1/1 pirate. It attacks immediately. 
        """
        super(Minion, self).__init__()


class Fly_Pirate(Minion):
    def __init__(self, *args, **kwargs):
        """
        Minion, 1/1, Attacks immediately. Summoned by Scallywag. 
        """
        super(Minion, self).__init__()