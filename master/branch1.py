import speech_recognition as sr
import requests
import threading


def recognize_speech_from_mic(recognizer, microphone, source):
    print("Listening")
    try:
        audio = recognizer.listen(source, timeout=5.0, phrase_time_limit=5)
    except sr.WaitTimeoutError:
        print("Too  Quiet")
        x = threading.Thread(target=loop, args=(source,))
        x.start()
        return ({"transcription": ""}, x)
    print("Listened")
    x = threading.Thread(target=loop, args=(source,))
    x.start()

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try: # idk i just copied this shit, I wouldnt touch those try blocks are there for a reason
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return (response, x)

def showalert(ghost: str):
    print(f"Found the ghost {ghost}")
    requests.get(f"http://127.0.0.1:8844/changeghost?ghost={ghost.capitalize()}")

def parse(words: str, transaltedghosts: dict, allghosts: list) -> None:
    for ghost in allghosts:
        if ghost.lower() in words.replace("spirit box", "").replace("spiritbox", "").split(" "):
            requests.get(f"http://127.0.0.1:8844/setmsg?msg={words.capitalize()}")
            return showalert(ghost)
    for ghost, translatedg in transaltedghosts.items():
        for tg in translatedg:
            if " " not in tg:
                if tg in words.replace("spirit box", "").replace("spiritbox", "").split(" "):
                    requests.get(f"http://127.0.0.1:8844/setmsg?msg={words.replace(tg, ghost).capitalize()}")
                    return showalert(ghost)
            else:
                if tg in words.replace("spirit box", "").replace("spiritbox", ""):
                    requests.get(f"http://127.0.0.1:8844/setmsg?msg={words.replace(tg, ghost).capitalize()}")
                    return showalert(ghost)
    requests.get(f"http://127.0.0.1:8844/setmsg?msg={words.capitalize()}")
    print(f"{words}: Could not find a ghost in the text")
    # if words.capitalize() in allghosts:
    #     return showalert(words)
    # else:
        # for ghost, translatedg in transaltedghosts.items():
        #     if ghost in translatedg:
        #         return showalert(ghost)

def loop(source):
    guess, x = recognize_speech_from_mic(recognizer, microphone, source)
    guess = guess["transcription"]
    print(guess)
    if guess:
        tghosts = {"deogen": ["deodorant", "dia", "doj", "deal jen", ". gin", ". jen", "kyojin", "dieldrin", "degen d", "yogen", "deogun", "yogan"], "jinn": ["jen", "gin"],  "goryo": ["gorio", "correo", "goryeo"], "hantu": ["hontou", "han to", "onto", "en tu", "khon2"], "moroi": ["morrow", "mora", "morris", "maura", "morai"], "myling": ["mylink", "miling", "mailing", "mi-ling", "smiling"], "obake": ["obaka", "obok a", "baki", "obate", "obagi"],
        "oni": ["only"], "onryo": ["on rio"], "raiju": ["raichu", "raisu", "raju"], "thaye": ["dai", "thigh", "thai"], "the Mimic": ["mimic"], "the Twins": ["twins"], "wraith": ["race", "rate", "raise"], "yurei": ["yuri", "urie"]}
        ghosts = ["Banshee", "Demon", "Deogen", "Goryo", "Hantu", "Jinn", "Mare", "Moroi", "Myling", "Obake", "Oni", "Onryo", "Phantom", "Poltergeist", "Raiju", "Revenant", "Shade", "Spirit", "Thaye", "The mimic", "The twins", "Wraith", "Yokai", "Yurei"]
        parse(guess.lower(), tghosts, ghosts)
    x.join()

def main():
    with microphone as source:
        print("Wait 3 seconds...")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print("Begin Talking")
        loop(source)
 
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    main()