import numpy as np                    # linear algebra, vector operations, numpy arrays
import matplotlib.pyplot as plt       # allows for plotting
import os
import cv2 as opencv
from scipy.io import wavfile


working_dir = 'numbers1/'
save_dir = 'reduced_images/'
count = 0
path = os.getcwd()

listings = os.listdir(working_dir)
print(f'listing: {listings}')

#graph original file and trimmed file next to each other
for file in listings:

    audio_file = os.path.join(working_dir, file)
    if os.path.isfile(audio_file):

        print(f'IMAGE {count} (filename {audio_file}):')
        # convert the wavfile into its frequency and array of channels
        # int, numpy array consisting of # of channels and data per channel
        amplitude, audio = wavfile.read(audio_file)
        print(f'amplitude: {amplitude}')
        print(f'audio (shape {audio}): {audio}')

        time = np.arange(0, len(audio)) / amplitude
        e_time = max(time, default=1)


        # setup plot
        fig, ax = plt.subplots(figsize=(.32, .32))

        # plot original file
        plt.plot(time, audio, 'blue', alpha=1, label='Original')
        plt.ylim([-20000, 20000])
        plt.xlim([0, 2])

        # commenting out labels for ridiculously tiny images
        '''
        plt.subplots_adjust(hspace=1)
        plt.xlabel('Time (s)')
        plt.ylabel('Sound Amplitude')
        plt.title(f'Original - {e_time:.2f} seconds')
        '''

        plt.savefig(save_dir + file[:-4] + 'r')
        # plt.show()
