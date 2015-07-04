#!/usr/bin/env python
import pygame
import time
from RPi import GPIO
from array import array
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

recorded_note = []

# defining the input pin number
KEY_C = 12
KEY_D = 16
KEY_E = 18
KEY_F = 22
PLAY = 35
RECORD = 37

# defining the output pin number
RED = 36
GREEN = 38
BLUE = 40

# difining the notes' frequency
freq_C = 261.6
freq_D = 293.7
freq_E = 329.6
freq_F = 349.2

#setting up the GPIO as board mode
GPIO.setmode(GPIO.BOARD)

# setting up the input pin for touch button
GPIO.setup(KEY_C, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(KEY_D, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(KEY_E, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(KEY_F, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(PLAY, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(RECORD, GPIO.IN, GPIO.PUD_DOWN)

# setting up the output pin for touch button
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)


# Tone sound generator class. Frequency and volume has to be passed during object creation
class ToneSound(pygame.mixer.Sound):
    def __init__(self, frequency, volume):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


# declaring ToneSound object for respective notes
note_C = ToneSound(frequency = freq_C, volume = 1)
note_D = ToneSound(frequency = freq_D, volume = 1)
note_E = ToneSound(frequency = freq_E, volume = 1)
note_F = ToneSound(frequency = freq_F, volume = 1)

# turn off all the LED
def light_off():
    GPIO.output(RED, False)
    GPIO.output(GREEN, False)
    GPIO.output(BLUE, False)

def wait_for_keydown():
    while not GPIO.input(KEY_C) and not GPIO.input(KEY_D) and not GPIO.input(KEY_E) and not GPIO.input(KEY_F) and not GPIO.input(PLAY) and not GPIO.input(RECORD):
        time.sleep(0.01)

def wait_for_keyup(pin):
    while GPIO.input(pin):
        time.sleep(0.1)

# this function will play the recorded note
def play_note():
    for i, v in enumerate(recorded_note):
        if v[0] is 'B':
            print(v[0], v[1])
            time.sleep(v[1])
        elif v[0] is 'C':
            print(v[0], v[1])
            note_C.play(-1)
            time.sleep(v[1])
            note_C.stop()
        elif v[0] is 'D':
            print(v[0], v[1])
            note_D.play(-1)
            time.sleep(v[1])
            note_D.stop()
        elif v[0] is 'E':
            print(v[0], v[1])
            note_E.play(-1)
            time.sleep(v[1])
            note_E.stop()
        elif v[0] is 'F':
            print(v[0], v[1])
            note_F.play(-1)
            time.sleep(v[1])
            note_F.stop()
            

record_flag = False     # if this flag is true than everything will be recorded in a list


# program entry point
while True:
    start_time = time.time()
    wait_for_keydown()
    diff_time = time.time() - start_time
    if record_flag:
        recorded_note.append(('B', diff_time))
    if GPIO.input(KEY_C):
        start_time = time.time()
        note_C.play(-1)
        wait_for_keyup(KEY_C)
        note_C.stop()
        diff_time = time.time() - start_time
        if record_flag:
            recorded_note.append(('C', diff_time))
    elif GPIO.input(KEY_D):
        start_time = time.time()
        note_D.play(-1)
        wait_for_keyup(KEY_D)
        note_D.stop()
        diff_time = time.time() - start_time
        if record_flag:
            recorded_note.append(('D', diff_time))
    elif GPIO.input(KEY_E):
        start_time = time.time()
        note_E.play(-1)
        wait_for_keyup(KEY_E)
        note_E.stop()
        diff_time = time.time() - start_time
        if record_flag:
            recorded_note.append(('E', diff_time))
    elif GPIO.input(KEY_F):
        start_time = time.time()
        note_F.play(-1)
        wait_for_keyup(KEY_F)
        note_F.stop()
        diff_time = time.time() - start_time
        if record_flag:
            recorded_note.append(('F', diff_time))
    elif GPIO.input(RECORD):
        if record_flag == False:
            recorded_note = []
            print('Recording started!')
        else:
            print('Recording stopped!')
        record_flag = not record_flag
        time.sleep(.5)
        GPIO.output(RED, record_flag)
    elif GPIO.input(PLAY):
        if record_flag:
            record_flag = False
            print('Recording stopped!')
        light_off()
        GPIO.output(GREEN, True)
        print('Playing note!')
        play_note()
        print('Stopped!')
        light_off()