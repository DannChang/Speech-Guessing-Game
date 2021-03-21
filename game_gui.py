#CMPT365 Final Project: Speech Synthesizer Game GUI

#Ryan Mei (301281466) && Daniel Chang (301224355)

#rymei@sfu.ca && dschang@sfu.ca

#CMPT 365 D100

#April 2019

##############################################################

# TODO: Entry box for both players and the middle frame for printing out console info
# -include a messagebox that counts down for the user to read in information

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import time
import random
import pyaudio
import wave
import speech_recognition as sr
import os
import numpy as np

# Global Variables
global p1_points
global p2_points
global player_turn
global roundCount
global CONSOLE_MSG
global start
TRIES = 3
ROUNDS = 1
RECOGNIZER = sr.Recognizer()
SPEECH = sr.Microphone()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

def update_msg(msg):
    global CONSOLE_MSG
    CONSOLE_MSG.set(msg)
    root.update()
    time.sleep(2)

def update_p1_points(points):
    points = "Points: " + str(points)
    global p1_points
    p1_points.set(points)
    root.update()

def update_p2_points(points):
    points = "Points: " + str(points)
    global p2_points
    p2_points.set(points)
    root.update()

def update_turn(turn):
    global player_turn
    if (turn ==1):
        player_turn.set("Player 1's Turn")
    else:
        player_turn.set("Player 2's Turn")
    root.update()

def update_round(count):
    global roundCount
    roundCount.set(count)
    root.update()

def update_p1(msg):
    global text_result_one
    text_result_one.insert(END, msg)
    text_result_one.insert(END, '\n')
    root.update()

def update_p2(msg):
    global text_result_two
    text_result_two.insert(END, msg)
    text_result_two.insert(END, '\n')
    root.update()


