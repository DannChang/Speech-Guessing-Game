# Credits
The project was done by Daniel Chang and Ryan Mei for a final term project in April 2019.

Prototype Drawing:
![image](https://user-images.githubusercontent.com/27746994/111914909-33155a00-8a31-11eb-8e1d-58cbde96f19c.png)

Final Application:
![image](https://user-images.githubusercontent.com/27746994/111914890-2133b700-8a31-11eb-839b-b4b384f76c6b.png)


# INSTRUCTIONS
To get the program running on your computer, 
you must have the following libraries installed via pip

These libraries include:
* tinkter
* wave
* speechrecognition
* os
* numpy
* pyaudio* (must first install 'portaudio.h' via brew install portaudio)

(If for some reason packages cannot be installed, try pip3 install ____)

# CMPT 365 Final Report
## Introduction

  Being able to accurately transcribe speech is powerful, and ubiquitous. So much that,
many big tech companies have started working on their own speech recognition software (e.g.
Google assistant, Alexa, Siri, Bixby, etc). These examples of voice assistants are very good at
identifying what the user asks for, but unable to respond like a human would be able to in a
normal conversation. Therefore, recent developments in AI speech recognition software have
become increasingly important in the future of AI and human-computer interaction domains.

  An example of recent advancements, which inspired us to try and tinker with speech
recognition, is with the use of Google Assistant. This was introduced as Google Duplex, which
has a call screening feature, and allows the user to see the interaction between Google
assistant (computer-to-human interaction) and the caller (human-to-computer interaction) in
real-time, by transcribing the entire conversation.

  We realized there are many applications, with today’s technology to apply speech
recognition in. For example, even without the use of AI or voice assistants, having the ability to
transcribe text accurately have its practical use in day-to-day life. A student may use a
transcription software to assist in taking notes, then the interviewer may use speech
recognition to convert notes from a video interview to a text-based one. Further, It could be
used as an automatic subtitle generator (closed captions) for movies and TV shows, or even
help a person learn a foreign language.

  Since the course is based solely around multimedia and its different constituents, we
thought it would be interesting to explore digital signal processing exclusively. The final project
inspired us to explore specific domains in audio processing, which draw on relevant concepts
taught in class (fourier transform, quantization, encoding, etc).

## Project Description
### How to Play
  At the start of the game, the players are greeted with a ‘Start’ button to start the game.
Upon pressing ‘Start’, the game asks for the player’s names in turn, starting with player 1.
Throughout the game, players will be prompted a ‘talk!’ text, to indicate the recording of audio
. First round of recordings include asking for the player names, then the program will ask for
player 1’s questions, and will modify the audio to store both the original and the modified in a
WAV file. The same will apply for player 2. Once all the questions have been recorded, the main
setup portion of the game is complete. The game will now take turns playing each of the
questions from the modified WAV files and the players will take turns guessing what the
original question is. Each correct answer is worth 1 point, and the player with the most points
at the end wins.

### Description
  Our project is based off of three main concepts: (1) transcription of speech-to-text, (2)
frequency modification of audio files, and (3) recording/playback of WAV files. (1) Transcription
of speech-to-text is implemented through the Speech Recognition library in Python 3, which
allow us to use cloud databases. Included in the library is an ambient filter, which sifts through
the recording for erroneous sounds in a poorly recorded audio clip. (2) Using FFT found in
Numpy, we were able to manipulate the pitch of the frequencies in a given WAV audio clip.
From there, we can recompile the modified WAV file in preparation for playback. (3) Finally, the
modified file will be saved and played for the player to decipher.

  As mentioned before, the transcription was created with the help of the Speech
Recognition library [1], and the recording and playing of WAV files was created using a
combination of Numpy, Pyaudio, and Wave libraries. We implemented two ways of
transcribing, one is from a recorded file (Wave), and the other is directly from the microphone
(Speech Recognition). The first way was demonstrated when the player records the sentence.
We record the sentence into a WAV file on the computer, and then transcribe it into words
from the WAV file. We needed to record the initial guess because we will manipulate it using a
filter before playing it for the second player to guess. The second way was demonstrated during
the guessing phase. Since there was no need to record the guess, we directly transcribe from
the microphone.

  Recording was implemented in single-channel, at a sampling rate of 44100 with 1024
chunks. Using pyaudio, we record for a specified number of seconds, and then write the
recording to a wav file on the local machine. Playback of the file is similar. Using pyaudio, we
open up an audio stream and play the recording without the need of an audio playback
application such as Windows Media Player.
Modifying the audio made use of the Fourier transform. Given the input file, which is
the file we recorded, we break down the file into ‘frames’ and process each frame individually
in a for loop. For each frame, we first combine the left and right channels (if it exists), then
perform the Fourier transform. After the transform, we shift the frequencies and then perform
the inverse Fourier transform and write the new file onto the disk of the local machine with a
new name.

  The GUI for our program was developed using the Tkinter library. To display the
necessary information of the game, we included three main sections in our GUI, one each for
the two player, and one central section for game messages (i.e. to indicate stage of game).
Finally, the GUI was developed using the Tkinter library. The necessary information to display in
the game includes three main sections in our GUI, one each for the two player, and one central
section for game messages (i.e. to indicate stage of game).

## Experimental Results
### Nuts and Bolts of Frequency Manipulation via Fast Fourier Transform
![image](https://user-images.githubusercontent.com/27746994/111915032-a8812a80-8a31-11eb-83b9-6aa4511eb184.png)

  FFT allows us to use DFT algorithmically and convert a signal to a frequency domain as
represented in the graphs below. With this implementation, we are able to get an O(n log n)
runtime to manipulate the frequencies and use inverse FFT to convert it back to a periodic
signal [9]. Breaking down e−j2πk/N , we have Euler’s formula so that we could manipulate the
sinusoid components. Pitch adjustment happens when we take the periodic waves and shift it
by either shortening or lengthening the frequencies to give us a modified WAV file. As shown in
the graph, we have pitch adjusted the waveform by lengthening its amplitude, so that a higher
pitch sound is yielded. As a result, we sum the frequency bins again so that it can be converted
back into period signals through inverse FFT.

### Working with the GUI
  While integrating the game into the Tkinter GUI, we noticed a few major issues. When
Tkinter’s GUI is prompted, the program will not update while the ‘main game’ is running on the
console. This would in effect cause the program to be seemingly unresponsive. Our solution
was to periodically call a function to update the GUI, so that the counters for turns and points
will be updated. However, while this stops the program from appearing as if it had crashed, it is
not an elegant solution.

### Working with Speech Recognition (Library)
  In our project, we mainly make use of Google’s Speech Recognition API, and although it
is excellent at identifying complete sentences, when the player only says a short phrase such as
their name, the API has a pretty high chance of identifying it as the wrong word. We believe this
is caused by the lack of context. In a full sentence, a few of the words could be deduced by
context, but in a short phrase or a single word, there isn’t enough information to correct any
mistakes. In addition, when a number is being transcribed, sometimes the API would return the
number in a numeric form such as “1” but other times it would return it as a word such as
“one”. This would cause issues when identifying the sentences during the scoring phase of the
game. Another issue is the background noise and how well the player articulates each word.
When a phrase is spoken in a loud environment or it is not articulated well enough, the
transcription is not accurate. Additionally, Google’s API only allows up to a maximum number
of requests up to 50. To get around this, we added Bing’s API to use if we couldn't connect to
Google. Aside from these issues, the main drawback to speech recognition softwares is the
need for an internet connection.

### Working with Audio Processing
  When researching about audio manipulation, one of the first things that came up was
the Fourier Transform, which breaks down a waveform into its individual constituent
frequencies. At first, we wanted to implement the transform ourselves, similar to implementing
the JPEG encoding for Assignment 2. This ended up being scrapped due to the slow processing
speed of Python that we discovered during the JPEG encoding assignment, and that it would
take too much time away from implementing other features we wanted in our game such as
modifying the recorded voice before playing it for the other user to guess. In the end, we
decided to make use of numpy’s Fast Fourier Transform (FFT) (to transform AC to DC) and the
inverse (iFFT) functions (to transform DC to AC).

  After we modified the recording, we realized that it was still clear enough to recognize
the original sentence without much effort. After playing around with a few values, we learned
that if we shifted the frequencies too much, there was a lot of reverb. We ended up sticking
with a value that still sounds noticeably different from the original recording while keeping the
reverb to a minimum.

## Process Documentation
#### March 11, 2019
* Narrowed idea down to audio manipulation after feedback from Professor Ze-Nian and
TA
* Started playing with WAV files in Python to get high level understanding of what’s going
on
* Ended with creation of Google docs to layout and brainstorm for the following week for
work
#### March 14, 2019
* Figured that the manipulation of audio files required for FFT and quantization
  * Defer this task as our core learning opportunity, once we liftoff
* Implement existing speech recognition libraries to play around with to get the project
started (prototype inspired)
####March 25, 2019
* Both successfully finished their part in game and gui development
* Core game consists of:
  * Many library packages
* GUI consists of:
  * Interactive responses for user
#### March 27, 2019
* To implement both GUI + game
  * Problem: cannot run simultaneously
    * Widgets in Tkinter GUI does not update as user is prompted a question (read-in from cmd shell)
  * Solution: run a timed event (after & update) manager, which updates the bash and GUI intermittently
#### March 29, 2019
* Added pitch adjustment function
  * Splits into left and right channel
  * Fast fourier transform
  * Shift frequency values
  * Inverse fourier transform
  * Combine
  * Output file
* Language + libraries result in very slow encoding/decoding times
  * May be difficult to do live audio manipulation
#### April 3, 2019
* Consolidating last bits-ish features/components to the game
* Organizing document to set up for paper and to do for the rest of the week before demo
* Decided to fully make the visualizer work by FRiday
#### April 6, 2019
* Game stalls when awaiting user input -> appears as unresponsive
* Continues as normal when next user input is received

## Conclusion
  Overall, the approach to this final project is a demonstration of certain concepts taught in class,
with a different angle. Instead of using DCT, we used FFT to draw individual frequencies from
compounded analog frequencies. We learned that our human perception of audio ranges from
20 Hz to 20 KHz, as a parallel to the human limitations to color perception taught in class. As in,
we are able to utilize such information for compression of audio files. Further, the sampling
rate of a frequency is a determiner for the quality of the audio (kind of like frames per second
for video).

  Our conception was to implement what we have learned in a concise program. In summary, the
game reads in analog signals from the microphone, transcribes the recorded file into text,
manipulate the recorded file, and playback for the user to guess. Given the time for the project,
this is a barebone for many iterations, which could be better and more robust.

## Discussion
  As this is an introductory course to multimedia, we are limited in wielding all of its tools.
Further applications of this project may be applied to signal processing and machine learning
for speech recognition. In the field of AI, current technologies are narrow in practicality and
additional research in this field would refine human-computer interactions. Language is
ambiguous and continues to evolve as cultures adapt new and trendier words. An area of
interest would be to look at the physical symbol system we use for language and how it applies
to human cognition and thus computer interaction. The closer we get to understanding human
cognition and language production/comprehension, the closer we would get to a seamless
human-to-computer interaction.

## References
[1]R. Python, "The Ultimate Guide To Speech Recognition With Python – Real Python",
Realpython.com , 2019. [Online]. Available:
https://realpython.com/python-speech-recognition/. [Accessed: 08- Apr- 2019].
[2]"Sound Pattern Recognition with Python", Medium , 2019. [Online]. Available:
https://medium.com/@almeidneto/sound-pattern-recognition-with-python-9aff69edce5d.
[Accessed: 08- Apr- 2019].
[3]"Machine Learning is Fun Part 6: How to do Speech Recognition with Deep Learning",
Medium , 2019. [Online]. Available:
https://medium.com/@ageitgey/machine-learning-is-fun-part-6-how-to-do-speech-recognition
-with-deep-learning-28293c162f7a. [Accessed: 08- Apr- 2019].
[4]"Let's Build an Audio Spectrum Analyzer in Python! (pt. 3) Switching to PyQtGraph",
YouTube , 2019. [Online]. Available: https://www.youtube.com/watch?v=RHmTgapLu4s.
[Accessed: 08- Apr- 2019].
[5]"Let's Build an Audio Spectrum Analyzer in Python! (pt. 1) the waveform viewer.", YouTube ,
2019. [Online]. Available: https://www.youtube.com/watch?v=AShHJdSIxkY. [Accessed: 08-
Apr- 2019].
[6]"Getting Started with Audio Manipulation in Python", CSHorde , 2019. [Online]. Available:
https://cshorde.wordpress.com/2014/09/05/start-audio-in-python/. [Accessed: 08- Apr- 2019].
[7]"Audio Signals in Python", Inspiration Information , 2019. [Online]. Available:
http://myinspirationinformation.com/uncategorized/audio-signals-in-python/. [Accessed: 08-
Apr- 2019].
[8] D. Reshetnikov, R. Smith and N. Scozzaro, "Python change pitch of wav file", Stack Overflow ,
2019. [Online]. Available:
https://stackoverflow.com/questions/43963982/python-change-pitch-of-wav-file. [Accessed:
09- Apr- 2019].
[9] “Fast Fourier Transform”, Wikipedia , 2019. [Online]. Available:
https://en.wikipedia.org/wiki/Fast_Fourier_transform [Accessed 09- Apr- 2019].
