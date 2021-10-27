import numpy as np
import tkinter as tk
from matplotlib import colors
from matplotlib.backend_bases import MouseButton
from matplotlib.colors import LogNorm
from matplotlib.widgets import Button, RectangleSelector
from numpy.random._examples.cffi.extending import rng
from scipy import fft
from scipy import signal
from audio.audio_utils import read_audio_file
import matplotlib.pyplot as plt

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)



def line_select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    rect = plt.Rectangle((min(x1, x2), min(y1, y2)), np.abs(x1 - x2), np.abs(y1 - y2))
    line_select_callback.ax.add_patch(rect)


def toggle_selector(event):
    print(' Key pressed.')
    if toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    elif not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

def on_click(event):
    if event.button is MouseButton.LEFT:
        x, y = event.x, event.y

        print(x,y)
    return event.x, event.y

def spectrogram(current_audio_file_path):
    # fig = Figure(figsize=(5, 5),
    #              dpi=100)
    # plot1 = fig.add_subplot(111)
    rate, audio_data = read_audio_file(current_audio_file_path)
    plt.connect('button_press_event', on_click)
    plt.connect('button_release_event', on_click)
    frequencies, times, spec = signal.spectrogram(audio_data, rate)
    plt.pcolormesh(times, frequencies, spec, shading='auto')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [ms]')
    # axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    # rectangle_selector = Button(axcut, 'Select freq', color='red', hovercolor='green')
    # line_select_callback.ax = ax
    # spectrogram.RS = RectangleSelector(ax, line_select_callback,
    #                                        drawtype='box', useblit=True,
    #                                        button=[1, 3],  # don't use middle button
    #                                        minspanx=5, minspany=5,
    #                                        spancoords='pixels',
    #                                        interactive=True)
    # rectangle_selector.on_clicked(toggle_selector)

class SpectrogramPlot(tk.Frame):
    """
        src https://stackoverflow.com/questions/54081159/how-do-i-link-an-mp3-file-with-a-slider-so-that-the-slider-moves-in-relation-to
        I just added a few modifications that allow to load wav files more easily
    """
    def __init__(self, master, title, current_audio_file_path):
        super().__init__(master)  # initilizes self, which is a tk.Frame
        self.master.title(title)
        # self.master.geometry("500x500")
        self.pack()
        self.current_audio_file_path = current_audio_file_path
        spectrogram(current_audio_file_path)
        canvas = FigureCanvasTkAgg(plt.gcf(),
                                   master=self.master)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                       master)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

