import json
import re
import os

INPUT_FILE = "searxng.json"
OUTPUT_FILE = "searxng_cleaned.json"


def normalize(text):
    """Normalize text for reliable matching."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_beach_name(beach):
    return beach.get(
        "tags",
        {}
    ).get(
        "name",
        ""
    ).strip()


def source_mentions_beach(source, beach_name):
    """
    Keep the source only if the exact beach name
    appears in its title or content.
    """

    name = normalize(beach_name)

    title = normalize(
        source.get("title", "")
    )

    content = normalize(
        source.get("content", "")
    )

    return (
        name in title
        or name in content
    )


def main():

    # --------------------------------------------------------
    # Load beach database
    # --------------------------------------------------------

    with open(
        "beaches.json",
        "r",
        encoding="utf-8"
    ) as f:

        beaches_data = json.load(f)

    beaches = beaches_data["elements"]


    # --------------------------------------------------------
    # Load existing web data
    # --------------------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        web_data = json.load(f)


    cleaned = {}

    total_sources = 0
    removed_sources = 0
    kept_sources = 0


    # --------------------------------------------------------
    # Clean each beach
    # --------------------------------------------------------

    for beach_id, sources in web_data.items():

        beach = next(
            (
                b
                for b in beaches
                if str(b.get("id")) == str(beach_id)
            ),
            None
        )

        if beach is None:

            print(
                f"WARNING → Beach {beach_id} "
                f"not found in beaches.json"
            )

            continue


        beach_name = get_beach_name(
            beach
        )

        print(
            f"\n{beach_id} → {beach_name}"
        )


        kept = []

        for source in sources:

            total_sources += 1

            if source_mentions_beach(
                source,
                beach_name
            ):

                kept.append(source)
                kept_sources += 1

                print(
                    f"  KEEP → "
                    f"{source.get('title', '')}"
                )

            else:

                removed_sources += 1

                print(
                    f"  REMOVE → "
                    f"{source.get('title', '')}"
                )


        cleaned[str(beach_id)] = kept


    # --------------------------------------------------------
    # Save safely
    # --------------------------------------------------------

    temp_file = OUTPUT_FILE + ".tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned,
            f,
            indent=2,
            ensure_ascii=False
        )

    os.replace(
        temp_file,
        OUTPUT_FILE
    )


    # --------------------------------------------------------
    # Stats
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)

    print(
        f"Total sources → {total_sources:,}"
    )

    print(
        f"Kept → {kept_sources:,}"
    )

    print(
        f"Removed → {removed_sources:,}"
    )

    print(
        f"Saved → {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()