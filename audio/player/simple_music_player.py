from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen import MutagenError
from pygame import mixer
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from tkinter import filedialog
from functools import partial


class MusicPlayer( tk.Frame ):
    """
        src https://stackoverflow.com/questions/54081159/how-do-i-link-an-mp3-file-with-a-slider-so-that-the-slider-moves-in-relation-to
        I just added a few modifications that allow to load wav files more easily
    """
    def __init__(self, master):

        super().__init__(master) #initilizes self, which is a tk.Frame
        self.pack()

        # MusicPlayer's Atrributes
        self.master = master     # Tk window
        self.track = None        # Audio file
        self.trackLength = 0  # Audio file length
        self.player = None       # Music player
        self.playBut = None      # Play Button
        self.stopBut = None      # Stop Button
        self.slider = None       # Progress Bar
        self.slider_value = None # Progress Bar value

        # # Call these methods
        # self.get_AudioFile_MetaData( tracktype )
        # self.load_AudioFile()
        self.create_Widgets()


    def get_AudioFile_MetaData( self, path ):
        '''Get audio file and it's meta data (e.g. tracklength).'''
        print( '\ndef get_AudioFileMetaData( self, audiofile ):' )

        try:
                audiofile=path # In current directory
                f = WAVE( audiofile )
        except MutagenError:
            print( "Fail to load audio file ({}) metadata".format(audiofile) )
        else:
            trackLength = f.info.length
        self.track = audiofile
        self.trackLength = trackLength; print( 'self.trackLength',type(self.trackLength),self.trackLength,' sec' )


    def load_AudioFile( self ):
        '''Initialise pygame mixer, load audio file and set volume.'''
        print( '\ndef load_AudioFile( self, audiofile ):' )
        player = mixer
        player.init()
        player.music.load( self.track )
        player.music.set_volume( .25 )

        self.player = player
        print('self.player ', self.player)



    def select_and_load_audio_file(self):
        path = filedialog.askopenfilename(filetypes = (("audio files", "*.wav"), ("All files", "*.*")))
        self.get_AudioFile_MetaData(path)
        self.load_AudioFile()
        self.slider.pack_forget()
        self.slider_value = tk.DoubleVar()

        self.slider = tk.Scale(self, to=self.trackLength, orient=tk.HORIZONTAL, length=700,
                               resolution=0.5, showvalue=True, tickinterval=30, digit=4,
                               variable=self.slider_value, command=self.UpdateSlider)
        self.slider.pack()

    def create_Widgets ( self ):
        '''Create Buttons (e.g. Start & Stop ) and Progress Bar.'''
        print( '\ndef create_Widgets ( self ):' )
        self.playBut = tk.Button( self, text='Play', command=self.Play )
        self.playBut.pack()

        self.stopBut = tk.Button( self, text='Stop', command=self.Stop )
        self.stopBut.pack()


        # load_command = partial(filedialog.askopenfilename, filetypes=(("audio files","*.wav"),("All files","*.*")))
        self.stopBut = tk.Button(self, text='Load', command=self.select_and_load_audio_file)
        self.stopBut.pack()

        self.slider_value = tk.DoubleVar()

        self.slider = tk.Scale( self, to=self.trackLength , orient=tk.HORIZONTAL, length=700,
                                resolution=0.5, showvalue=True, tickinterval=30, digit=4,
                                variable=self.slider_value, command=self.UpdateSlider )
        self.slider.pack()



    def Play( self ):
        '''Play track from slider location.'''
        print('\ndef Play():')
        #1. Get slider location.
        #2. Play music from slider location.
        #3. Update slider location (use tk's .after loop)
        playtime = self.slider_value.get();       print( type(playtime),'playtime = ',playtime,'sec' )
        self.player.music.play( start=playtime ); print( 'Play Started' )
        self.TrackPlay( playtime )


    def TrackPlay( self, playtime ):
        '''Slider to track the playing of the track.'''
        print('\ndef TrackPlay():')
        #1.When track is playing
        #   1. Set slider position to playtime
        #   2. Increase playtime by interval (1 sec)
        #   3. start TrackPlay loop
        #2.When track is not playing
        #   1. Print 'Track Ended'
        if self.player.music.get_busy():
            self.slider_value.set( playtime ); print( type(self.slider_value.get()),'slider_value = ',self.slider_value.get() )
            playtime += 1.0
            self.loopID = self.after(1000, lambda:self.TrackPlay( playtime ) );\
                                               print( 'self.loopID = ', self.loopID )
        else:
            print('Track Ended')


    def UpdateSlider( self, value ):
        '''Move slider position when tk.Scale's trough is clicked or when slider is clicked.'''
        print( '\ndef UpdateSlider():' );       print(type(value),'value = ',value,' sec')
        if self.player.music.get_busy():
            print("Track Playing")
            self.after_cancel( self.loopID ) #Cancel PlayTrack loop
            self.slider_value.set( value )   #Move slider to new position
            self.Play( )                     #Play track from new postion
        else:
            print("Track Not Playing")
            self.slider_value.set( value )   #Move slider to new position


    def Stop( self ):
        '''Stop the playing of the track.'''
        print('\ndef Stop():')
        if self.player and self.player.music.get_busy():
            self.player.music.stop()
            print('Play Stopped')


def ask_quit():
    '''Confirmation to quit application.'''
    if tkMessageBox.askokcancel("Quit", "Exit MusicPlayer"):
        app.Stop()
        if app.player:#Stop playing track
            app.player.quit()  #Quit pygame.mixer
        root.destroy()     #Destroy the Tk Window instance.

        # Note: After initialzing pygame.mixer, it will preoccupy an entire CPU core.
        #       Before destroying the Tk Window, ensure pygame.mixer is quitted too else
        #       pygame.mixer will still be running in the background despite destroying the
        #       Tk Window instance.

if __name__ == "__main__":
    root = tk.Tk()
    #Initialize an instance of Tk window.
    app = MusicPlayer( root)  #Initialize an instance of MusicPlayer object and passing Tk window instance into it as it's master.
    root.protocol("WM_DELETE_WINDOW", ask_quit) #Tell Tk window instance what to do before it is destroyed.
    root.mainloop()