import openwakeword
from openwakeword.model import Model

print("Loading wake-word engine...")

# Download/load the built-in wake-word models
openwakeword.utils.download_models()

model = Model(
    wakeword_models=["hey_jarvis"]
)

print("Wake-word engine ready.")
print("Say: Hey JARVIS")


def detect_wake_word():
    import pyaudio
    import numpy as np

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1280
    )

    try:
        while True:

            data = stream.read(
                1280,
                exception_on_overflow=False
            )

            audio_data = np.frombuffer(
                data,
                dtype=np.int16
            )

            prediction = model.predict(audio_data)

            for name, score in prediction.items():

                if score > 0.5:

                    print(
                        f"Wake word detected: {name} "
                        f"(score: {score:.2f})"
                    )

                    return True

    finally:

        stream.stop_stream()
        stream.close()
        audio.terminate()


if __name__ == "__main__":
    detect_wake_word()