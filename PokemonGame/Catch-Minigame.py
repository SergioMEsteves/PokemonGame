import tkinter as tk
import random

try: # Ensuring installation
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    print("Pillow is not installed. Installing it now...")
    import os
    os.system('pip install Pillow')
    from PIL import Image, ImageTk, ImageDraw
try:
    import pygame
except ImportError:
    print("pygame is not installed. Installing it now...")
    import os
    os.system('pip install pygame')
    import pygame

class PokemonCatchMiniGame(tk.Tk):
    tolerance = 10 # CHANGE AS NEEDED ; impacts how easy it is to win the minigame

    def __init__(self, pokeName):
        super().__init__()

        def resize(image, base_width=50):
            """
                Resizes an image for the minigame constructor
                parameters: image (Type Image), base_width default 30.
                returns: new image
            """
            # Get the current width and height
            width, height = image.size

            # Calculate the new dimensions while maintaining aspect ratio
            w_percent = (base_width / float(width))
            h_size = int((float(height) * float(w_percent)))
            return image.resize((base_width, h_size), Image.Resampling.LANCZOS) # Provides high quality image downsampling

        # Window setup
        self.title("Pokemon Catching Game")
        self.attributes("-fullscreen", True)  # Enable fullscreen
        self.resizable(False, False)  # Disable resizing
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill="both", expand=True)
        self.bind('<Configure>', self.on_resize) # Listen for fullscreen
        self.pokeName=pokeName
        self.pokemon_x=650
        self.pokemon_y=500
        self.canClick=True
        self.ball_x=650
        self.ball_y=800

        # Load background image
        self.load_background("Pokemon-Assets/Forest-Background.jpg")

        # Ring settings
        self.max_ring_size = 150  # Maximum radius of the pulsing ring
        self.min_ring_size = 50   # Minimum radius of the pulsing ring
        self.pulse_speed = 0.01    # Speed at which the ring pulses (larger value = slower pulse)
        self.current_size = self.min_ring_size
        self.is_increasing = True

        # Timing variables
        self.target_time = random.uniform(2.5, 5.0)  # Random time before optimal catch (in seconds)
        self.catch_radius = random.randint(self.min_ring_size + 30, self.max_ring_size - 10)  # FIXME Optimal ring size to catch

        def draw_semi_transparent_ring(self):
                # Create a transparent image to draw on
                image = Image.new("RGBA", (1300, 1000), (0, 0, 0, 0))  # transparent background
                draw = ImageDraw.Draw(image)

                # Coordinates for the oval (the target ring)
                x1 = 650 - self.catch_radius
                y1 = 500 - self.catch_radius
                x2 = 650 + self.catch_radius
                y2 = 500 + self.catch_radius

                # Draw a semi-transparent ring (outline with transparent fill)
                # The ring will be semi-transparent by setting an RGBA value for the color
                # (0, 0, 0, 0) is fully transparent, (128, 128, 128, 128) is semi-transparent gray
                draw.ellipse([x1, y1, x2, y2], outline=(128, 128, 128, 200), width=5)

                # Convert the image to a format Tkinter can use
                photo = ImageTk.PhotoImage(image)

                # Display the image with the semi-transparent ring on the canvas
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

                # Store a reference to the image to prevent garbage collection
                self.canvas.image = photo

        self.pokeImage = resize(Image.open("Pokemon-Assets/Sprites/pokeball.png"))
        def loadPokeballs():
            """
                Loads pokeballs in the top right corner
            """
            # Pokeball counter
            self.pokeballs_left = 5  # FIXME temporarily hardcoded to 3

            # Loading the pokeball image
            pokeball = ImageTk.PhotoImage(self.pokeImage)

            self.pokeballs_on_screen = [] # Will keep track of balls to delete later

            # Adding pokeballs to top right
            for balls in range(self.pokeballs_left):
                self.pokeballs_on_screen.append(self.canvas.create_image(1240 - (balls * 60), 40, image=pokeball))
            self.canvas.pokeball = pokeball  # Prevent garbage collection

        def loadPokemon(name):
            """
                Loads pokemon on screen depending on the name passed to it
            """

            #? Temporary until proper widths are integrated
            pokeWidth = 180
            if name=="charizard":
                pokeWidth+=200

            pokemon = ImageTk.PhotoImage(resize(Image.open(f"Pokemon-Assets/Sprites/Pokemon/{name}.png"), pokeWidth))
            self.canvas.create_image(self.pokemon_x, self.pokemon_y, image=pokemon)
            self.canvas.pokemon = pokemon  # Prevent garbage collection

        self.after_id = None  # To keep track of the pulsing animation

        # Bind Escape to exit fullscreen
        self.bind("<Escape>", self.quit_fullscreen)
        loadPokeballs()
        loadPokemon(pokeName)
        draw_semi_transparent_ring(self)

    def load_background(self, image_path):
        """ Load and set the background image for the canvas. """
        # Open the image and resize it
        self.original_bg_image = Image.open(image_path)  # Store the original PIL Image object
        self.bg_image = ImageTk.PhotoImage(self.original_bg_image)
        
        # Initially create a background (this will get updated later by on_resize)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def on_resize(self, event):
        """ Resize background when the window is resized. """
        new_width, new_height = event.width, event.height

        if self.original_bg_image:
            # Resize the background using the original PIL Image
            background_resized = self.original_bg_image.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            
            # Convert the resized image back to PhotoImage to display it in Tkinter
            self.bg_image = ImageTk.PhotoImage(background_resized)

            # Update the background image on the canvas
            self.canvas.itemconfig(self.canvas.find_all()[0], image=self.bg_image)

    def start_game(self):
        """Start the pulse animation and wait for user input."""
        self.game_running = True
        self.animate_ring()

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load("Pokemon-Assets/Sounds/Music/Battle-Pokemon.mp3")  # Plays music
        pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

    def animate_ring(self):
        """Animate the pulsing ring on the screen."""
        if not self.game_running:
            return

        self.canvas.delete("pulse")  # Clear the previous ring each frame

        # Draw the pulsing ring
        self.canvas.create_oval(
            650 - self.current_size, 500 - self.current_size,
            650 + self.current_size, 500 + self.current_size,
            outline="black", width=2, tags="pulse"
        )

        # Change the size of the ring
        if self.is_increasing:
            self.current_size += 2
            if self.current_size >= self.max_ring_size:
                self.is_increasing = False
        else:
            self.current_size -= 2
            if self.current_size <= self.min_ring_size:
                self.is_increasing = True

        # Check for user click on canvas
        self.canvas.bind("<Button-1>", self.on_click)

        # Schedule the next animation frame
        self.after_id = self.after(int(self.pulse_speed * 1000), self.animate_ring)

    def pause_ring_animation(self):
        """Pause the pulsing ring animation."""
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def resume_ring_animation(self):
        """Resume the pulsing ring animation."""
        if self.game_running:
            self.animate_ring()

    def display_result(self):
        """Display the result after the Pokéball animation finishes."""
        # Check if the click happens at the right moment (optimal ring size)
        if abs(self.current_size - self.catch_radius) <= self.tolerance:  # A small tolerance for timing
            # Catch was successful
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Pokemon-Assets/Sounds/Music/Victory-Pokemon.mp3")  # Victory music
            pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

            self.game_running = False
            self.canvas.create_text(650, 300, text="Pokemon Caught!", fill="green", font=("Arial", 24))
            self.after_cancel(self.after_id)

            button = tk.Button(self.canvas, text="OK", font=("Arial", 14), command=self.quit_fullscreen)
            button.pack()
            return

        # If clicked at the wrong time or ran out of Pokéballs
        if self.pokeballs_left <= 0:
            pygame.mixer.music.stop()
            pygame.mixer.Sound("Pokemon-Assets/Sounds/Effects/loose.mp3").play()
            self.game_running = False
            self.canvas.create_text(650, 300, text=f"Out of Pokeballs! {self.pokeName} escaped!", fill="red", font=("Arial", 24))
            self.after_cancel(self.after_id)

            button = tk.Button(self.canvas, text="OK", font=("Arial", 14), command=self.quit_fullscreen)
            button.pack()
            return

        # If the Pokéball count is still > 0, show the remaining count
        if self.pokeballs_left > 0:
            missed_text = self.canvas.create_text(650, 300, text=f"Missed! {self.pokeballs_left} Left", fill="red", font=("Arial", 18))
            self.after(1000, self.canvas.delete, missed_text)  # Deleting the text after 1 second

    def animate_ball(self):
        """
            Plays a throwing animation for a pokeball
        """

        pokemonX = int(self.pokemon_x)
        pokemonY = int(self.pokemon_y)

       # Calculate the movement step (distance per frame)
        step_x = (self.pokemon_x - int(self.ball_x)) / 10  # Customize steps for speed
        step_y = (self.pokemon_y - int(self.ball_y)) / 10

        # Update Pokéball position
        self.ball_x += step_x
        self.ball_y += step_y
        self.canvas.coords(self.ball, int(self.ball_x), int(self.ball_y))

        # Check if the ball reached the Pokémon
        if not (abs(int(self.ball_x) - pokemonX) < 5 and abs(int(self.ball_y) - pokemonY) < 5):
            self.after(50, self.animate_ball) # Delay per frame
        else:
            self.canClick=True
            self.canvas.delete(self.ball)
            self.display_result()  # Call the callback function when animation is complete
            self.resume_ring_animation()

    def on_click(self, event):
        """Handle the user click event."""
        if not self.game_running:
            return
        
        if not self.canClick:
            return

        self.canClick=False
        self.pause_ring_animation()

        # Throw ball
        self.ball_x=650
        self.ball_y=800
        self.ball_image = ImageTk.PhotoImage(self.pokeImage)
        self.ball = self.canvas.create_image(650, 800, image=self.ball_image)
        self.animate_ball()

        # Decrease num of pokeballs and update images
        self.pokeballs_left -= 1
        pokeball_id = self.pokeballs_on_screen.pop(-1)
        self.canvas.delete(pokeball_id)  # Delete the image from the canvas

    def quit_fullscreen(self, event=None):
        """ Exit the game entirely when Escape is pressed. """
        print("Exiting the game...")
        self.quit()  # This stops the Tkinter mainloop and closes the app
        self.destroy()  # This ensures all resources are cleaned up

# Start the game
if __name__ == "__main__":
    game = PokemonCatchMiniGame("butterfree")
    game.start_game()
    game.mainloop()