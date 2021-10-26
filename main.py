
import tkinter as tk
from gui.master_view import MasterView
from gui.player.simple_music_player import MusicPlayer

def init_views():
    views = [
        ("Simple player", MusicPlayer, "Simple player")
    ]
    return views


if __name__ == "__main__":
    root = tk.Tk()
    #Initialize an instance of Tk window.
    app = MasterView(root, init_views())
    root.mainloop()