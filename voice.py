import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()


def speak(text):
    print("JARVIS:", text)

    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        engine.say(str(text))
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print("TTS ERROR:", repr(e))


def listen():
    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text

    except sr.UnknownValueError:

        print("JARVIS: I didn't understand that.")

        return ""

    except sr.RequestError as e:

        print("Speech recognition error:", e)

        return ""