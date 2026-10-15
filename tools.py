import subprocess
import webbrowser
import urllib.parse

from youtube_control import play_youtube


TOOLS = {
    "open_chrome": {
        "description": "Open Google Chrome"
    },

    "open_youtube": {
        "description": "Open YouTube"
    },

    "open_google": {
        "description": "Open Google"
    },

    "open_calculator": {
        "description": "Open Windows Calculator"
    },

    "open_notepad": {
        "description": "Open Windows Notepad"
    },

    "open_vscode": {
        "description": "Open Visual Studio Code"
    },

    "open_whatsapp": {
        "description": "Open WhatsApp"
    },

    "open_spotify": {
        "description": "Open Spotify"
    },

    "open_chatgpt": {
        "description": "Open ChatGPT"
    },

    "open_file_explorer": {
        "description": "Open Windows File Explorer"
    },

    "search_google": {
        "description": "Search Google for a user-provided query"
    },

    "search_youtube": {
        "description": "Search YouTube for a user-provided query"
    },

    "play_youtube": {
        "description": "Play the first YouTube video matching a user-provided query"
    }
}


def execute_tool(tool_name, argument=None):

    # =====================================================
    # EXISTING TOOLS
    # =====================================================

    if tool_name == "open_chrome":

        subprocess.Popen(
            "start chrome",
            shell=True
        )

        return "Chrome opened."


    elif tool_name == "open_youtube":

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "YouTube opened."


    elif tool_name == "open_google":

        webbrowser.open(
            "https://www.google.com"
        )

        return "Google opened."


    elif tool_name == "open_calculator":

        subprocess.Popen(
            "calc.exe"
        )

        return "Calculator opened."


    elif tool_name == "open_notepad":

        subprocess.Popen(
            "notepad.exe"
        )

        return "Notepad opened."


    # =====================================================
    # NEW APPLICATION TOOLS
    # =====================================================

    elif tool_name == "open_vscode":

        try:

            subprocess.Popen(
                "code",
                shell=True
            )

            return "VS Code opened."

        except Exception as e:

            print(
                "VS CODE ERROR:",
                repr(e)
            )

            return "I couldn't open VS Code."


    elif tool_name == "open_whatsapp":

        try:

            subprocess.Popen(
                "start whatsapp:",
                shell=True
            )

            return "WhatsApp opened."

        except Exception as e:

            print(
                "WHATSAPP ERROR:",
                repr(e)
            )

            return "I couldn't open WhatsApp."


    elif tool_name == "open_spotify":

        try:

            subprocess.Popen(
                "start spotify:",
                shell=True
            )

            return "Spotify opened."

        except Exception as e:

            print(
                "SPOTIFY ERROR:",
                repr(e)
            )

            return "I couldn't open Spotify."


    elif tool_name == "open_chatgpt":

        webbrowser.open(
            "https://chatgpt.com"
        )

        return "ChatGPT opened."


    elif tool_name == "open_file_explorer":

        try:

            subprocess.Popen(
                "explorer.exe"
            )

            return "File Explorer opened."

        except Exception as e:

            print(
                "FILE EXPLORER ERROR:",
                repr(e)
            )

            return "I couldn't open File Explorer."


    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

    elif tool_name == "search_google":

        if not argument:

            return "I need something to search for."

        query = urllib.parse.quote_plus(
            argument
        )

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        return f"Searching Google for {argument}."


    # =====================================================
    # YOUTUBE SEARCH
    # =====================================================

    elif tool_name == "search_youtube":

        if not argument:

            return "I need something to search for."

        query = urllib.parse.quote_plus(
            argument
        )

        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}"
        )

        return f"Searching YouTube for {argument}."


    # =====================================================
    # YOUTUBE PLAYBACK
    # =====================================================

    elif tool_name == "play_youtube":

        if not argument:

            return "I need to know what you want me to play."

        success = play_youtube(
            argument
        )

        if success:

            return f"Playing {argument} on YouTube."

        return f"I couldn't find a video for {argument}."


    # =====================================================
    # UNKNOWN TOOL
    # =====================================================

    return "I don't have permission to perform that action."