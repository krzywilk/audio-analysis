from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen import MutagenError
from pygame import mixer
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from tkinter import filedialog
from functools import partial


def get_audio_metadata(path):
    '''Get audio file and it's meta data (e.g. track_length).'''
    f = None
    try:
        f = WAVE(path)
    except MutagenError:
        print("Fail to load audio file ({}) metadata".format(path))
    return f


class MusicPlayer(tk.Frame):
    """
        src https://stackoverflow.com/questions/54081159/how-do-i-link-an-mp3-file-with-a-slider-so-that-the-slider-moves-in-relation-to
        I just added a few modifications that allow to load wav files more easily
    """
    def __init__(self, master, title):
        super().__init__(master)  # initilizes self, which is a tk.Frame
        self.master.title(title)
        self.pack()

        # MusicPlayer's Atrributes
        self.master = master  # Tk window
        self.track = None  # Audio file
        self.track_length = 0  # Audio file length
        self.player = None  # Music player
        self.play_button = None  # Play Button
        self.stop_button = None  # Stop Button
        self.slider = None  # Progress Bar
        self.slider_value = None  # Progress Bar value
        self.player = mixer
        self.create_widgets()

    def close_windows(self):
        self.master.destroy()

    def load_audio(self, path):
        """Initialise pygame mixer, load audio file and set volume."""
        self.current_audio_file_path = path
        self.player.init()
        self.player.music.load(path)
        self.player.music.set_volume(.25)

    def create_widgets(self):
        """Create Buttons (e.g. Start & Stop ) and Progress Bar."""
        self.play_button = tk.Button(self, text='Play', command=self._play)
        self.play_button.pack()

        self.stop_button = tk.Button(self, text='Stop', command=self._stop)
        self.stop_button.pack()

        self.stop_button = tk.Button(self, text='Load', command=self._select_and_load_audio_file)
        self.stop_button.pack()

        self.slider_value = tk.DoubleVar()

        self.slider = tk.Scale(self, orient=tk.HORIZONTAL, length=700,
                               resolution=0.5, showvalue=True, tickinterval=30, digit=4,
                               variable=self.slider_value, command=self._update_slider)
        self.slider.pack()

    # widgets functions
    def _select_and_load_audio_file(self):
        path = filedialog.askopenfilename(filetypes=(("audio files", "*.wav"), ("All files", "*.*")))
        metadata = get_audio_metadata(path)
        self.load_audio(path)
        self.slider.pack_forget()
        self.slider_value = tk.DoubleVar()

        # TODO: refresh scale without recreating
        self.slider = tk.Scale(self, to=metadata.info.length, orient=tk.HORIZONTAL, length=700,
                               resolution=0.5, showvalue=True, tickinterval=30, digit=4,
                               variable=self.slider_value, command=self._update_slider)
        self.slider.pack()

    def _play(self):
        """Play track from slider location."""
        playtime = self.slider_value.get();
        self.player.music.play(start=playtime);
        self._track_play(playtime)

    def _track_play(self, playtime):
        if self.player.music.get_busy():
            self.slider_value.set(playtime);
            playtime += 1.0
            self.loopID = self.after(1000, lambda: self._track_play(playtime))

    def _update_slider(self, value):
        """Move slider position when tk.Scale's trough is clicked or when slider is clicked."""
        if self.player.music.get_busy():
            self.after_cancel(self.loopID)  # Cancel PlayTrack loop
            self.slider_value.set(value)  # Move slider to new position
            self._play()  # Play track from new postion
        else:
            self.slider_value.set(value)  # Move slider to new position

    def _stop(self):
        '''Stop the playing of the track.'''
        if self.player and self.player.music.get_busy():
            self.player.music.stop()
