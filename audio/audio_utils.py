from scipy.io import wavfile


def read_audio_file(file_path):
    rate, data = wavfile.read(file_path)
    return rate, data