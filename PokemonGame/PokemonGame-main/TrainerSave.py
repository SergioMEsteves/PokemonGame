from collections import namedtuple
from random import randint
from datetime import datetime
from Pokemon import Pokemon

PokemonData = namedtuple('PokemonData', ['name', 'minCP', 'maxCP', 'evoString'])

class TrainerSave:

    def __init__(self, filePath = None):
        if filePath:
            with open(filePath, 'r') as save_file:
                self.name, self.tid, self.creation_datetime = save_file.readline().strip().split(',')

                line = save_file.readline()
                pokemon_list = []
                while line:
                    pokemon_list.append(Pokemon.from_string(line.strip()))
                    line = save_file.readline()


                line = save_file.readline()
                item_dict = {}
                while line:
                    split = line.split(',')
                    item_dict[split[0]] = split[1]
                    line = save_file.readline()
        else:
            self.creation_datetime = datetime.now()
            self.tid = hash(self.creation_datetime)
            self.pokemon_list = []
            self.item_dict = {}
            self.name = None

    def set_save_name(self, name):
        '''Sets save file name'''
        self.name = name

    def append_pokemon(self, pokemon):
        '''Adds a pokemon to the trainers pokemon list data'''
        self.pokemon_list.append(pokemon)

    def pokemon_index(self, pid):
        '''Returns the index of the pokemon list for a particular pid'''
        return [p.pid for p in self.pokemon_list].index(pid)

    def release_pokemon(self, pokemon):
        '''Releses a particular pokemon from the pokemon list data'''
        self.pokemon_list.pop(self.pokemon_index(pokemon.pid))