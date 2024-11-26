import pygame
import sys
import os
from random import randint, choice
from Pokemon import Pokemon
from PokemonData import POKEMON_DATA
from TrainerSave import TrainerSave
import threading
import CatchMinigame

def main(saveFile):
    global candy_count

    # Initialize Pygame
    pygame.init()

    print(saveFile.name)

    # Load the Candy image
    candy_image = pygame.image.load('Pokemon-Assets/Sprites/candy.png')
    candy_image = pygame.transform.scale(candy_image, (32, 32)) 

    # Track the number of candies
    candy_count = 10 

    # Initialize pygame mixer for background music
    pygame.mixer.init()
    pygame.mixer.music.load(
        "./Pokemon-Assets/Sounds/Music/Game-Background.mp3")  # Path to your music
    pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

    # Keep track of pokemon
    pokemonOnScreen = []

    # Set up display
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Map Game")

    # Map layout (0 = empty, 1 = obstacle)
    file = open("map.txt")
    game_map = [line.strip().split(", ") for line in file.readlines()]
    file.close()

    # To check valid moves
    playerx=8
    playery=7
    inventoryShowing = False

    # Load the sprite sheet
    sprite_sheet = pygame.image.load("Pokemon-Assets/Sprites/Player-Sprites.png").convert_alpha()  # Use the correct file path
    sprite_sheet = pygame.transform.scale(sprite_sheet, (400, 400))
    frames = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            # Extract a frame from the sprite sheet
            frame = sprite_sheet.subsurface((j * 100, i * 100, 100, 100))
            frames[i].append(frame)

    # Tile size after zoom
    TILE_SIZE = 80
    LIGHT_BLUE = (100, 200, 255)
    BLACK = (0, 0, 0)
    # Define font
    font = pygame.font.SysFont(None, 24)


    # Load background image (Make sure the image dimensions match your window)
    background_image = pygame.image.load(
        "./Pokemon-Assets/Game-Background.jpg")
    background_image = pygame.transform.scale(background_image, (800, 600))

    tree_image = pygame.image.load(
        "./Pokemon-Assets/Sprites/tree.png")
    tree_image = pygame.transform.scale(tree_image, (TILE_SIZE, TILE_SIZE))

    # Player setup (fixed position in the center of the screen)
    player_pos = [WIDTH // 2, HEIGHT // 2]  # Center player on screen (50 is half the player's width/height)

    # Cooldown setup
    COOLDOWN = 333  # Cooldown in milliseconds (1000 ms / 3 moves per second)
    last_move_time = 0  # Initialize the last move time

    # Function to get the image for a tile type
    def get_tile_image(tile_type):
        if tile_type == 'G':
            return "grass_image"
        elif tile_type == 'T':
            return tree_image
        elif tile_type == 'B':
            return "building_image"
        else:
            return None  # Default case for unknown symbols

    def start_game(pokemon):
            """
            Starts the catching minigame
            """

            global candy_count
            pygame.mixer.music.stop()
            game = CatchMinigame.PokemonCatchMiniGame(pokemon.nickname.lower())
            game.start_game()
            game.mainloop()
            if game.success:
                saveFile.append_pokemon(pokemon)

                # This just randomly picks 3, 5, or 10 candies
                randnum = randint(3, 10)
                randnum -= randnum%5
                if randnum == 0: randnum = 3
                candy_count += randnum

    # Function to move the camera
    def move(dx, dy):
        nonlocal playerx, playery
        playerx+=dx
        playery+=dy

    # Function to check if a tile is walkable.
    def is_walkable(x, y):
        return game_map[y-1][x]=="0"

    def generateEncounter():
        """ Generates a random pokemon on screen """

        # Check if too many pokemon on screen
        if len(pokemonOnScreen)>=10: pass

        dir_path = './Pokemon-Assets/Sprites/Pokemon/'
        while True:
            pokemon_data = choice(list(POKEMON_DATA.items()))[1]
            if not os.path.exists(dir_path + f'{pokemon_data[0]}.png'):
                pokemon_data = choice(list(POKEMON_DATA.items()))[1]
            else:
                break
        while True:
            randx = randint(6, 23)
            randy = randint(6, 15)
            if game_map[randy][randx] != 'T':
                break
        pokemonOnScreen.append([Pokemon(pokemon_data[0].lower()), randx, randy])
        threading.Timer(5, generateEncounter).start()

    def updateN():
        """ Just updates n value for animation """
        nonlocal n
        n = (n+1)%4

    def draw_inventory(pokemon_list):
        """ Displays inventory """
        x_offset = 50
        y_offset = 100
        for i, pokemon in enumerate(pokemon_list):
            # Draw the Pokémon card background
            pygame.draw.rect(screen, LIGHT_BLUE, (x_offset, y_offset + i * 70, 200, 60))
            
            # Draw the sprite
            screen.blit(pygame.transform.scale(pygame.image.load(f"Pokemon-Assets/Sprites/Pokemon/{pokemon.pokemon_data[0].lower()}.png"), (50, 50)), (x_offset + 5, y_offset + i * 70 + 5))

            # Draw the text (Name, Level, Combat Power)
            name_text = font.render(pokemon.nickname, True, BLACK)
            level_text = font.render(f"Level: {pokemon.level}", True, BLACK)
            cp_text = font.render(f"CP: {pokemon.cp}", True, BLACK)
            
            screen.blit(name_text, (x_offset + 60, y_offset + i * 70 + 5))
            screen.blit(level_text, (x_offset + 60, y_offset + i * 70 + 25))
            screen.blit(cp_text, (x_offset + 60, y_offset + i * 70 + 45))

    def draw_candy_count(candy_count):
        """ Displays candy counter on top right """
        # Draw the candy image
        screen.blit(candy_image, (WIDTH - 70, 10))  # Position near the top-right corner
        
        # Draw the candy count text next to the image
        candy_text = font.render(str(candy_count), True, BLACK)
        screen.blit(candy_text, (WIDTH - 35, 20))  # Position slightly right of the image

    # Game loop
    clock = pygame.time.Clock()
    generateEncounter()
    d = 0
    n = 0

    while True:
        screen.fill((0, 0, 0))  # Fill screen with black to clear previous frames
        screen.blit(background_image, (0, 0))

        # Render the map
        for row_index, row in enumerate(game_map[playery-5:playery+5]):
            for col_index, tile in enumerate(row[playerx-5:playerx+5]):
                # Get the image corresponding to the tile symbol
                tile_image = get_tile_image(tile)
                if tile_image:
                    # Draw the tile image at the correct position
                    screen.blit(tile_image, (col_index * TILE_SIZE, row_index * TILE_SIZE))

        # Draw the player (fixed in the center of the screen)
        screen.blit(frames[d][n], player_pos)

        for info in pokemonOnScreen:
            pokemon, pokex, pokey = info
            screen.blit(pygame.transform.scale(pygame.image.load(f"./Pokemon-Assets/Sprites/Pokemon/{pokemon.nickname.lower()}.png"),
                (TILE_SIZE, TILE_SIZE)), ((pokex-playerx+5)*TILE_SIZE, (pokey-playery+4)*TILE_SIZE))

            # check collision
            if pokex==playerx and pokey==playery:
                start_game(pokemon)
                #pygame.mixer.stop()
                pokemonOnScreen.remove(info) # remove pokemon
                pygame.mixer.music.load("./Pokemon-Assets/Sounds/Music/Game-Background.mp3")
                pygame.mixer.music.play(-1)


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the current time
        current_time = pygame.time.get_ticks()

        dx, dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_i]:
            inventoryShowing = True

        if keys[pygame.K_s]:
            saveFile.save_to_file()

        # show inventory
        if inventoryShowing:
            draw_inventory(saveFile.pokemon_list)

        inventoryShowing = False

        # Draw the candy count in the top-right corner
        draw_candy_count(candy_count)

        # Check if enough time has passed since the last move
        if current_time - last_move_time > COOLDOWN:
            # Player movement input (camera movement)
            if keys[pygame.K_LEFT]:
                d = 1
                dx = -1
                last_move_time = current_time  # Update the last move time
                updateN()
            if keys[pygame.K_RIGHT]:
                d = 2
                dx = 1
                last_move_time = current_time
                updateN()
            if keys[pygame.K_UP]:
                d = 3
                dy = -1
                last_move_time = current_time
                updateN()
            if keys[pygame.K_DOWN]:
                d = 0
                dy = 1
                last_move_time = current_time
                updateN()

            if is_walkable(playerx+dx, playery+dy):
                move(dx, dy)

        pygame.display.update()  # Update the display
        clock.tick(60)  # Set the frame rate to 60 FPS