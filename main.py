from langchain_community.llms import Ollama
import pyttsx3
import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer

llm = Ollama(model="llama3.2:1b", system="You are a citizen helpline chatbot. Your duty is to assist citizens with their queries of differenct government schemes and services. To keep the chat conversational, answer user query in very short and ask user what they want to know more with regards to their query.")

engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_KalpanaM")

q = queue.Queue()
model = Model("vosk-model-small-hi-0.22")
recognizer = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
     while True:
        print("Listening...")
        data = q.get()
        if recognizer.AcceptWaveform(data):
            query = json.loads(recognizer.Result())['text']
            
            response = llm.invoke(query)
            print(response)
            engine.say(response)
            engine.runAndWait()
