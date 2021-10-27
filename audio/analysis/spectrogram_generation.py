import numpy as np
from matplotlib import colors
from matplotlib.backend_bases import MouseButton
from matplotlib.colors import LogNorm
from matplotlib.widgets import Button, RectangleSelector
from numpy.random._examples.cffi.extending import rng
from scipy import fft
from scipy import signal


def synthetic_signal_1():
    fs = 10e3
    N = 1e5
    NFFT = 1024
    amp = 2 * np.sqrt(2)
    noise_power = 0.01 * fs / 2
    time = np.arange(N) / float(fs)
    mod = 500 * np.cos(2 * np.pi * 0.25 * time)
    carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
    noise = rng.normal(scale=np.sqrt(noise_power), size=time.shape)
    noise *= np.exp(-time / 5)
    x = carrier + noise
    return fs,x, NFFT


if __name__ == '__main__':
    from audio.audio_utils import read_audio_file
    import cv2
    import matplotlib.pyplot as plt


    def line_select_callback(eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        rect = plt.Rectangle((min(x1, x2), min(y1, y2)), np.abs(x1 - x2), np.abs(y1 - y2))
        ax.add_patch(rect)


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


    plt.connect('button_press_event', on_click)
    plt.connect('button_release_event', on_click)

    rate, audio_data = read_audio_file('../../tmp_files/StarWars3.wav')
    # rate, audio_data, nfft = synthetic_signal_1()
    ax = plt.subplot()

    frequencies, times, spectrogram = signal.spectrogram(audio_data, rate)

    plt.pcolormesh(times, frequencies, spectrogram, shading='auto')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [ms]')


    axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    bcut = Button(axcut, 'ies', color='red', hovercolor='green')
    toggle_selector.RS = RectangleSelector(ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
    bcut.on_clicked(toggle_selector)
    plt.show()
