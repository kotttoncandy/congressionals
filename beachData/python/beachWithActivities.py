import json
import requests
from bs4 import BeautifulSoup

BEACHES_FILE = "beaches.json"
WEB_DATA_FILE = "web_data.json"
OUTPUT_FILE = "beaches_with_activities.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:latest"

PAGE_TIMEOUT = 12
OLLAMA_TIMEOUT = 180

MAX_PAGE_CHARS = 12000

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/139.0 Safari/537.36"
    )
}


ALLOWED_ACTIVITIES = [
    "Swimming",
    "Surfing",
    "Snorkeling",
    "Fishing",
    "Taking Pictures for the gram",
    "Sunset watching",
    "Beach walking",
    "Eat and talk story",
    "Wildlife watching",
    "Tide pooling",
    "Beach volleyball",
    "Two-touch Football with friends",
    "Watch the sunset with friends",
    "Talk Story"
]


def get_beach_name(beach):

    return beach.get(
        "tags",
        {}
    ).get(
        "name",
        f"ID {beach.get('id')}"
    ).strip()


# --------------------------------------------------
# Fetch actual webpage
# --------------------------------------------------

def fetch_page(url):

    if not url:
        return ""

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=PAGE_TIMEOUT
        )

        response.raise_for_status()

        # Make sure we're actually dealing with HTML
        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" not in content_type:
            print(
                f"    NOT HTML → {url}"
            )

            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove useless webpage elements

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript",
            "svg",
            "form"
        ]):

            element.decompose()

        # Get actual visible text

        text = soup.get_text(
            " ",
            strip=True
        )

        # Clean excessive whitespace

        text = " ".join(
            text.split()
        )

        # Prevent gigantic pages
        text = text[:MAX_PAGE_CHARS]

        return text

    except requests.Timeout:

        print(
            f"    PAGE TIMEOUT → {url}"
        )

        return ""

    except requests.RequestException as e:

        print(
            f"    PAGE ERROR → {url}: {e}"
        )

        return ""

    except Exception as e:

        print(
            f"    PARSE ERROR → {url}: {e}"
        )

        return ""


# --------------------------------------------------
# Build context from actual webpages
# --------------------------------------------------

def build_web_context(sources):

    context = []

    for index, source in enumerate(
        sources,
        start=1
    ):

        title = source.get(
            "title",
            ""
        )

        url = source.get(
            "url",
            ""
        )

        print(
            f"    FETCH {index}/{len(sources)} → "
            f"{url}"
        )

        page_text = fetch_page(
            url
        )

        if not page_text:

            print(
                "    SKIPPED → no page content"
            )

            continue

        context.append(
            f"""
SOURCE {index}

TITLE:
{title}

URL:
{url}

ACTUAL WEBPAGE CONTENT:
{page_text}
"""
        )

    return "\n\n====================\n\n".join(
        context
    )


# --------------------------------------------------
# Ask Ollama
# --------------------------------------------------

