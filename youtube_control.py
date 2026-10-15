from playwright.sync_api import sync_playwright
import urllib.parse


def play_youtube(query):
    print(f"Opening YouTube and searching for: {query}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        search_url = (
            "https://www.youtube.com/results?search_query="
            + urllib.parse.quote_plus(query)
        )

        page.goto(search_url, wait_until="domcontentloaded")

        page.wait_for_timeout(4000)

        # Click the first video result
        video = page.locator("a#video-title").first

        if video.count() == 0:
            print("No video found.")
            browser.close()
            return False

        video.click()

        page.wait_for_timeout(5000)

        print(f"Playing: {query}")

        # Keep browser open
        return True


if __name__ == "__main__":
    query = input("What do you want to play? ")

    if play_youtube(query):
        print("YouTube playback started.")
    else:
        print("Could not start playback.")