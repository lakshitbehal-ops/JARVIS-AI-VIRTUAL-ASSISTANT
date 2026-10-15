import speech_recognition as sr
from faster_whisper import WhisperModel
import tempfile
import os

recognizer = sr.Recognizer()

print("Loading local Whisper model...")

model = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8"
)

print("Local Whisper ready.")


def listen():
    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        audio = recognizer.listen(source)

    temp_file = None

    try:
        print("Transcribing locally...")

        # Save microphone audio as a temporary WAV file
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as f:

            temp_file = f.name
            f.write(audio.get_wav_data())

        # Whisper reads the WAV file
        segments, info = model.transcribe(
            temp_file,
            beam_size=1
        )

        text = " ".join(
            segment.text for segment in segments
        ).strip()

        print("You:", text)

        return text

    except Exception as e:

        print("LOCAL STT ERROR:", repr(e))

        return ""

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)