def get_activities(
    beach,
    web_context
):

    name = get_beach_name(
        beach
    )

    allowed = ", ".join(
        ALLOWED_ACTIVITIES
    )

    prompt = f"""
You are a STRICT activity classifier for a Hawaii beach app.

BEACH:
{name}

LOCATION:
Oahu, Hawaii

Your task is to determine which activities are supported by the
ACTUAL WEBPAGE CONTENT provided below.

IMPORTANT:

You MUST base your answer ONLY on the webpage content.

Do NOT use your general knowledge.

Do NOT assume something is possible just because this is a beach.

Do NOT infer swimming just because the beach is popular.

Do NOT infer surfing just because the beach is on Oahu.

Do NOT infer snorkeling just because the beach has clear water.

If the webpage content does not provide evidence for an activity,
DO NOT include that activity.

When uncertain, leave the activity out.

AVAILABLE ACTIVITIES:

{allowed}

RULES:

- Choose between 2 and 5 activities.
- Only choose activities from the allowed list.
- Do not create new activities.
- Do not explain your answer.
- Return ONLY the activity names separated by commas.
- Do not return JSON.
- Do not use bullet points.

Example:

Swimming, Beach walking, Sunset watching

ACTUAL WEBPAGE CONTENT:

{web_context}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=OLLAMA_TIMEOUT
        )

        response.raise_for_status()

        result = response.json().get(
            "response",
            ""
        ).strip()

        # Remove accidental newlines
        result = " ".join(
            result.split()
        )

        # ------------------------------------------
        # Validate against allowed activities
        # ------------------------------------------

        found = []

        result_lower = result.lower()

        for activity in ALLOWED_ACTIVITIES:

            if activity.lower() in result_lower:

                found.append(
                    activity
                )

        # Remove duplicates
        found = list(
            dict.fromkeys(found)
        )

        return ", ".join(
            found
        )

    except requests.Timeout:

        print(
            f"    OLLAMA TIMEOUT → {name}"
        )

        return ""

    except Exception as e:

        print(
            f"    OLLAMA ERROR → {name}: {e}"
        )

        return ""


# --------------------------------------------------
# Save
# --------------------------------------------------

def save_data(data):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # ----------------------------------------------
    # Load beaches
    # ----------------------------------------------

    with open(
        BEACHES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        beach_data = json.load(
            f
        )

    beaches = beach_data[
        "elements"
    ]

    print(
        f"Found {len(beaches)} beaches."
    )

    # ----------------------------------------------
    # Load web search data
    # ----------------------------------------------

    with open(
        WEB_DATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        web_data = json.load(
            f
        )

    print(
        f"Loaded web data for "
        f"{len(web_data)} beaches."
    )

    # ----------------------------------------------
    # Load existing output
    # ----------------------------------------------

    try:

        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            output = json.load(
                f
            )

        print(
            f"Loaded {len(output)} "
            "already processed beaches."
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        output = {}

    print()

    # ----------------------------------------------
    # Process one beach at a time
    # ----------------------------------------------

    for index, beach in enumerate(
        beaches,
        start=1
    ):

        beach_id = str(
            beach.get("id")
        )

        name = get_beach_name(
            beach
        )

        print(
            f"======================================"
        )

        print(
            f"[{index}/{len(beaches)}] {name}"
        )

        print(
            f"======================================"
        )

        # Resume support

        if beach_id in output:

            print(
                "Already processed — skipping."
            )

            print()

            continue

        # ------------------------------------------
        # Get search results
        # ------------------------------------------

        sources = web_data.get(
            beach_id,
            []
        )

        if not sources:

            print(
                "No search data."
            )

            beach_copy = beach.copy()

            beach_copy[
                "activities"
            ] = ""

            output[
                beach_id
            ] = beach_copy

            save_data(
                output
            )

            continue

        print(
            f"Search sources: "
            f"{len(sources)}"
        )

        # ------------------------------------------
        # Fetch actual webpages
        # ------------------------------------------

        print(
            "Fetching actual webpages..."
        )

        web_context = build_web_context(
            sources
        )

        if not web_context:

            print(
                "No usable webpage content."
            )

            beach_copy = beach.copy()

            beach_copy[
                "activities"
            ] = ""

            output[
                beach_id
            ] = beach_copy

            save_data(
                output
            )

            continue

        # ------------------------------------------
        # Ask Ollama
        # ------------------------------------------

        print(
            "Asking Ollama..."
        )

        activities = get_activities(
            beach,
            web_context
        )

        print(
            f"ACTIVITIES → "
            f"{activities or 'NONE'}"
        )

        # ------------------------------------------
        # Store result
        # ------------------------------------------

        beach_copy = beach.copy()

        beach_copy[
            "activities"
        ] = activities

        output[
            beach_id
        ] = beach_copy

        # ------------------------------------------
        # Save immediately
        # ------------------------------------------

        save_data(
            output
        )

        print(
            "Saved."
        )

        print()

    print(
        "======================================"
    )

    print(
        "FINISHED!"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()