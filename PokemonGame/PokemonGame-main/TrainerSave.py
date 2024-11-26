from collections import namedtuple
from random import randint
from datetime import datetime
from Pokemon import Pokemon

PokemonData = namedtuple('PokemonData', ['name', 'minCP', 'maxCP'])

class TrainerSave:

    def __init__(self, filePath = None):
        if filePath:
            with open(filePath, 'r') as save_file:
                self.name, self.tid, self.creation_datetime, self.candy_count = save_file.readline().strip().split(',')
                pokemon_list = []
                while True:
                    line = save_file.readline()
                    if line.strip():
                        pokemon_list.append(Pokemon.from_string(line.strip()))
                    else:
                        break
                self.pokemon_list = pokemon_list
        else:
            self.creation_datetime = datetime.now()
            self.tid = hash(self.creation_datetime)
            self.candy_count = 10
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

    def save_to_file(self):
        with open(f'./Saves/{self.name}.txt', 'w') as f:
            lines = [','.join([self.name, str(self.tid), str(self.creation_datetime), str(self.candy_count)])] + [','.join([p.pokemon_data[0].lower(), p.nickname, str(p.pid), str(p.creation_datetime), str(p.cp), str(p.level)]) for p in self.pokemon_list] + [''] + [','.join(item) for item in self.item_dict.items()]
            f.write('\n'.join(lines))