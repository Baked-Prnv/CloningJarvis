import pyttsx3
import speech_recognition
import datetime
import os
import cv2
import random
from playsound import playsound
from requests import get
import wikipedia
import pywhatkit
import smtplib
import sys

engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def take_command():
    listener = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("listening...")
        listener.pause_threshold = 1
        audio = listener.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = listener.recognize_google(audio,language="en-in")
        print(f"user said : {query}.")

    except Exception as e:
        speak("say that again.")
        return "none"
    return query

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>0 and hour<12:
        speak("good morning.")
    elif hour>12 and hour<18:
        speak("good afternoon.")
    else:
        speak("good evening.")
    speak("i am jarvis sir. how can i help you?")

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('YourEmailAddress','PassWord')
    server.sendmail('YourEmailAddress', to, content)
    server.close()

if __name__ == "__main__":
    wish()
    while True:

        query = take_command().lower()

        # logic building for tasks
        if "open microsoft word" in query:
            os.system("open /Applications/Microsoft\ Word.app")

        elif "open chess" in query:
            os.system("open /System/Applications/Chess.app")

        elif "open terminal" in query:
            os.system("open /System/Applications/Utilities/Terminal.app")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img =cap.read()
                cv2.imshow('webcam',img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "song" in query:
            music_dir = "Data/Music"
            song = os.listdir(music_dir)
            rd = random.choice(song)
            #os.system(os.path.join(music_dir, rd))  # sh: permission denied error
            playsound(rd) #jugaad

        elif "ip address" in query:
            ip = get("https://api.ipify.org")
            speak(f"your ip address is {ip}")

        elif "time" in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"current time is {time}")

        elif "wikipedia" in query:
            speak("searching wikipedia")
            query = query.replace(" jarvis wikipedia","")
            result = wikipedia.summary(query, sentences=2)
            '''try:
                speak("according to wikipedia " + result)
            except:
                speak("sorry wikipedia gave an error")'''
            speak("according to wikipedia")
            speak(result)
            '''speak("what should i search on wikipedia for you")
            wiki_search = take_command().lower()
            wiki_result = pywhatkit.info(wiki_search, lines=2)
            speak(wiki_result)'''                 #disambiguation error to be resolved

        elif "google" in query:
            speak("what should i search on google for you")
            google_search = take_command().lower()
            pywhatkit.search(google_search)

        elif "youtube" in query:
            speak("what should i search on youtube for you")
            yt_search = take_command().lower()
            pywhatkit.playonyt(yt_search)

        elif "shutdown" in query:
            speak("shutting down in 1 min")
            pywhatkit.shutdown(100)

        elif "cancel shutdown" in query:
            speak("canceling shut down")
            pywhatkit.cancelShutdown()

        elif "whatsapp" in query:
            whom ="+91(NUMBER)"
            speak("to whom you wanted to send the message")
            to_whom = take_command().lower()
            if to_whom == "pranav":
                whom = "+91(NUMBER)"
            speak("what message should i send")
            msg = take_command().lower()
            pywhatkit.sendwhatmsg(whom,msg,13,43)

        elif "email" in query:
            try:
                to = "Receiver'sEmailAddress"
                content = "test msg "
                sendEmail(to, content)
                speak("email has been sent.")
            except Exception as e:
                print(e)
                speak("sorry sir something went wrong.")

        elif "no thank you" in query:
            speak("have a good day sir.")
            sys.exit()

        speak("is there anything else i can do for you?")