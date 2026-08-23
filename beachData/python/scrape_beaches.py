import json
import requests
import time
import re


INPUT_FILE = "beaches.json"
OUTPUT_FILE = "searxng.json"

OPENSERP_URL = "http://127.0.0.1:7000"

SEARCH_RESULTS = 10

HEADERS = {
    "User-Agent": "BeachResearch/1.0"
}


def get_beach_name(beach):

    return beach.get(
        "tags",
        {}
    ).get(
        "name",
        f"ID {beach.get('id')}"
    ).strip()


def normalize_text(text):

    text = text.lower()

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def contains_beach_name(result, beach_name):

    title = normalize_text(
        result.get("title", "")
    )

    content = normalize_text(
        result.get("content")
        or result.get("description")
        or ""
    )

    name = normalize_text(
        beach_name
    )

    # Exact beach name must appear in either
    # the title OR the content.
    return (
        name in title
        or name in content
    )


def search_beach(beach):

    beach_id = beach.get("id")
    name = get_beach_name(beach)

    if not name:
        return beach_id, []

    query = f'"{name}" Hawaii Beach Activities'

    print(f"SEARCH → {name}")

    try:

        response = requests.get(
            f"{OPENSERP_URL}/mega/search",
            params={
                "text": query,
                "engines": (
                    "google,"
                    "duckduckgo,"
                    "yandex,"
                    "baidu,"
                    "ecosia"
                ),
                "limit": SEARCH_RESULTS,
                "format": "json",
                "mode": "balanced",
                "extract": 2
            },
            headers=HEADERS,
            timeout=90
        )

        response.raise_for_status()

        data = response.json()

        cleaned_results = []

        for result in data.get(
            "results",
            []
        ):

            title = result.get(
                "title",
                ""
            )

            content = (
                result.get("content")
                or result.get("description")
                or ""
            )

            url = result.get(
                "url",
                ""
            )

            cleaned_result = {
                "title": title,
                "content": content,
                "url": url
            }

            # ------------------------------------------------
            # IMPORTANT:
            # Only keep results that explicitly mention
            # the beach name.
            # ------------------------------------------------

            if not contains_beach_name(
                cleaned_result,
                name
            ):

                print(
                    f"  REJECT → {title}"
                )

                continue

            print(
                f"  ACCEPT → {title}"
            )

            cleaned_results.append(
                cleaned_result
            )

        print(
            f"FOUND → {name}: "
            f"{len(cleaned_results)} relevant sources"
        )

        return beach_id, cleaned_results

    except Exception as e:

        print(
            f"ERROR → {name}: {e}"
        )

        return beach_id, []


def save_data(results):

    temp_file = OUTPUT_FILE + ".tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )

    # Replace the old file only after writing
    # the new one successfully.

    import os

    os.replace(
        temp_file,
        OUTPUT_FILE
    )


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    beaches = data["elements"]

    print(
        f"Found {len(beaches)} beaches.\n"
    )

    # --------------------------------------------------------
    # Resume existing data
    # --------------------------------------------------------

    try:

        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            results = json.load(f)

        print(
            f"Loaded {len(results)} existing results.\n"
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        results = {}

    beaches_to_search = [
        beach
        for beach in beaches
        if str(beach.get("id"))
        not in results
    ]

    print(
        f"Remaining: "
        f"{len(beaches_to_search)}\n"
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    try:

        for index, beach in enumerate(
            beaches_to_search,
            start=1
        ):

            name = get_beach_name(
                beach
            )

            print(
                f"[{index}/{len(beaches_to_search)}] "
                f"{name}"
            )

            beach_id, search_results = search_beach(
                beach
            )

            results[str(beach_id)] = search_results

            # Save after EVERY beach
            save_data(
                results
            )

            print(
                f"PROGRESS → "
                f"{index}/{len(beaches_to_search)}"
            )

            print()

            # Don't hammer OpenSERP
            time.sleep(1)

    except KeyboardInterrupt:

        print()
        print("STOPPED.")
        print(
            "Everything up to the last completed beach "
            "has been saved."
        )
        print(
            "Run the script again to resume."
        )

        return

    print("Finished!")

    print(
        f"Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()