def transcribe(file):
    #Transcribe from speech using a Recognizer

    # if not( isinstance(recognizer, sr.Recognizer) and isinstance(speech, sr.Microphone)):
    #     print("error with recgonizer")
    #     return
    if not isinstance(RECOGNIZER, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(SPEECH, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    for i in range(TRIES):
        #try 3 tiems to transcribe
        print("talk!")
        CONSOLE_TEXT.set("Talk!")
        root.update()
        #start recording
        if file is not None:
            source = sr.AudioFile(file)
            with source as data:
                RECOGNIZER.adjust_for_ambient_noise(data)
                audio = RECOGNIZER.listen(data)
        else:
            with SPEECH as data:
                RECOGNIZER.adjust_for_ambient_noise(data)
                audio = RECOGNIZER.listen(data)
        result = {"success": True, "error": None, "transcription": None}

        try:
            result["transcription"] = RECOGNIZER.recognize_google(audio)
            break
        except sr.RequestError:
            print("google didnt work")
            try:
                print("bing")
                result["transcription"] = RECOGNIZER.recognize_bing(audio)
                break
            except sr.RequestError:
                print("RequestError")
                result["success"] = False
                result["error"] = "Could not connect to API, try again.."
            except sr.UnknownValueError:
                print("UnknownValueError")
                result["error"] = "Could not transcribe into words..."
        except sr.RequestError:
            print("RequestError")
            result["success"] = False
            result["error"] = "Could not connect to API, try again.."
        except sr.UnknownValueError:
            print("UnknownValueError")
            result["error"] = "Could not transcribe into words..."
    if (result["transcription"] is not None):
        msg = ("You said: " + result["transcription"])
    else:
        msg = ""
    CONSOLE_TEXT.set(msg)
    root.update()
    time.sleep(2)
    return result



def record(file_name):
    # print(p.get_default_input_device_info())
    p = pyaudio.PyAudio()
    CONSOLE_TEXT.set("talk!")
    root.update()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
        data= stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def play(file_name):
    p = pyaudio.PyAudio()
    wf = wave.open(file_name, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()


def modify(file_name):
    input_file = wave.open(file_name, 'r')
    # Set the parameters for the output file.
    par = list(input_file.getparams())
    par[3] = 0  # The number of samples will be set by writeframes.
    par = tuple(par)
    output_name = file_name[:-4] + '_modified.wav'
    output_file = wave.open(output_name, 'w')
    output_file.setparams(par)
    fr = 20
    sz = input_file.getframerate()//fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = int(input_file.getnframes()/sz)  # count of the whole file
    shift = 100//fr  # shifting 100 Hz
    for num in range(c):
        da = np.fromstring(input_file.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2]  # left and right channel
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf, rf = np.roll(lf, shift), np.roll(rf, shift)             #'roll' aka shift the values
        lf[0:shift], rf[0:shift] = 0, 0
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)                 #inverse fourier transform
        ns = np.column_stack((nl, nr)).ravel().astype(np.int16)     #combining the two channels
        output_file.writeframes(ns.tostring())
    input_file.close()
    output_file.close()

def main_game():
    global start
    start = False
    global CONSOLE_MSG
    while start == False:
        root.update()
    global name1, name2
    p1_score = 0
    p2_score = 0
    # Start of Game
    update_msg("Starting game..")
    update_msg("Player 1, what is your name?")
    update_turn(1)
    p1 = transcribe(None)
    msg = "Hello, " + p1["transcription"]
    update_p1(msg)
    update_msg("Player 2, what is your name?")
    update_turn(2)
    p2 = transcribe(None)
    msg = "Hello, " + p2["transcription"]
    update_p2(msg)
    msg = "Player 1: " + p1["transcription"] + "Player 2: " + p2["transcription"]
    update_msg(msg)

    #Setup
    p1_questions = [None] * (ROUNDS+1)
    p2_questions = [None] * (ROUNDS+1)
    for i in range(1, ROUNDS+1):
        update_turn(1)
        msg = "Player 1, please say question: " + str(i)
        update_msg(msg)
        file_name = "p1_questions_" + str(i) + '.wav'
        record(file_name)
        modify(file_name)
        #transform
        p1_questions[i] = transcribe(file_name)
    for i in range(1, ROUNDS+1):
        update_turn(2)
        msg = "Player 2, please say question: " + str(i)
        update_msg(msg)
        file_name = "p2_questions_" + str(i) + '.wav'
        record(file_name)
        modify(file_name)
        p2_questions[i] = transcribe(file_name)

    #Main Game
    for i in range(1, ROUNDS+1):
        update_turn(2)
        file_name = "p1_questions_" + str(i) + '_modified.wav'
        play(file_name)
        modify(file_name)

        update_msg("Guess what Player1 said!")
        #play p2_questions[i]
        p1_guess = transcribe(None)

        if (p1_guess == p1_questions[i]):
            update_p2("CORRECT!")
            p2_score = p2_score + 1
            p2_points = p2_score
            update_p2_points(p2_points)
        else:
            update_p2("WRONG!")

        update_turn(1)
        file_name = "p2_questions_" + str(i) + '_modified.wav'
        play(file_name)
        update_msg("Guess what Player2 said!")
        p2_guess = transcribe(None)
        msg = "your guess: " +  str(p2_guess["transcription"])
        print(msg)
        msg = "actual: " + str(p2_questions[i])
        print(msg)
        if (p2_guess == p2_questions[i]):
            update_p1("CORRECT!")
            p1_score = p1_score + 1
            p1_points = p1_score
            update_p1_points(p1_points)
        else:
            update_p1("WRONG!")

    update_msg("GAME OVER")
    if (p1_score > p2_score):
        update_p1("YOU WIN!")
    elif (p2_score > p1_score):
        update_p2("YOU WIN!")
    else:
        update_p1("TIED!")
        update_p2("TIED!")





class Feedback:
    def __init__(self, master):

        global start
        start = False
        global CONSOLE_MSG
        CONSOLE_MSG = StringVar()
        global CONSOLE_TEXT
        CONSOLE_TEXT = StringVar()
        CONSOLE_TEXT.set("Press Start!")
        global p1_points
        p1_points = StringVar()
        p1_points.set("Points: 0")
        global p2_points
        p2_points = StringVar()
        p2_points.set("Points: 0")
        global player_turn
        player_turn = StringVar()
        global roundCount
        roundCount = StringVar()
        global text_result_one
        global text_result_two
        master.title('Fizzler the Speech Jumbler Game')
        master.configure(background = '#e1f1d5')
        #master.resizable(False,False)

        # Stylization
        # self.style = ttk.Style()
        # self.style.configure('TLabel', font = ('Arial', 13))
        # self.style.configure('TButton', font = ('Arial', 14))
        # self.style.configure('Header.TLabel', font = ('Arial', 13, 'bold'))
        # self.style.configure('Header.TLabelframe', font = ('Arial', 13, 'bold'))

        # Function for updating counters
        def showValue(self):
            p1_points = 0
            p2_points = 0
            player_turn = 0
            roundCount = 0


        # Player One Panel and Scoring
        self.p1Frame = ttk.LabelFrame(master, height = 400, width = 250,
                                       text = "Player 1")
        self.p1Frame.pack(side = LEFT, anchor = N)
        text_result_one = Text(self.p1Frame, width=20, height=10)
        text_result_one.grid(row = 0)

        ttk.Label(self.p1Frame, textvariable = p1_points).grid(row = 1)



        # Middle frame initialization
        self.frame_middle = ttk.Frame(master)
        self.frame_middle.pack(side = LEFT, anchor = N)
        self.frame_middle.config(height = 300, width = 200)
        self.frame_middle.config(relief = RIDGE)
        self.frame_middle.config(padding = (15, 15))

        # Audio Analyzer
        # TODO: replace counters in format, color player accordingly
        roundCount = 0
        ttk.Label(self.frame_middle,
                  textvariable = CONSOLE_MSG).grid(row = 0, column = 0)
        ttk.Label(self.frame_middle,
                  textvariable = player_turn).grid(row = 1, column = 0)
        # ttk.Label(self.frame_middle,
        #           text = "Round starts in {}".format('3'),
        #           style = 'TLabel').grid(row = 1, column = 0, pady = 10)

        ttk.Label(self.frame_middle,
                  textvariable = CONSOLE_TEXT).grid(row = 2, column = 0)



        # Button to start game TODO: link command to main game
        ttk.Button(self.frame_middle, text = 'Start', command  = self.start).grid(row = 7, pady = 10)


        # Player Two Panel and Scoring
        self.p2Frame = ttk.LabelFrame(master, height = 400, width = 250,
                                       text = "Player 2")
        self.p2Frame.pack(side = LEFT, anchor = N)
        text_result_two = Text(self.p2Frame, width=20, height=10)
        text_result_two.grid(row = 0)
        ttk.Label(self.p2Frame, textvariable = p2_points).grid(row = 1)

    def start(self):
        global start
        print("start")
        start = True




root = Tk()
root.geometry('600x250')
feedback = Feedback(root)
root.after(1000, main_game)
root.mainloop()
