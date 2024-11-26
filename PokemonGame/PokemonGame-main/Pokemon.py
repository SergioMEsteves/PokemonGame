from datetime import datetime
from random import randint
from PokemonData import POKEMON_DATA

class Pokemon:
    _exp = 0
    MAX_LEVEL = 40
    DOUBLE_CANDY_THRESHOLD = 31

    def __init__(self, pokemon_name, nickname = None, pid = None, creationTime = None, cp = None, level = None):
        self.pokemon_data = POKEMON_DATA[pokemon_name]
        self.nickname = nickname if nickname else pokemon_name
        self.creation_datetime = creationTime if creationTime else datetime.now()
        #self.pid = hash(str(self.creation_datetime) + pokemon_data.name)
        self.cp = cp if cp else randint(pokemon_data.minCP, pokemon_data.maxCP)
        self.level = level if level else 1

    @classmethod
    def from_string(cls, string):
        return cls(*string.split(','))

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        if value != self._exp:
            self._exp = value
            self.attempt_level_up()

    def use_candy(self, num_used):
        """
        Increases exp, then attempts level up
        :param num_used: The amount of candy to be used on the pokemon
        :return: none
        """
        self._exp += 1 # Attempt level up on set

    def attempt_level_up(self):
        """
        Levels up if exp is above a certain treshhold
        :parameter: self
        :return: none
        """

        # Continue attempting to level up until failure
        while True:
            if self.level <= 30 and self._exp >= 1:
                self.level += 1
                self._exp -= 1
            elif self.level < self.MAX_LEVEL and self._exp >= 2:
                self.level += 1
                self._exp -= 2
            else:
                break