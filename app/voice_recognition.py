import speech_recognition as sr
import pyaudio

r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except:
        pass
