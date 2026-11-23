
from pathlib import Path
import pandas as pd
import re
import logging

ROOT = Path(__file__).resolve().parents[1]

BASICS_FILE = ROOT / "data/raw/imdb/title.basics.tsv.gz"
RATINGS_FILE = ROOT / "data/raw/imdb/title.ratings.tsv.gz"

STAGING_DIR = ROOT / "data/staging/imdb"
PROCESSED_DIR = ROOT / "data/processed/imdb"

STAGING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

# Candidate films and alternative IMDb title spellings.
FILMS = {
    "Chhaava": ["Chhaava"],
    "Deva": ["Deva"],
    "Saiyaara": ["Saiyaara"],
    "Dragon": ["Dragon"],
    "Coolie": ["Coolie"],
    "Sitaare Zameen Par": ["Sitaare Zameen Par", "Sitaare Zameen Par!"],
    "Kantara Chapter 1": [
        "Kantara Chapter 1",
        "Kantara A Legend Chapter 1",
        "Kantara: A Legend - Chapter 1"
    ],
    "Lokah Chapter One Chandra": [
        "Lokah Chapter One Chandra",
        "Lokah Chapter 1 Chandra",
        "Lokah Chapter One: Chandra"
    ]
}


def normalize(value):
    """Normalize titles for matching."""
    value = str(value).lower()
    return re.sub(r"[^a-z0-9]", "", value)


def main():
    if not BASICS_FILE.exists() or not RATINGS_FILE.exists():
        raise FileNotFoundError("IMDb source datasets are missing.")

    aliases = {
        normalize(alias): film
        for film, names in FILMS.items()
        for alias in names
    }

    matched_rows = []

    logging.info("Scanning IMDb title basics dataset...")

    columns = [
        "tconst", "titleType", "primaryTitle",
        "originalTitle", "startYear",
        "runtimeMinutes", "genres"
    ]

    for chunk in pd.read_csv(
        BASICS_FILE,
        sep="\t",
        compression="gzip",
        usecols=columns,
        dtype=str,
        chunksize=250_000,
        na_values="\\N"
    ):
        chunk = chunk[
            (chunk["titleType"] == "movie") &
            (chunk["startYear"] == "2025")
        ]

        for _, row in chunk.iterrows():
            primary = normalize(row["primaryTitle"])
            original = normalize(row["originalTitle"])

            film = aliases.get(primary) or aliases.get(original)

            if film:
                record = row.to_dict()
                record["project_film_name"] = film
                matched_rows.append(record)

    if not matched_rows:
        raise RuntimeError(
            "No matching films found. Check IMDb title spellings."
        )

    matches = pd.DataFrame(matched_rows)

    matches.to_csv(
        STAGING_DIR / "eight_films_title_matches.csv",
        index=False
    )

    logging.info("Loading IMDb ratings dataset...")

    ratings = pd.read_csv(
        RATINGS_FILE,
        sep="\t",
        compression="gzip",
        dtype={"tconst": str},
        na_values="\\N"
    )

    result = matches.merge(
        ratings,
        on="tconst",
        how="left"
    )

    result = result.rename(columns={
        "tconst": "imdb_id",
        "primaryTitle": "primary_title",
        "originalTitle": "original_title",
        "startYear": "release_year",
        "runtimeMinutes": "runtime_minutes",
        "genres": "genres",
        "averageRating": "imdb_rating",
        "numVotes": "imdb_votes"
    })

    result["release_year"] = pd.to_numeric(
        result["release_year"], errors="coerce"
    )
    result["runtime_minutes"] = pd.to_numeric(
        result["runtime_minutes"], errors="coerce"
    )
    result["imdb_rating"] = pd.to_numeric(
        result["imdb_rating"], errors="coerce"
    )
    result["imdb_votes"] = pd.to_numeric(
        result["imdb_votes"], errors="coerce"
    )

    output_columns = [
        "project_film_name",
        "imdb_id",
        "primary_title",
        "original_title",
        "release_year",
        "runtime_minutes",
        "genres",
        "imdb_rating",
        "imdb_votes"
    ]

    result = result[output_columns].sort_values(
        ["project_film_name", "imdb_votes"],
        ascending=[True, False]
    )

    output_file = PROCESSED_DIR / "eight_films_imdb.csv"
    result.to_csv(output_file, index=False)

    found = set(result["project_film_name"].dropna())
    missing = set(FILMS) - found

    print("\n========== IMDb COLLECTION RESULTS ==========")
    print(result.to_string(index=False))
    print(f"\nMatched film names: {len(found)} / {len(FILMS)}")

    if missing:
        print("\nFilms requiring manual matching:")
        for film in sorted(missing):
            print("-", film)

    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()
