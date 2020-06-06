#VIRTUAL ASSISTANT that can give today's date, and information of a person from wikipedia, all of that through audio(both input and output)

#importing the libraries
import playsound
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
import os
from tkinter import *

root = Tk()
myStr = StringVar()
myStr.set("hi,how may i help you?")

audioFlag = 0

#ignoring all the warnings
#warnings.filterwarnings('ignore')

#record audio and return it as a string
def hearAudio():
    global audioFlag
    #record the audio
    r = sr.Recognizer() #creating a recognizer object
    #open the mic
    with sr.Microphone() as source:
        print("say something")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("done listening")
    #use google's speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print("you said : " + data)
        audioFlag = 0
    except:
        audioFlag = 1
    return data

#take in audio and say it out
def speakAudio(text):

    #talk back with audio
    print(text)

    #convert text to speech
    t2s = gTTS(text=text, lang='en')

    #save the converted audio to a file
    t2s.save('assistantResponse.mp3')

    #play the audio file
    playsound('assistantResponse.mp3')
    os.remove('assistantResponse.mp3')

#this function is for wake word
def wakeWords(text):
    wakeWordList = ['hi computer','okay computer','hey computer','computer']

    text = text.lower()

    #check if text has a wake words
    for phrase in wakeWordList:
        if phrase in text:
            return True

    return False

#function for current date
def getDate():

    now = datetime.datetime.now()
    myDate = datetime.datetime.today()
    weekDay = calendar.day_name[myDate.weekday()]
    monthNum = now.month
    dayNum = now.day

    monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ordinalNums = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                     '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
                     '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
                     '29th', '30th', '31st']

    return 'today is ' + weekDay + ' ' + monthNames[monthNum - 1] + ' the ' + ordinalNums[dayNum - 1]

#random greeting
def greeting(text):

    #greeting inputs
    greetingInputs = ['hi','hey','wassup','hello']

    #greeting responses
    greetingOutput = ['oh hi there', 'hey cutie', 'hello there', "it's good to see you"]

    for word in text.split():
        if word.lower() in greetingInputs:
            return random.choice(greetingOutput) + '.'

    #for no greeting,
    return ''

#getting a person's first and last name through the text
def getPerson(text):

    text = [x.lower() for x in text.split()]
    for i in range(len(text)):
        if i + 3 < len(text) and text[i] == 'who' and text[i+1] == 'is':
            if text[i+3] != 'and':
                return text[i+2] + ' ' + text[i+3]
            else:
                return text[i+2]
    if text[len(text)-3] == 'who' and text[len(text)-2] == 'is':
        return text[len(text)-1]

def driver():
    #record the audio
    print("in")
    global myStr
    myStr.set("listening..")
    print("listening..")
    text = hearAudio()
    print("done listening, in driver")
    if audioFlag == 0:
        response = ''

        if(wakeWords(text)):

            #check for greetings by the user
            response += greeting(text)

            #it is related to date?
            if 'date' in text:
                getDate()
                response += ',' + getDate()

            #did the user say 'who is ..'?
            if 'who is' in text:
                person = getPerson(text)
                print(person)
                wiki = wikipedia.summary(person, sentences=2)
                response += ',' + wiki

            #lets have the assistant to talk
            myStr.set(response)
            speakAudio(response)


myLabel = Label(root,textvariable = myStr)
speakButton = Button(root,text = "click me to talk",command = driver)
myLabel.pack()
speakButton.pack()
root.mainloop()