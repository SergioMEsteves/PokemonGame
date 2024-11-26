with open('PokeList_v3.csv', 'r') as csv:
    lines = csv.readlines()
    POKEMON_DATA = dict([(l.split(',')[1].lower(), tuple([e.strip() for e in l.split(',')[1:]])) for l in lines])
