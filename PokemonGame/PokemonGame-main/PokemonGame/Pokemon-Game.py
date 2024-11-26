import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize pygame mixer for background music
pygame.mixer.init()
pygame.mixer.music.load(
    "./Pokemon-Assets/Sounds/Music/Game-Background.mp3")  # Path to your music
pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Map Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Map layout (0 = empty, 1 = obstacle)
file = open("map.txt")
game_map = [line.strip().split(", ") for line in file.readlines()]
file.close()

# To check valid moves
playerx=8
playery=7

# Tile size after zoom
TILE_SIZE = 80

# Load background image (Make sure the image dimensions match your window)
background_image = pygame.image.load(
    "./Pokemon-Assets/Game-Background.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))

tree_image = pygame.image.load(
    "./Pokemon-Assets/Sprites/tree.png")
tree_image = pygame.transform.scale(tree_image, (TILE_SIZE, TILE_SIZE))

# Load player image
player_image = pygame.image.load(
    "./Pokemon-Assets/Sprites/Player-Temp-Image.png")
player_image = pygame.transform.scale(player_image, (100, 100))  # Scale to match tile size

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

# Function to move the camera
def move(dx, dy):
    global playerx, playery
    playerx+=dx
    playery+=dy

# Function to check if a tile is walkable.
def is_walkable(x, y):
    return game_map[y-1][x]=="0"

# Game loop
clock = pygame.time.Clock()

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
    screen.blit(player_image, player_pos)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the current time
    current_time = pygame.time.get_ticks()

    dx, dy = 0, 0

    # Check if enough time has passed since the last move
    if current_time - last_move_time > COOLDOWN:
        # Player movement input (camera movement)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -1
            last_move_time = current_time  # Update the last move time
        if keys[pygame.K_RIGHT]:
            dx = 1
            last_move_time = current_time 
        if keys[pygame.K_UP]:
            dy = -1
            last_move_time = current_time
        if keys[pygame.K_DOWN]:
            dy = 1
            last_move_time = current_time
        
        if is_walkable(playerx+dx, playery+dy):
            move(dx, dy)

    pygame.display.update()  # Update the display
    clock.tick(30)  # Set the frame rate to 60 FPS