import json
import requests
import re
import time
from bs4 import BeautifulSoup


# ============================================================
# CONFIG
# ============================================================

INPUT_BEACHES = "beaches_with_activities.json"
WEB_DATA = "searxng_cleaned.json"
OUTPUT_FILE = "beaches_with_safety.json"

REQUEST_TIMEOUT = 15
DELAY = 0.5

# True = automatically continue where it left off
RESUME = True


# ============================================================
# KEYWORDS
# ============================================================

UNSAFE_KEYWORDS = {
    "dangerous for swimming": 10,
    "dangerous to swim": 10,
    "unsafe for swimming": 10,
    "unsafe to swim": 10,
    "not safe for swimming": 10,
    "not safe to swim": 10,
    "do not swim": 10,
    "don't swim": 10,
    "avoid swimming": 9,
    "not recommended for swimming": 9,
    "not suitable for swimming": 10,
    "unsuitable for swimming": 10,
    "strong currents": 8,
    "strong current": 8,
    "rip currents": 9,
    "rip current": 9,
    "dangerous currents": 10,
    "rough surf": 7,
    "dangerous surf": 10,
    "heavy surf": 7,
    "large surf": 6,
    "high surf": 6,
    "treacherous surf": 10,
    "hazardous surf": 10,
    "dangerous waves": 9,
    "large waves": 6,
    "dangerous shorebreak": 10,
    "pounding shorebreak": 8,
}


SAFE_KEYWORDS = {
    "good for swimming": 8,
    "great for swimming": 8,
    "excellent for swimming": 9,
    "ideal for swimming": 9,
    "perfect for swimming": 8,
    "safe for swimming": 9,
    "safe to swim": 9,
    "swimming is safe": 9,
    "popular for swimming": 6,
    "swimming is popular": 6,
    "calm waters": 7,
    "calm water": 7,
    "calm ocean": 7,
    "calm seas": 7,
    "gentle waves": 6,
    "gentle surf": 6,
    "small waves": 5,
    "protected cove": 5,
    "protected bay": 5,
    "sheltered waters": 6,
    "swimmable": 7,
}


CONDITIONAL_KEYWORDS = {
    "when calm": 6,
    "during calm conditions": 7,
    "in calm conditions": 7,
    "when the ocean is calm": 7,
    "when surf is low": 7,
    "during low surf": 6,
    "when waves are small": 6,
    "conditions permitting": 5,
    "depending on conditions": 5,
    "weather permitting": 4,
    "avoid during high surf": 8,
    "avoid during large surf": 8,
    "avoid during rough surf": 8,
}


# ============================================================
# FETCH PAGE
# ============================================================

def fetch_page(url):

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/139.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.text

    except Exception as e:

        print(
            f"    FETCH ERROR → {url}"
        )

        return ""


# ============================================================
# EXTRACT TEXT
# ============================================================

def extract_text(html):

    if not html:
        return ""

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
        "header",
        "aside"
    ]):

        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.lower()


# ============================================================
# KEYWORD MATCHING
# ============================================================

def find_keywords(text, keywords):

    matches = []
    score = 0

    for keyword, weight in keywords.items():

        if keyword in text:

            matches.append({
                "keyword": keyword,
                "weight": weight
            })

            score += weight

    return matches, score


# ============================================================
# SCORE URL
# ============================================================

def score_url(url):

    print(
        f"    FETCH → {url}"
    )

    html = fetch_page(url)

    if not html:
        return None

    text = extract_text(html)

    if not text:
        return None

    unsafe_matches, unsafe_score = find_keywords(
        text,
        UNSAFE_KEYWORDS
    )

    safe_matches, safe_score = find_keywords(
        text,
        SAFE_KEYWORDS
    )

    conditional_matches, conditional_score = find_keywords(
        text,
        CONDITIONAL_KEYWORDS
    )

    return {
        "url": url,
        "safe_score": safe_score,
        "unsafe_score": unsafe_score,
        "conditional_score": conditional_score,
        "safe_keywords": safe_matches,
        "unsafe_keywords": unsafe_matches,
        "conditional_keywords": conditional_matches
    }


# ============================================================
# SCORE BEACH
# ============================================================

