pc_box = None # Holds a list of pokemon that will be rendered when the pc_box is displayed
selected_pokemon = None # The pokemon that is highlighted within the pc_box, its information will be displayed
active_savefile = None # The active savefile that stores information that is read and needs to be written to file
POKEMON_DATA = None # A dictionary that maps pokemon names to a tuple containing their csv data
MAX_LEVEL = 40
DOUBLE_CANDY_THRESHOLD = 31

def throw_pokeball():
    '''Uses one pokeball, if timing is within the tolerated range, the catch is successful, returns pokemon data is successful and None if failed'''
    pass

def reward_candy():
    '''Adds 3, 5, or 10 candies to the trainers candy_count if a catch is successful'''
    pass

def set_active_pokemon():
    '''Sets the active pokemon in the pc_box'''
    pass

def attempt_level_up():
    '''Uses the number of candy to level up, only succeeds if enough candy is provided'''
    pass

def wild_encounter():
    '''Generates a wild encounter on the map'''
    pass

def display_pokemon_data():
    '''Displays a pokemon and its cp and level'''
    pass

def generate_pc_box():
    '''Adds the first 30 pokemon caught to the pc_box'''
    pass

def display_pc_box():
    '''Generates a GUI that allows the user to select pokemon and displays all pokemon in the pc_box'''
    pass

def load_savefile():
    '''Initializes TrainerSave objects from files to be read into the game'''
    pass

def write_savefile():
    '''Wrties a TrainerSave object to a file to be read on another launch of the game'''
    pass