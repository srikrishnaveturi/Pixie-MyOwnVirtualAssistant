# say hi to pixie,your own python virtual assistant
# ask her what date it is today,
# or ask her who is spiderman?, i would say it's but whatever
# you can also ask her for today's weather in your city

#importing the libraries

import playsound
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import datetime
import calendar
import random
import wikipedia
import os
from tkinter import *
import spacy
import requests

#nlp is for named entity recognition,myStr is the string that will be printed on the GUI
weatherApiAddress = 'https://api.openweathermap.org/data/2.5/weather?appid=070f601ac897b008a3ae6d4c310e1244&q='
nlp = spacy.load('en_core_web_sm')
root = Tk()
root.minsize(200,200)
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
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source,timeout=3)
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
    wakeWordList = ['hi computer','computer','hi pixie','pixie','hypixi','a pixie']

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
    greetingInputs = ['hi','hey','wassup','hello','hypixi','hai','hay','pixie']

    #greeting responses
    greetingOutput = ['oh hi there', 'hey cutie', 'hello there', "it's good to see you"]

    for word in text.split():
        if word.lower() in greetingInputs:
            print("have a greeting")
            return random.choice(greetingOutput)

    #for no greeting,
    print("no greeting")
    return ''

def driver():
    #record the audio
    global myStr
    myStr.set("listening..")
    print("listening..")
    text = hearAudio()
    print("done listening, in driver")
    if audioFlag == 0:
        response = ''

        if(wakeWords(text)):
            print("pixie is awake")
            #check for greetings by the user
            response += greeting(text)

            entities = nlp(text)
            # print("entities : ")
            # for ent in entities.ents:
            #     print(ent.text,ent.label_)

            # print("end of entities")
            #it is related to date?
            if 'date' in text:
                getDate()
                response += ',' + getDate()

            #did the user say 'who is ..'?
            if 'who is' in text:
                print("getting info on ")
                personList = [x.text for x in entities.ents if x.label_ == 'PERSON']
                print(personList)
                for person in personList:
                    if 'pixie' != person.lower():
                        wiki = wikipedia.summary(person, sentences=2)
                        response += ',' + wiki

            #is the user asking how the weather is?
            if 'weather' in text:
                cityList = [x.text for x in entities.ents if x.label_ == 'GPE']
                for city in cityList:
                    url = weatherApiAddress + city
                    jsonData = requests.get(url).json()
                    print(' , for {},we can see {} and the temperature is {} degree celsius'.format(city,
                                                                                                 jsonData['weather'][0]['description'],
                                                                                                 int(jsonData['main']['temp'] - 273.15)))
                    response += ' , for {},we can see {} and the temperature is {} degree celsius'.format(city,
                                                                                                 jsonData['weather'][0]['description'],
                                                                                                 int(jsonData['main']['temp'] - 273.15))

            #lets have the assistant to talk
            myStr.set(response)
            speakAudio(response)

myLabel = Label(root,textvariable = myStr,anchor=W)
speakButton = Button(root,text = "click me to talk",command = driver)
myLabel.pack()
speakButton.pack(side=BOTTOM)
root.mainloop()