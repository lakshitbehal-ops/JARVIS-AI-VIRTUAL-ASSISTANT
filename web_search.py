from ddgs import DDGS


def search_web(query, max_results=4):

    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        output = []

        for result in results:

            title = result.get("title", "").strip()
            body = result.get("body", "").strip()[:300]
            url = result.get("href", "").strip()

            if title or body:
                output.append({
                    "title": title,
                    "body": body,
                    "url": url
                })

        return output

    except Exception as e:

        print("WEB SEARCH ERROR:", repr(e))

        return []


if __name__ == "__main__":

    query = input("Search: ")

    results = search_web(query)

    for i, result in enumerate(results, 1):

        print(f"\n--- RESULT {i} ---")
        print("TITLE:", result["title"])
        print("DESCRIPTION:", result["body"])
        print("URL:", result["url"])
        