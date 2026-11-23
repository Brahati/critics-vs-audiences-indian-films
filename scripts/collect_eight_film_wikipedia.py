
from pathlib import Path
import json
import time
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data/raw/wikipedia"
STAGING_DIR = ROOT / "data/staging/wikipedia"

RAW_DIR.mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)

FILMS = [
    {"film_id": "FILM_001", "film_name": "Chhaava", "wiki_title": "Chhaava"},
    {"film_id": "FILM_002", "film_name": "Coolie", "wiki_title": "Coolie (2025 film)"},
    {"film_id": "FILM_003", "film_name": "Deva", "wiki_title": "Deva (2025 film)"},
    {"film_id": "FILM_004", "film_name": "Dragon", "wiki_title": "Dragon (2025 film)"},
    {
        "film_id": "FILM_005",
        "film_name": "Kantara: A Legend - Chapter 1",
        "wiki_title": "Kantara: Chapter 1",
    },

    {
        "film_id": "FILM_006",
        "film_name": "Lokah Chapter One: Chandra",
        "wiki_title": "Lokah Chapter 1: Chandra",
    },
    {"film_id": "FILM_007", "film_name": "Saiyaara", "wiki_title": "Saiyaara (film)"},
    {
        "film_id": "FILM_008",
        "film_name": "Sitaare Zameen Par",
        "wiki_title": "Sitaare Zameen Par",
    },
]

API_BASE = "https://en.wikipedia.org/api/rest_v1/page/summary/"

HEADERS = {
    "User-Agent": (
        "EightFilmResearchProject/1.0 "
        "(academic data analysis project)"
    )
}


def main():
    session = requests.Session()
    session.headers.update(HEADERS)

    raw_responses = []
    records = []

    print("========== WIKIPEDIA COLLECTION ==========")

    for film in FILMS:
        title = film["wiki_title"]
        url = API_BASE + requests.utils.quote(title, safe="")

        print(f"\nFetching: {film['film_name']}")

        try:
            response = session.get(url, timeout=30)

            if response.status_code == 404:
                print(f"Page not found: {title}")
                records.append({
                    **film,
                    "collection_status": "not_found",
                    "api_url": url,
                })
                continue

            response.raise_for_status()
            data = response.json()

            # Preserve the original nested JSON response.
            raw_responses.append({
                "film_id": film["film_id"],
                "film_name": film["film_name"],
                "requested_title": title,
                "api_response": data,
            })

            # Flatten nested JSON using pandas.json_normalize.
            flat = pd.json_normalize(data, sep="_").to_dict(
                orient="records"
            )[0]

            flat["film_id"] = film["film_id"]
            flat["film_name"] = film["film_name"]
            flat["requested_title"] = title
            flat["collection_status"] = "success"
            flat["api_url"] = url

            records.append(flat)

            print(f"Retrieved: {data.get('title', 'Unknown title')}")
            time.sleep(1)

        except requests.RequestException as error:
            print(f"Request failed: {error}")
            records.append({
                **film,
                "collection_status": "request_failed",
                "api_url": url,
                "error": str(error),
            })

    # Save original JSON.
    raw_json_path = RAW_DIR / "eight_films_wikipedia_raw.json"
    with open(raw_json_path, "w", encoding="utf-8") as file:
        json.dump(raw_responses, file, ensure_ascii=False, indent=2)

    # Save flattened staging dataset.
    df = pd.DataFrame(records)

    staging_path = STAGING_DIR / "eight_films_wikipedia_flat.csv"
    df.to_csv(staging_path, index=False, encoding="utf-8-sig")

    print("\n========== COLLECTION SUMMARY ==========")
    print(f"Films requested: {len(FILMS)}")
    print(f"Successful responses: {(df['collection_status'] == 'success').sum()}")
    print(f"Unsuccessful responses: {(df['collection_status'] != 'success').sum()}")
    print(f"Raw JSON: {raw_json_path}")
    print(f"Flattened CSV: {staging_path}")

    if "title" in df.columns:
        print("\nRetrieved articles:")
        print(df[["film_name", "title", "description"]].to_string(index=False))


if __name__ == "__main__":
    main()
