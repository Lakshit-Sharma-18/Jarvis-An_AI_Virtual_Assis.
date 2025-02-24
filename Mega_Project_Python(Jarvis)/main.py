# in this we installed speech recognition , setup tools 
import speech_recognition as sr
import webbrowser  # this is used for opeing and closing of webbrowser 
import pyttsx3 # this is use for text to spech (jarvis) -- this is installed not given by python directly  
import musiclib
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
# init func is used to initialise the object of the class pyttsx 
ttsx = pyttsx3.init()  
newsapi = "news_api" 

def speak(text) :
    ttsx.say(text)
    ttsx.runAndWait()


def aiProcess(command):
    client = OpenAI(api_key="open_api_key",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content
    
def processCommand(c):
    if "google kholna" in c.lower():
        webbrowser.open("https://www.google.com")
   
    elif "youtube kholna" in c.lower():
        webbrowser.open("https://www.youtube.com")  
   
    elif "spotify kholna" in c.lower():
        webbrowser.open("https://open.spotify.com")
    
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclib.music[song] 
        webbrowser.open(link)
   
    elif "news" in c.lower():
        r = requests.get("news_api")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
                
            
    else:
        #if nothing works then ai will handle
        
        
        output = aiProcess(c)
        speak(output) 
    
if __name__ == "__main__":
    speak("Jarvis is waking up .......  ")
    
    while True:
        r = sr.Recognizer()
        print ("Recognizing .... ")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
                            
        except Exception as e:
            print("Error " .format(e))
        