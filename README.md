# VideoToAscii
Python Script that turns a video or image into ascii art

  __/\\\\\\\\\\\\_________/\\\\\\\\\______/\\\________/\\\___/\\\\\\\\\\\___/\\\\\\\\\\\\_____________/\\\________/\\\________
   _\/\\\////////\\\_____/\\\\\\\\\\\\\___\/\\\_______\/\\\__\/////\\\///___\/\\\////////\\\__________\/\\\_______\/\\\________
    _\/\\\______\//\\\___/\\\/////////\\\__\//\\\______/\\\_______\/\\\______\/\\\______\//\\\_________\/\\\_______\/\\\________
     _\/\\\_______\/\\\__\/\\\_______\/\\\___\//\\\____/\\\________\/\\\______\/\\\_______\/\\\_________\/\\\\\\\\\\\\\\\________
      _\/\\\_______\/\\\__\/\\\\\\\\\\\\\\\____\//\\\__/\\\_________\/\\\______\/\\\_______\/\\\_________\/\\\/////////\\\________
       _\/\\\_______\/\\\__\/\\\/////////\\\_____\//\\\/\\\__________\/\\\______\/\\\_______\/\\\_________\/\\\_______\/\\\________
        _\/\\\_______/\\\___\/\\\_______\/\\\______\//\\\\\___________\/\\\______\/\\\_______/\\\__________\/\\\_______\/\\\________
         _\/\\\\\\\\\\\\/____\/\\\_______\/\\\_______\//\\\_________/\\\\\\\\\\\__\/\\\\\\\\\\\\/___________\/\\\_______\/\\\___/\\\_
          _\////////////______\///________\///_________\///_________\///////////___\////////////_____________\///________\///___\///__

## This is the README for my video to ascii program

### What is it?

- it's a program (script) that converts a video or image file to a video or image made of ASCII characters.
- examples may be found here.

### How does it work?

- it calculates the average brightness of pixels from each frame and chooses an according character.
- a bright pixel could be represented with " . " and a dark one with " W ".

### How to run?

- install libraries
- run with python

### Libraries

- update pip: $ pip install --upgrade pip
- install the following libraries in your terminal:

$ pip install tk
$ pip install opencv-python
$ pip install progress

### Run with python

- unpack zip, if you haven't already
- from your terminal: navigate to "videoToAscii" folder
- run command: $ python3 main.py

- enter resolution (width) in characters -> default is 150 characters
- select if you want compression

- the finished file will be saved as .html under "videoToAscii/file-to-text", which you can run in your favored webbrowser.
- 
### Keep in mind!

- this program does not contain a "good" compression algorithm, there is a chance of getting a larger output file if you choose to compress it.
- if the file you want to convert contains a lot of same-colored pixels, i.e. a picture of the moon which is mostly black, the compression may work.
- I might add an suitable algorithm later :)
- thanks for trying my program :) David - nov 2022
