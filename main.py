import requests
from local_voice import listen
from voice import speak

API_URL = "http://127.0.0.1:8000/chat"

WAKE_WORDS = [
    "hey jarvis",
    "hey jarvis",
    "jarvis"
]


def send_to_jarvis(text):
    try:
        response = requests.post(
            API_URL,
            params={"message": text},
            timeout=300
        )

        if response.status_code == 200:
            data = response.json()
            return data.get(
                "response",
                "I couldn't generate a response."
            )

        print("API error:", response.status_code)
        return "There was a problem with my API."

    except Exception as e:
        print("API ERROR:", repr(e))
        return "I couldn't connect to my API."


speak("JARVIS is online.")

while True:

    # -------------------------
    # WAIT FOR WAKE WORD
    # -------------------------

    print("\nWaiting for wake word...")
    text = listen()

    if not text:
        continue

    text = text.lower().strip()

    # Check wake word
    if any(word in text for word in WAKE_WORDS):

        speak("Yes?")

        # -------------------------
        # LISTEN FOR COMMAND
        # -------------------------

        command = listen()

        if not command:
            continue

        command = command.strip()

        # Exit command
        if command.lower() in [
            "exit",
            "quit",
            "shutdown",
            "goodbye"
        ]:
            speak("Shutting down. Goodbye.")
            break

        # -------------------------
        # SEND COMMAND TO API
        # -------------------------

        print("Command:", command)

        answer = send_to_jarvis(command)

        speak(answer)

































































































# import requests

# OLLAMA_URL = "http://localhost:11434/api/chat"
# MODEL = "qwen3:4b"

# print("JARVIS is online.")
# print("Type 'exit' to shut down.\n")

# while True:
#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         print("JARVIS: Shutting down.")
#         break

#     data = {
#         "model": MODEL,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "You are JARVIS, a helpful personal AI assistant."
#             },
#             {
#                 "role": "user",
#                 "content": user_input
#             }
#         ],
#         "stream": False
#     }

#     response = requests.post(OLLAMA_URL, json=data)

#     if response.status_code == 200:
#         result = response.json()
#         print("JARVIS:", result["message"]["content"])
#     else:
#         print("Error:", response.text)