def score_beach(sources):

    total_safe = 0
    total_unsafe = 0
    total_conditional = 0

    evidence = []

    for source in sources:

        url = source.get(
            "url",
            ""
        )

        if not url:
            continue

        result = score_url(url)

        if result is None:
            continue

        total_safe += result["safe_score"]
        total_unsafe += result["unsafe_score"]
        total_conditional += result["conditional_score"]

        if (
            result["safe_score"] > 0
            or result["unsafe_score"] > 0
            or result["conditional_score"] > 0
        ):

            evidence.append({
                "title": source.get(
                    "title",
                    ""
                ),
                "url": url,
                "safe_score": result["safe_score"],
                "unsafe_score": result["unsafe_score"],
                "conditional_score": result["conditional_score"],
                "safe_keywords": result["safe_keywords"],
                "unsafe_keywords": result["unsafe_keywords"],
                "conditional_keywords": result[
                    "conditional_keywords"
                ]
            })

        time.sleep(DELAY)


    # --------------------------------------------------------
    # No evidence
    # --------------------------------------------------------

    if not evidence:

        return {
            "status": "unknown",
            "score": 0,
            "safe_score": 0,
            "unsafe_score": 0,
            "conditional_score": 0,
            "reason": (
                "No relevant swimming keywords "
                "were found."
            ),
            "evidence": []
        }


    # --------------------------------------------------------
    # Determine status
    # --------------------------------------------------------

    if (
        total_unsafe >= 10
        and total_unsafe > total_safe
    ):

        status = "unsafe"

    elif (
        total_conditional >= 6
        and total_conditional >= total_safe
        and total_conditional > total_unsafe
    ):

        status = "conditional"

    elif total_safe > total_unsafe:

        status = "safe"

    elif total_unsafe > total_safe:

        status = "unsafe"

    else:

        status = "unknown"


    score = (
        total_safe
        - total_unsafe
        - int(total_conditional * 0.5)
    )


    if status == "safe":

        reason = (
            "The linked sources contain positive "
            "evidence for swimming."
        )

    elif status == "unsafe":

        reason = (
            "The linked sources contain significant "
            "warnings about swimming hazards."
        )

    elif status == "conditional":

        reason = (
            "The linked sources indicate that swimming "
            "depends on ocean or weather conditions."
        )

    else:

        reason = (
            "The linked sources do not contain enough "
            "swimming-specific information."
        )


    return {
        "status": status,
        "score": score,
        "safe_score": total_safe,
        "unsafe_score": total_unsafe,
        "conditional_score": total_conditional,
        "reason": reason,
        "evidence": evidence
    }


# ============================================================
# SAVE
# ============================================================

def save_data(beaches):

    temp_file = OUTPUT_FILE + ".tmp"

    # Write to temporary file first.
    # This prevents a crash during json.dump from destroying
    # the previous good output file.

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            beaches,
            f,
            indent=2,
            ensure_ascii=False
        )

    # Replace old file only after writing succeeds.
    import os

    os.replace(
        temp_file,
        OUTPUT_FILE
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Load beaches
    # --------------------------------------------------------

    with open(
        INPUT_BEACHES,
        "r",
        encoding="utf-8"
    ) as f:

        beaches = json.load(f)


    # --------------------------------------------------------
    # Resume from previous output
    # --------------------------------------------------------

    if RESUME:

        try:

            with open(
                OUTPUT_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                saved_beaches = json.load(f)

            # Use the saved version so previous progress
            # isn't lost.

            beaches = saved_beaches

            print(
                f"RESUME → loaded {len(beaches):,} beaches "
                f"from {OUTPUT_FILE}"
            )

        except FileNotFoundError:

            print(
                "RESUME → no previous output found"
            )

        except json.JSONDecodeError:

            print(
                "WARNING → output file is corrupted"
            )

            print(
                "Starting from input file."
            )


    # --------------------------------------------------------
    # Load web data
    # --------------------------------------------------------

    with open(
        WEB_DATA,
        "r",
        encoding="utf-8"
    ) as f:

        web_data = json.load(f)


    total = len(beaches)

    completed = sum(
        1
        for beach in beaches.values()
        if "swimming_safety" in beach
    )

    print()
    print(
        f"TOTAL BEACHES → {total:,}"
    )

    print(
        f"ALREADY DONE → {completed:,}"
    )

    print(
        f"REMAINING → {total - completed:,}"
    )

    print()
    print(
        "Press Ctrl+C at any time to stop."
    )
    print(
        "Progress is saved after every beach."
    )
    print()


    # --------------------------------------------------------
    # Process
    # --------------------------------------------------------

    try:

        for index, (
            beach_id,
            beach
        ) in enumerate(
            beaches.items(),
            1
        ):

            # ------------------------------------------------
            # Skip completed beaches
            # ------------------------------------------------

            if (
                RESUME
                and "swimming_safety" in beach
            ):

                continue


            name = beach.get(
                "tags",
                {}
            ).get(
                "name",
                f"Beach {beach_id}"
            )

            print("=" * 70)

            print(
                f"[{index:,}/{total:,}] {name}"
            )

            print(
                f"ID → {beach_id}"
            )


            # ------------------------------------------------
            # Get URLs
            # ------------------------------------------------

            sources = web_data.get(
                str(beach_id),
                []
            )


            if not sources:

                result = {
                    "status": "unknown",
                    "score": 0,
                    "safe_score": 0,
                    "unsafe_score": 0,
                    "conditional_score": 0,
                    "reason": "No URLs available.",
                    "evidence": []
                }

            else:

                print(
                    f"URLS → {len(sources)}"
                )

                result = score_beach(
                    sources
                )


            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            beach["swimming_safety"] = result


            print(
                f"RESULT → "
                f"{result['status'].upper()}"
            )

            print(
                f"SCORE → "
                f"{result['score']}"
            )


            # ------------------------------------------------
            # CHECKPOINT
            # ------------------------------------------------

            save_data(
                beaches
            )

            print(
                f"CHECKPOINT → {OUTPUT_FILE}"
            )

            print()


    except KeyboardInterrupt:

        print()
        print("=" * 70)
        print("STOPPED BY USER")
        print("=" * 70)

        # The previous beach was already saved.
        print(
            "All completed beaches have been saved."
        )

        print(
            "Run the script again to resume."
        )

        return


    except Exception as e:

        print()
        print("=" * 70)
        print("SCRIPT FAILED")
        print("=" * 70)

        print(
            f"ERROR → {e}"
        )

        print(
            "Previously completed beaches are safe."
        )

        print(
            "Run the script again to resume."
        )

        raise


    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)

    print(
        f"Saved → {OUTPUT_FILE}"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()