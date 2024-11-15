import tkinter as tk
import subprocess
import pygame #! pygame intalled from CL

class GameMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Pokémon Game Menu")
        self.geometry("400x300")  # Set the window size

        # Label and button setup
        label = tk.Label(self, text="Welcome to the Pokémon Catching Game!", font=("Arial", 16))
        label.pack(pady=20)

        start_button = tk.Button(self, text="Catch a Pokémon!", font=("Arial", 14), command=self.start_game)
        start_button.pack(pady=10)

        quit_button = tk.Button(self, text="Quit", font=("Arial", 14), command=self.quit_game)
        quit_button.pack(pady=10)

        pygame.mixer.init()
        pygame.mixer.music.load("Pokemon-Assets/Sounds/Music/Background.mp3")  # Plays music
        pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

    def start_game(self):
        """
            Starts the catching minigame
        """
        pygame.mixer.music.stop()
        # Call the Pokémon Catching Minigame script
        subprocess.run(["python", "Catch-Minigame.py"])  # Runs the minigame file

    def quit_game(self):
        """
            Closes game when quit is pressed
        """
        self.quit()
        self.destroy()

# Start the menu
if __name__ == "__main__":
    menu = GameMenu()
    menu.mainloop()
