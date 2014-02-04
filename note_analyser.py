#!/usr/bin/env python
import pyaudio
import struct
import numpy as np
import math
import sys

FORMAT = pyaudio.paInt16 
CHANNELS = 2
RATE = 44100
BLOCK_DURATION = 0.15
FRAMES_PER_BLOCK = int(RATE*BLOCK_DURATION)
NORMALIZATION = (1.0/32768.0)

MIN_RMS = 0.015
NOTE_PPRECISION = 20
NOTES = [[440, 'A'], [329.6, 'E'], [261.6, 'C'], [392, 'G']] # ukulele, G tuning


pa = pyaudio.PyAudio()
stream = pa.open(format = FORMAT,
         channels = CHANNELS,
         rate = RATE,
         input = True,
         frames_per_buffer = FRAMES_PER_BLOCK)

def get_rms( block ):
    '''
    http://en.wikipedia.org/wiki/Root_mean_square
    '''
    sample_size = len(block)/CHANNELS
    samples = struct.unpack("%dh"%(sample_size), block )
    sum_squares = sum([math.pow(sample * NORMALIZATION, 2) for sample in samples])

    return math.sqrt( sum_squares / sample_size )

def frequency(block):
    '''
    Does fast fourier transform (fft) and quadratic interpolation on the 
    data sample to find the frequency.
    '''
    data = np.array(struct.unpack("%dh" % (len(block)/CHANNELS), block))
    data = abs(np.fft.rfft(data))**2
    fftmax = data[1:].argmax() + 1

    # quadratic interpolation
    if fftmax != len(data)-1:
        y0, y1, y2 = np.log(data[fftmax-1:fftmax+2:])
        x1 = (y2-y0) * 0.5 / (2*y1 - y2-y0)
        freq = (fftmax+x1) * RATE / FRAMES_PER_BLOCK
    else:
        freq = fftmax * RATE / FRAMES_PER_BLOCK

    return freq

while True:
    try:
        block = stream.read(FRAMES_PER_BLOCK)
        rms = get_rms(block)
        if (rms > MIN_RMS):
            freq = frequency(block)
            for hz, note in NOTES:
                if abs(hz-freq) < NOTE_PPRECISION:
                    sys.stdout.write(note)
                    sys.stdout.flush() # so other proccess can read stdout after each note

    except IOError, e:
        errorcount += 1
        print("(!) Error recording: %s" % (e))