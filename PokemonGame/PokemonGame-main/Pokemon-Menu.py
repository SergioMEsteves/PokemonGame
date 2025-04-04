import tkinter as tk
import Pokemon_Game
from TrainerSave import TrainerSave
from functools import partial
from random import choice
from PokemonData import POKEMON_DATA
from Pokemon import Pokemon
import os
try: # Ensuring installation
    from PIL import Image, ImageTk, ImageEnhance
except ImportError:
    print("Pillow is not installed. Installing it now...")
    os.system('pip install Pillow')
    from PIL import Image, ImageTk, ImageEnhance
try:
    import pygame
except ImportError:
    print("pygame is not installed. Installing it now...")
    import os
    os.system('pip install pygame')
    import pygame

class GameMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Pokémon Game Menu")
        self.attributes("-fullscreen", True)  # Fullscreen mode
        self.bind("<Escape>", lambda event: self.quit_game())  # Exit fullscreen with ESC key
        self.bind('<Configure>', self.on_resize) # Listen for fullscreen

        # Set up the canvas to handle the background image
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Initialize images
        self.image_paths = [
            "Pokemon-Assets/MenuBackground1.jpg",  
            "Pokemon-Assets/MenuBackground2.jpg",  
            "Pokemon-Assets/MenuBackground3.jpg"   
        ]

        # Set up zoom variables
        self.zoom_factor = 1.5  # Starts at normal size
        self.zoom_step = 0.0025  # Zoom-out increment
        self.min_zoom = 1.0    # Minimum size (when to switch image)
        self.darken_factor = 0.4  # Adjust this factor to darken the image (0.0 - completely black, 1.0 - normal brightness)
        self.current_image_index = 0
        self.load_background_image(self.image_paths[self.current_image_index])

        # Load title image
        self.title_image = Image.open(
            "./Pokemon-Assets/Sprites/pokemonTitle.png")
        self.title = ImageTk.PhotoImage(self.title_image)

        pixel_font = ("Press Start 2P", 14) # Doesn't actually work just sets sizes for buttons.

        self.selected_save = TrainerSave()

        self.saves_button = tk.Button(
            self,
            text="Select Save",
            font=pixel_font,
            fg="yellow",
            bg="#355C7D",
            activebackground="#6C5B7B",
            relief="ridge",
            bd=5,  # A thicker border
            highlightthickness=2,
            highlightbackground="#222",  # Dark border to blend with the darkened background
            command=self.show_saves
        )

        self.start_button = tk.Button(
            self,
            text="Start Game!",
            font=pixel_font,
            fg="yellow",  # Text color
            bg="#355C7D",  # A Pokémon blue/purple color
            activebackground="#6C5B7B",
            relief="ridge",
            bd=5,  # A thicker border
            highlightthickness=2,
            highlightbackground="#222",  # Dark border to blend with the darkened background
            command=self.start_game
        )

        self.quit_button = tk.Button(
            self,
            text="Quit",
            font=pixel_font,
            fg="yellow",  # Text color
            bg="#355C7D",  # A Pokémon blue/purple color
            activebackground="#6C5B7B",
            relief="ridge",
            bd=5,  # A thicker border
            highlightthickness=2,
            highlightbackground="#222",  # Dark border to blend with the darkened background
            command=self.quit_game
        )

        self.instructions_button = tk.Button(
            self,
            text="Instructions",
            font=pixel_font,
            fg="yellow",  # Text color
            bg="#355C7D",  # A Pokémon blue/purple color
            activebackground="#6C5B7B",
            relief="ridge",
            bd=5,  # A thicker border
            highlightthickness=2,
            highlightbackground="#222",  # Dark border to blend with the darkened background
            command=self.show_instructions
        )

        # Initially hidden Overlay frames
        self.instructions_overlay = None
        self.saves_overlay = None

        # Hover animations to buttons
        def on_enter(e):
            e.widget['bg'] = '#6C5B7B'  # Change to a brighter color on hover

        def on_leave(e):
            e.widget['bg'] = '#355C7D'  # Revert to original color

        self.saves_button.bind("<Enter>", on_enter)
        self.saves_button.bind("<Leave>", on_leave)
        self.start_button.bind("<Enter>", on_enter)
        self.start_button.bind("<Leave>", on_leave)
        self.quit_button.bind("<Enter>", on_enter)
        self.quit_button.bind("<Leave>", on_leave)
        self.instructions_button.bind("<Enter>", on_enter)
        self.instructions_button.bind("<Leave>", on_leave)

        # Initialize pygame mixer for background music
        pygame.mixer.init()
        pygame.mixer.music.load(
            "./Pokemon-Assets/Sounds/Music/Background.mp3")  # Path to your music
        pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

        # Start the zoom-out animation
        self.zoom_out_animation()

    def load_background_image(self, image_path):
        """Load and resize the background image based on the zoom factor, and apply darkening effect."""
        self.background_image = Image.open(image_path)
        resized_width = int(self.winfo_screenwidth() * self.zoom_factor)
        resized_height = int(self.winfo_screenheight() * self.zoom_factor)
        self.resized_bg_image = self.background_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

        # Darken the image
        enhancer = ImageEnhance.Brightness(self.resized_bg_image)
        darkened_image = enhancer.enhance(self.darken_factor)

        self.tk_bg_image = ImageTk.PhotoImage(darkened_image)

        # Center the image by calculating the position offsets
        x_offset = (self.winfo_screenwidth() - resized_width) // 2
        y_offset = (self.winfo_screenheight() - resized_height) // 2
        self.canvas.delete("bg_image")
        self.canvas.create_image(x_offset, y_offset, image=self.tk_bg_image, anchor="nw", tags="bg_image")
        try:
            self.canvas.tag_raise(self.title_image_id)  # Raise title to the top
        except:
            pass
    
    def zoom_out_animation(self):
        """Animate the zoom-out effect and switch images when reaching the minimum zoom."""
        self.zoom_factor -= self.zoom_step
        if self.zoom_factor <= self.min_zoom:
            # Reset zoom and switch to the next image
            self.zoom_factor = 1.5
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.load_background_image(self.image_paths[self.current_image_index])
        else:
            # Continue zooming out
            self.load_background_image(self.image_paths[self.current_image_index])
        
        # Schedule the next zoom-out update
        self.after(10, self.zoom_out_animation)  # Adjust delay for smoother/faster animation

    # FIXME Currently very primitive - improve later if time allows
    def show_instructions(self):
        """Show the instructions overlay."""
        if self.instructions_overlay:
            return  # If overlay is already open, don't create another one

        # Create a semi-transparent overlay using a canvas
        self.instructions_overlay = tk.Canvas(self, bg="black", width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.instructions_overlay.place(x=0, y=0)

        # Add a semi-transparent rectangle to simulate transparency
        self.instructions_overlay.create_rectangle(
            0, 0, self.winfo_screenwidth(), self.winfo_screenheight(),
            fill="black", stipple="gray50"  # Stipple creates a pattern effect to simulate transparency
        )

        # Add instruction text inside the overlay
        instructions_text = """
        Welcome to the Pokémon!

        To get started:
        Select a save file, then press New Game!
        For new players, press New Game and input a username for your save file.

        Once you are in the game:
        Use the arrow keys to move around! 
        Press "I" to see the pokemon in your inventory, and press "Escape" to close it!
        Press "S" to save your game
        Run into a pokemon to attempt to catch it!

        To catch a pokemon:
        Time the pulsing ring so that it matches the gray outline
        You only have 5 pokeballs, so be careful!

        Good luck and have fun!
        """

        label = tk.Label(self.instructions_overlay, text=instructions_text, font=("Arial", 18), bg="black", fg="white", justify="left", padx=20, pady=20)
        label.pack()

        # Add Close button (X) to dismiss the overlay
        close_button = tk.Button(self.instructions_overlay, text="X", font=("Arial", 14), fg="red", command=self.close_instructions)
        close_button.pack(padx=10, pady=10, anchor="ne")

    def close_instructions(self):
        """Close the instructions overlay."""
        if self.instructions_overlay:
            self.instructions_overlay.destroy()
            self.instructions_overlay = None

    def show_saves(self):
        """ Shows window with available save games"""
        if self.saves_overlay:
            return
        self.saves_overlay = tk.Canvas(self, bg="black", width=self.winfo_screenwidth(),
                                              height=self.winfo_screenheight())
        self.saves_overlay.place(x=0, y=0)

        # Add a semi-transparent rectangle to simulate transparency
        self.saves_overlay.create_rectangle(
            0, 0, self.winfo_screenwidth(), self.winfo_screenheight(),
            fill="black", stipple="gray50"  # Stipple creates a pattern effect to simulate transparency
        )
        saves = self.load_saves()
        for save in saves:
            save_button = tk.Button(self.saves_overlay, text=save.name, font=("Arial", 14), fg="black",
                                 command=partial(self.select_save, save))
            save_button.pack(padx=10, pady=10, anchor='center')

        # Add Close button (X) to dismiss the overlay
        close_button = tk.Button(self.saves_overlay, text="X", font=("Arial", 14), fg="red",
                                 command=self.close_saves)
        close_button.pack(padx=10, pady=10, anchor="ne")

    def load_saves(selfs):
        """ Loads all saves from dir below: """
        path = './Saves/'
        return [TrainerSave(path + f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    def loadPokemonData(filePath='PokeList_v3.csv'):
        """ Loads data from pokemon list file """
        with open(filePath, 'r') as csv:
            lines = csv.readlines()
            data = dict([(l.split(',')[1], tuple([e.strip() for e in l.split(',')[1:]])) for l in lines])
        return data

    def select_save(self, save):
        """ Selects Save"""
        print(save.name)
        self.selected_save = save
        self.close_saves()

    def close_saves(self):
        """Close the saves overlay."""
        if self.saves_overlay:
            self.saves_overlay.destroy()
            self.saves_overlay = None

    def start_game(self):
        """
        Starts the catching minigame
        """

        if not self.selected_save.name:
            label = tk.Label(self, text="Please enter your username:")
            username_entry = tk.Entry(self, width=30)
            # Button to submit the username
            submit_button = tk.Button(
                self,
                text="Submit",
                command=lambda: self.set_username(username_entry)
            )
            
            input_label = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.3), anchor="center", window=label)
            input_entry = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.35), anchor="center", window=username_entry)
            input_butn = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.4), anchor="center", window=submit_button)

        else:
            pygame.mixer.music.stop()
            self.quit_game()
            Pokemon_Game.main(self.selected_save)

    def set_username(self, entry_widget):
        """
        Retrieves the username from the entry widget and sets it for the game.
        """
        username = entry_widget.get()
        if username.strip():  # Check if the username is not empty or just spaces
            self.selected_save.set_save_name(username)

        pygame.mixer.music.stop()
        self.quit_game()
        if len(self.selected_save.pokemon_list) == 0:
            pokemon = Pokemon(choice(list(POKEMON_DATA.items()))[1][0].lower())
            print(pokemon.nickname)
            self.selected_save.append_pokemon(pokemon)
        Pokemon_Game.main(self.selected_save)

    def quit_game(self):
        """
        Closes game when quit is pressed
        """
        pygame.mixer.music.stop()
        self.quit()
        self.destroy()

    def on_resize(self, event):
        """Runs when window resized"""
        # Place title image directly on the canvas (no background box)
        self.title_image_id = self.canvas.create_image(self.winfo_screenwidth() // 2, self.winfo_screenheight() // 4, image=self.title)

        # Keep a reference to the image to prevent garbage collection
        self.canvas.image = self.title
        
        start_button_window = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.45), anchor="center", window=self.start_button)
        saves_button_window = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.5), anchor="center", window=self.saves_button)
        quit_button_window = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.6), anchor="center", window=self.quit_button)
        instructions_button_window = self.canvas.create_window(self.winfo_screenwidth() // 2, int(self.winfo_screenheight() * 0.55), anchor="center", window=self.instructions_button)

# Start the menu
if __name__ == "__main__":
    menu = GameMenu()
    menu.mainloop()