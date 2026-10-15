from fastapi import FastAPI
import requests
import json
import re

from memory import init_db, save_memory, get_memories
from tools import execute_tool, TOOLS
from web_search import search_web


app = FastAPI(title="JARVIS API")

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"

init_db()


# =========================================================
# QWEN
# =========================================================

def ask_jarvis(message, system_prompt):

    data = {
        "model": MODEL,

        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],

        "think": False,
        "stream": False,

        "options": {
            "num_predict": 150,
            "temperature": 0.2
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=300
        )

        if response.status_code != 200:

            print(
                "OLLAMA ERROR:",
                response.status_code
            )

            return None

        return response.json()["message"]["content"]

    except Exception as e:

        print(
            "OLLAMA CONNECTION ERROR:",
            repr(e)
        )

        return None


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "JARVIS API is running."
    }


# =========================================================
# YOUTUBE PLAY QUERY EXTRACTION
# =========================================================

def extract_youtube_play_query(message):

    text = message.strip()

    # Remove wake-word if it reaches the API
    text = re.sub(
        r"^\s*(hey\s+jarvis|jarvis)\s*[,:\-]?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove polite words at the beginning
    text = re.sub(
        r"^\s*(please|can you|could you|would you)\s+",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Must contain "play"
    match = re.search(
        r"\bplay\b\s+(.+)",
        text,
        flags=re.IGNORECASE
    )

    if not match:
        return None

    query = match.group(1).strip()

    # Remove YouTube wording from the END.
    # This is intentionally done only at the end so
    # artist/song names containing similar words are safer.

    query = re.sub(
        r"\s+(on|in|from)\s+youtube\s*$",
        "",
        query,
        flags=re.IGNORECASE
    )

    query = re.sub(
        r"\s+youtube\s*$",
        "",
        query,
        flags=re.IGNORECASE
    )

    query = query.strip(" .,!?")

    if not query:
        return None

    return query


# =========================================================
# CHAT
# =========================================================

@app.post("/chat")
def chat(message: str):

    print("\nUSER:", message)

    lower_message = message.lower().strip()


    # =====================================================
    # MEMORY
    # =====================================================

    if lower_message.startswith("remember that"):

        memory = message[
            len("remember that"):
        ].strip()

        if memory:

            save_memory(memory)

            print(
                "MEMORY SAVED:",
                memory
            )

            return {
                "response":
                    f"Understood. I'll remember that: {memory}",

                "action":
                    "save_memory"
            }


    # =====================================================
    # DIRECT YOUTUBE PLAYBACK
    # =====================================================
    # This is handled BEFORE Agent Mode.
    #
    # Example:
    # "play Arijit Singh songs on YouTube"
    #
    # This directly calls Playwright through
    # execute_tool("play_youtube", query).
    # =====================================================

    if "play" in lower_message and "youtube" in lower_message:

        youtube_query = extract_youtube_play_query(message)

        if youtube_query:

            print(
                "YOUTUBE PLAY REQUEST:",
                youtube_query
            )

            result = execute_tool(
                "play_youtube",
                youtube_query
            )

            print(
                "TOOL:",
                "play_youtube",
                "| QUERY:",
                youtube_query
            )

            return {
                "response": result,
                "action": "play_youtube"
            }


    # =====================================================
    # DIRECT COMPUTER COMMANDS
    # =====================================================
    # These do NOT depend on Qwen.
    # This makes simple commands reliable.
    # =====================================================

    # Calculator

    if "calculator" in lower_message:

        result = execute_tool(
            "open_calculator"
        )

        print(
            "TOOL:",
            "open_calculator"
        )

        return {
            "response": result,
            "action": "open_calculator"
        }


    # Notepad

    if "notepad" in lower_message:

        result = execute_tool(
            "open_notepad"
        )

        print(
            "TOOL:",
            "open_notepad"
        )

        return {
            "response": result,
            "action": "open_notepad"
        }


    # Chrome

    if (
        "open chrome" in lower_message
        or "launch chrome" in lower_message
        or "start chrome" in lower_message
    ):

        result = execute_tool(
            "open_chrome"
        )

        print(
            "TOOL:",
            "open_chrome"
        )

        return {
            "response": result,
            "action": "open_chrome"
        }


    # YouTube

    if (
        "open youtube" in lower_message
        or "launch youtube" in lower_message
        or "start youtube" in lower_message
    ):

        result = execute_tool(
            "open_youtube"
        )

        print(
            "TOOL:",
            "open_youtube"
        )

        return {
            "response": result,
            "action": "open_youtube"
        }


    # Google

    if (
        "open google" in lower_message
        or "launch google" in lower_message
        or "start google" in lower_message
    ):

        result = execute_tool(
            "open_google"
        )

        print(
            "TOOL:",
            "open_google"
        )

        return {
            "response": result,
            "action": "open_google"
        }


    # =====================================================
    # DIRECT GOOGLE SEARCH
    # =====================================================

    if (
        "search" in lower_message
        and "google" in lower_message
    ):

        query = lower_message

        query = query.replace(
            "search",
            "",
            1
        )

        query = query.replace(
            "on google",
            ""
        )

        query = query.replace(
            "in google",
            ""
        )

        query = query.replace(
            "google",
            ""
        )

        query = query.replace(
            "for",
            "",
            1
        )

        query = query.strip()

        if query:

            result = execute_tool(
                "search_google",
                query
            )

            print(
                "TOOL:",
                "search_google",
                "| QUERY:",
                query
            )

            return {
                "response": result,
                "action": "search_google"
            }


    # =====================================================
    # DIRECT YOUTUBE SEARCH
    # =====================================================

    if (
        "search" in lower_message
        and "youtube" in lower_message
    ):

        query = lower_message

        query = query.replace(
            "search",
            "",
            1
        )

        query = query.replace(
            "on youtube",
            ""
        )

        query = query.replace(
            "in youtube",
            ""
        )

        query = query.replace(
            "youtube",
            ""
        )

        query = query.replace(
            "for",
            "",
            1
        )

        query = query.strip()

        if query:

            result = execute_tool(
                "search_youtube",
                query
            )

            print(
                "TOOL:",
                "search_youtube",
                "| QUERY:",
                query
            )

            return {
                "response": result,
                "action": "search_youtube"
            }


    # =====================================================
    # AGENT MODE
    # =====================================================

    tool_words = [
        "open",
        "launch",
        "start",
        "run",
        "search",
        "find",
        "go"
    ]

    needs_agent = any(
        word in lower_message.split()
        for word in tool_words
    )


    if needs_agent:

        tool_text = "\n".join(
            f"{name}: {info['description']}"
            for name, info in TOOLS.items()
        )


        decision_prompt = f"""
You are JARVIS's computer-action planner.

AVAILABLE SAFE TOOLS:

{tool_text}

USER REQUEST:

{message}

Return ONLY valid JSON.

Example:

{{"actions":[{{"tool":"open_calculator","argument":""}}]}}

For multiple actions:

{{"actions":[{{"tool":"open_chrome","argument":""}},{{"tool":"search_google","argument":"DSA questions"}}]}}

If no computer action is required:

{{"actions":[]}}

Rules:

- Only use available tools.
- Never invent tools.
- Search queries go inside argument.
- Do not use Markdown.
- Do not use ``` .
- Return JSON only.
"""


        decision = ask_jarvis(
            message,
            decision_prompt
        )


        actions = []


        if decision:

            try:

                decision = decision.strip()


                # Remove Markdown fences if Qwen
                # accidentally adds them.

                if "{" in decision:

                    start = decision.find("{")
                    end = decision.rfind("}") + 1

                    decision = decision[
                        start:end
                    ]


                parsed = json.loads(
                    decision
                )

                actions = parsed.get(
                    "actions",
                    []
                )

                print(
                    "AGENT DECISION:",
                    parsed
                )

            except Exception as e:

                print(
                    "AGENT JSON ERROR:",
                    repr(e)
                )

                print(
                    "RAW RESPONSE:",
                    decision
                )


        results = []


        # Maximum 5 actions

        for action in actions[:5]:

            tool_name = action.get(
                "tool"
            )

            argument = action.get(
                "argument",
                ""
            )


            if tool_name in TOOLS:

                print(
                    "EXECUTING:",
                    tool_name,
                    argument
                )

                result = execute_tool(
                    tool_name,
                    argument
                )

                results.append(
                    result
                )


        if results:

            return {
                "response":
                    " ".join(results),

                "action":
                    "agent"
            }


    # =====================================================
    # WEB SEARCH
    # =====================================================

    web_words = [
        "latest",
        "today",
        "current",
        "recent",
        "news",
        "weather",
        "price",
        "who won",
        "look up"
    ]


    needs_web = any(
        word in lower_message
        for word in web_words
    )


    if needs_web:

        print(
            "JARVIS: Searching the web..."
        )


        results = search_web(
            message,
            max_results=3
        )


        if results:

            web_context = "\n\n".join(

                f"""
RESULT {i}

TITLE:
{r['title']}

DESCRIPTION:
{r['body'][:300]}

SOURCE:
{r['url']}
"""

                for i, r in enumerate(
                    results,
                    1
                )
            )


            web_prompt = f"""
You are JARVIS.

User question:

{message}

Search results:

{web_context}

Answer using the search results.

Rules:

- Give the actual answer.
- Do not simply tell the user to visit a website.
- Do not invent information.
- Keep the answer under 120 words.
- Mention the source when useful.
"""


            answer = ask_jarvis(
                message,
                web_prompt
            )


            if answer:

                return {
                    "response": answer,
                    "action": "web_search"
                }


        return {
            "response":
                "I couldn't find useful information on the web.",

            "action":
                "web_search"
        }


    # =====================================================
    # NORMAL AI CHAT
    # =====================================================

    memories = get_memories()


    memory_text = "\n".join(
        f"- {memory}"
        for memory in memories
    )


    system_prompt = f"""
You are JARVIS, a helpful personal AI assistant.

Saved memories:

{memory_text}

Use these memories when relevant.

Be helpful, concise and natural.

Do not claim that you performed a computer action
unless a real tool actually performed it.
"""


    answer = ask_jarvis(
        message,
        system_prompt
    )


    if answer is None:

        return {
            "response":
                "I couldn't get a response from my local AI.",

            "action":
                "none"
        }


    return {
        "response":
            answer,

        "action":
            "none"
    }



































































































































































# from tools import execute_command
# from memory import init_db, save_memory, get_memories
# from fastapi import FastAPI
# import requests

# app = FastAPI(title="JARVIS API")

# OLLAMA_URL = "http://localhost:11434/api/chat"
# MODEL = "qwen3:4b"
# init_db()

# @app.get("/")
# def home():
#     return {
#         "status": "online",
#         "message": "JARVIS API is running."
#     }



# @app.post("/chat")
# def chat(message: str):

#     # Computer tools
#     tool_commands = [
#         "open chrome",
#         "open youtube",
#         "open google",
#         "open calculator",
#         "open notepad"
#     ]

#     if message.lower().strip() in tool_commands:
#         result = execute_command(message)

#         return {
#             "response": result
#         }

    

#     # Check if the user wants JARVIS to remember something
#     if message.lower().startswith("remember that"):
#         memory = message[len("remember that"):].strip()

#         if memory:
#             save_memory(memory)

#             return {
#                 "response": f"Understood. I'll remember that: {memory}"
#             }

#     # Get existing memories
#     memories = get_memories()

#     memory_text = "\n".join(
#         f"- {memory}" for memory in memories
#     )

#     system_prompt = f"""
# You are JARVIS, a helpful personal AI assistant.

# The following are memories explicitly saved by the user:

# {memory_text}

# Use these memories when relevant.
# Do not claim to remember something that isn't in the memory list.
# """

#     data = {
#         "model": MODEL,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": message
#             }
#         ],
#         "stream": False
#     }

#     response = requests.post(
#         OLLAMA_URL,
#         json=data
#     )

#     if response.status_code != 200:
#         return {
#             "error": response.text
#         }

#     result = response.json()

#     return {
#         "response": result["message"]["content"]
#     }
