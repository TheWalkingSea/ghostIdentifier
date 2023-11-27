import speech_recognition as sr
import requests

def recognize_speech_from_mic(recognizer, microphone, ran=False):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        if not ran:
            recognizer.adjust_for_ambient_noise(source, duration=3)
            print("go go go ")
        print("Listening")
        audio = recognizer.listen(source, timeout=5.0)
        print("Listened")

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def showalert(ghost: str):
    print(f"Found the ghost {ghost}")
    requests.get(f"http://127.0.0.1:8844/changeghost?ghost={ghost.capitalize()}")

def main(words: str, transaltedghosts: dict, allghosts: list) -> None:
    print(words)
    for ghost in allghosts:
        if ghost.lower() in words.replace("spirit box", "").replace("spiritbox", "").split(" "):
            requests.get(f"http://127.0.0.1:8844/setmsg?msg={words.capitalize()}")
            return showalert(words)
    for ghost, translatedg in transaltedghosts.items():
        for tg in translatedg:
            if tg in words.replace("spirit box", "").replace("spiritbox", "").split(" "):
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

    
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    ran = False
    print("Wait 3 seconds...")
    # while True:
    # guess = recognize_speech_from_mic(recognizer, microphone, ran)["transcription"]
    guess = "i didn\'t get i didn\'t get spirit box i never got spiritbox i don't know why so annoying could have gone on to"
    ran = True
    if guess:
        tghosts = {"deogen": ["deodorant", "dia", "doj", "deal jen", ". gin", ". jen", "kyojin", "dieldrin"], "jinn": ["jen", "gin"],  "goryo": ["gorio", "correo", "goryeo"], "hantu": ["onto", "en tu", "khon2"], "moroi": ["morrow", "mora", "morris", "maura"], "myling": ["mylink", "miling", "mailing"], "obake": ["obaka", "obok a", "no baki", "obate"],
        "oni": ["only"], "onryo": ["on rio"], "raiju": ["raichu", "raisu", "raju"], "thaye": ["dai", "thigh", "thai"], "the Mimic": ["mimic"], "the Twins": ["twins"], "wraith": ["race", "rate", "raise"], "yurei": ["yuri", "urie"]}
        ghosts = ["Banshee", "Demon", "Deogen", "Goryo", "Hantu", "Jinn", "Mare", "Moroi", "Myling", "Obake", "Oni", "Onryo", "Phantom", "Poltergeist", "Raiju", "Revenant", "Shade", "Spirit", "Thaye", "The mimic", "The twins", "Wraith", "Yokai", "Yurei"]
        main(guess.lower(), tghosts, ghosts)