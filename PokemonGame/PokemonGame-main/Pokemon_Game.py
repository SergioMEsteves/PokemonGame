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

    grass_image = pygame.image.load(
        "./Pokemon-Assets/Sprites/grass.png")
    grass_image = pygame.transform.scale(grass_image, (TILE_SIZE, TILE_SIZE))

    stone_image = pygame.image.load(
        "./Pokemon-Assets/Sprites/stone.png")
    stone_image = pygame.transform.scale(stone_image, (TILE_SIZE, TILE_SIZE))

    # Player setup (fixed position in the center of the screen)
    player_pos = [WIDTH // 2, HEIGHT // 2]  # Center player on screen (50 is half the player's width/height)

    # Cooldown setup
    COOLDOWN = 200  # Cooldown in milliseconds (1000 ms / 3 moves per second)
    last_move_time = 0  # Initialize the last move time

    # PC Box Variables
    pc_box = []
    current_box_index = 0
    selected_pokemon_index = 0
    BOX_ROW_COUNT = 5
    BOX_COL_COUNT = 6
    BOX_COUNT = BOX_COL_COUNT * BOX_ROW_COUNT

    def generate_pc_box(index):
        '''Populates the PC box with Pokemon from the players collection'''
        box = []

        for i in range(BOX_COUNT * index, BOX_COUNT * (index + 1) + 1):
             if i < len(saveFile.pokemon_list):
                 box.append(saveFile.pokemon_list[i])
             else:
                 box.append(None)
        return box

    def draw_pc_box():
        '''Draws the PC box with Pokemon within it'''
        screen.fill((255, 255, 255))
        y_offset = 50
        x_offset = 50
        for i in range(BOX_ROW_COUNT):
            for j in range(BOX_COL_COUNT):
                index = i * BOX_COL_COUNT + j
                pokemon = pc_box[index]
                rect = pygame.Rect(x_offset + j * TILE_SIZE, y_offset + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, LIGHT_BLUE, rect)
                if pokemon:
                    pokemon_sprite = pygame.image.load(
                        f"Pokemon-Assets/Sprites/Pokemon/{pokemon.pokemon_data[0].lower()}.png")
                    pokemon_sprite = pygame.transform.scale(pokemon_sprite, (TILE_SIZE, TILE_SIZE))
                    screen.blit(pokemon_sprite, rect.topleft)

                if index == selected_pokemon_index:
                    pygame.draw.rect(screen, (0, 255, 0), rect, 5)

    # Handle movement between PC boxes
    def navigate_pc_menu():
        nonlocal selected_pokemon_index, current_box_index
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            selected_pokemon_index = (selected_pokemon_index - BOX_COL_COUNT) % BOX_COUNT
        elif keys[pygame.K_DOWN]:
            selected_pokemon_index = (selected_pokemon_index + BOX_COL_COUNT) % BOX_COUNT
        elif keys[pygame.K_LEFT]:
            selected_pokemon_index = (selected_pokemon_index - 1) % BOX_COUNT
        elif keys[pygame.K_RIGHT]:
            selected_pokemon_index = (selected_pokemon_index + 1) % BOX_COUNT
        elif keys[pygame.K_RETURN]:
            # Select the Pokémon if there is one
            selected_pokemon = pc_box[selected_pokemon_index]
            if selected_pokemon:
                print(f"Selected {selected_pokemon.nickname}")
        elif keys[pygame.K_ESCAPE]:
            # Exit the PC box and go back to the main game
            return False  # Returning False means the menu should close
        return True

    # Function to get the image for a tile type
    def get_tile_image(tile_type):
        """ Returns an image for the type of object in that position. """

        if tile_type == 'G':
            return grass_image
        elif tile_type == 'T':
            return tree_image
        elif tile_type == 'S':
            return stone_image
        else:
            return None  # Default case for unknown symbols

    def start_game(pokemon):
            """
            Starts the catching minigame
            """


            nonlocal candy_count, pc_box

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
                nonlocal candy_count
                candy_count += randnum
                pc_box = generate_pc_box(0)

    def move(dx, dy):
        """ Function to move the camera """
        nonlocal playerx, playery
        playerx+=dx
        playery+=dy

    def is_walkable(x, y):
        """ Function to check if a tile is walkable. """
        return game_map[y-1][x]=="0"or game_map[y-1][x]=="G"

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
            if game_map[randy][randx] != 'T' and game_map[randy][randx] != 'S':
                break
        pokemonOnScreen.append([Pokemon(pokemon_data[0].lower()), randx, randy])
        threading.Timer(5, generateEncounter).start()

    def updateN():
        """ Just updates n value for animation """
        nonlocal n
        n = (n+1)%4

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
    pc_box = generate_pc_box(0)

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

        # Handle PC box menu
        if inventoryShowing:
            if not navigate_pc_menu():
                inventoryShowing = False  # Exit PC box menu
            draw_pc_box()

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