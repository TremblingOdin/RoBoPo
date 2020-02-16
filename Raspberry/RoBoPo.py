#!/usr/bin/python
#
#     RoBoPo.py 2/15/2020
#
#     GPIO15 (board 10)
#     GPIO18 (board 12)
#     GPIO23 (board 16)
#     GPIO24 (board 18)
#
#   Written by Kayvan Ehteshami
#   TremblingTitan

import os
import random
import RPi.GPIO as gpio
import serial
import subprocess
import threading
import time

testPIN = 10
v1PIN = 12
v2PIN = 16
v3PIN = 18
ledPIN = 40

#this is needed to prevent the python from trying to run 2 or 3 files at a time
flag= 1

test = "../Poems/Test.txt"
v1 = "../Poems/So I became a Robot.txt"
v2 = "../Poems/I have no name.txt"
v3 = "../Poems/I saw a flower.txt"

voices = ["slt", "awb", "rms"]
vowel = ["a", "e", "i", "o", "u", "y"]

port = None

def setup():
    global port
    port = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    #on button release
    gpio.setup(testPIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    gpio.setup(v1PIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    gpio.setup(v2PIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    gpio.setup(v3PIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    gpio.setup(ledPIN,gpio.OUT)
    flag_flip()

def flag_flip():
    global flag
    if flag != 0:
        flag = 0
        gpio.output(ledPIN,gpio.HIGH)
    elif flag == 0:
        flag = 1
        gpio.output(ledPIN,gpio.LOW)


def syllables(word):
    syllableList = []
    start = 0
    stop = 0
    length = len(word)
    lastCharConst = False
    firstSyll = True
    for i in range(0,length):
        if word[i] not in vowel:
            lastCharConst = True
        elif word[i] in vowel and lastCharConst == True:
            stop = i + 1
            if i < length and not firstSyll:
                syllableList.append(word[start:stop])
                start = i
            elif i == length and not firstSyll:
                syllableList.append(word[start:i])
                start = i
            lastCharConst = False
            firstSyll = False
    if start < length:
        syllableList.append(word[start:length])
    return syllableList


def first_syllable(word):
    syllableList = syllables(word)
    fSyllable = syllableList[0]
    return fSyllable

def serial_thread(name):
    global port
    while flag == 1:
        port.write("1")
        pause = random.uniform(0.4,1)
        time.sleep(pause)
        port.write("0")

def read_poem(poemName):
    global flag
    
    mouthMove = threading.Thread(target=serial_thread,args=(1,))
    mouthMove.start()
    with open(poemName) as f:
        for line in f:
            line.rstrip()
            voice = random.randint(0,2)

            newLine = ""

            #for word in line.split(" "):
            #    newWord = word
            #    stutter = random.randint(-20,3)
            #    if stutter > 0:
            #        stutChar = first_syllable(word)
            #        newWord = ((stutChar + "-") * stutter) + word
            #    newLine = newLine + newWord + " "
            
            #print(newLine)
            #command = "flite --setf duration_stretch=1.5 -voice " + voices[voice] + " -t \"" + newLine  + "\""
            dur = random.uniform(1,1.4)
            pitch = random.randint(0,200)

            command = "flite --setf duration_stretch="+str(dur)+" int_f0_target_mean="+str(pitch)+" -voice "+ voices[voice] + " -t \"" + line + "\""
            
            os.system(command)
    flag_flip()
    mouthMove.join()

def test_press(channel):
    global flag
    if flag == 0:
        flag_flip()
        fileName = test
        read_poem(fileName)

def v1_press(channel):
    global flag
    if flag == 0:
        flag_flip()
        fileName = v1
        read_poem(fileName)

def v2_press(channel):
    global flag
    if flag == 0:
        flag_flip()
        fileName = v2
        read_poem(fileName)

def v3_press(channel):
    global flag
    if flag == 0:
        flag_flip()
        fileName = v3
        read_poem(fileName)

if __name__ == '__main__':
    setup()

    #on button release raise event
    gpio.add_event_detect(testPIN, gpio.RISING, callback=test_press, bouncetime=300)
    gpio.add_event_detect(v1PIN, gpio.RISING, callback=v1_press, bouncetime=300)
    gpio.add_event_detect(v2PIN, gpio.RISING, callback=v2_press, bouncetime=300)
    gpio.add_event_detect(v3PIN, gpio.RISING, callback=v3_press, bouncetime=300)

    while 1:
        time.sleep(50)
