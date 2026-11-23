
from pathlib import Path
import pandas as pd
import logging

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data/raw/critics"
STAGING_DIR = ROOT / "data/staging/critics"

RAW_DIR.mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)

COLLECTION_DATE = "2026-11-23"

# IMDb IDs are taken from our locally matched IMDb dataset.
REVIEWS = [
    {
        "review_id": "CRITIC_001",
        "film_id": "FILM_001",
        "film_name": "Chhaava",
        "imdb_id": "tt27922706",
        "publication": "The Indian Express",
        "critic_name": "Shubhra Gupta",
        "review_date": "2025-02-14",
        "rating_raw": "2.5/5",
        "rating_scale": "5",
        "review_url": "https://indianexpress.com/article/entertainment/movie-review/chhaava-movie-review-vicky-kaushal-in-fully-committed-laxman-utekars-ultra-loud-ultra-violent-and-exhausting-film-9835599/",
        "source_id": "CRITICS_INDIANEXPRESS"
    },
    {
        "review_id": "CRITIC_002",
        "film_id": "FILM_002",
        "film_name": "Coolie",
        "imdb_id": "tt27441481",
        "publication": "The Indian Express",
        "critic_name": "Arjun Menon",
        "review_date": "2025-08-14",
        "rating_raw": "2.5/5",
        "rating_scale": "5",
        "review_url": "https://indianexpress.com/article/entertainment/movie-review/coolie-movie-review-rajinikanth-elevates-lokesh-kanagarajs-frustrating-action-vehicle-10188565/",
        "source_id": "CRITICS_INDIANEXPRESS"
    },
    {
        "review_id": "CRITIC_003",
        "film_id": "FILM_003",
        "film_name": "Deva",
        "imdb_id": "tt27852049",
        "publication": "The Times of India",
        "critic_name": "Dhaval Roy",
        "review_date": "2025-01-31",
        "rating_raw": "3.5/5",
        "rating_scale": "5",
        "review_url": "https://timesofindia.indiatimes.com/entertainment/hindi/movie-reviews/deva/movie-review/117782878.cms",
        "source_id": "CRITICS_TOI"
    },
    {
        "review_id": "CRITIC_004",
        "film_id": "FILM_004",
        "film_name": "Dragon",
        "imdb_id": "tt32080876",
        "publication": "The Times of India",
        "critic_name": "TNN",
        "review_date": "2025-02-21",
        "rating_raw": "4/5",
        "rating_scale": "5",
        "review_url": "https://timesofindia.indiatimes.com/entertainment/tamil/movie-reviews/dragon/movie-review/118443297.cms",
        "source_id": "CRITICS_TOI"
    },
    {
        "review_id": "CRITIC_005",
        "film_id": "FILM_005",
        "film_name": "Kantara: A Legend - Chapter 1",
        "imdb_id": "tt26439764",
        "publication": "Hindustan Times",
        "critic_name": "Abhimanyu Mathur",
        "review_date": "2025-10-02",
        "rating_raw": "3/5",
        "rating_scale": "5",
        "review_url": "https://www.hindustantimes.com/entertainment/others/kantara-chapter-1-review-folk-goes-mass-as-rishab-shetty-rukmini-vasanth-excel-in-uneven-but-visually-splendid-prequel-101759390665616.html",
        "source_id": "CRITICS_HT"
    },
    {
        "review_id": "CRITIC_006",
        "film_id": "FILM_006",
        "film_name": "Lokah Chapter One: Chandra",
        "imdb_id": "tt33372494",
        "publication": "The Indian Express",
        "critic_name": "Anandu Suresh",
        "review_date": "2025-09-03",
        "rating_raw": "4/5",
        "rating_scale": "5",
        "review_url": "https://indianexpress.com/article/entertainment/movie-review/lokah-chapter-1-review-kalyani-priyadarshan-naslen-deliver-one-of-indian-cinemas-finest-superhero-films-10215021/",
        "source_id": "CRITICS_INDIANEXPRESS"
    },
    {
        "review_id": "CRITIC_007",
        "film_id": "FILM_007",
        "film_name": "Saiyaara",
        "imdb_id": "tt28037987",
        "publication": "The Indian Express",
        "critic_name": "Shubhra Gupta",
        "review_date": "2025-07-18",
        "rating_raw": "2/5",
        "rating_scale": "5",
        "review_url": "https://indianexpress.com/article/entertainment/movie-review/saiyaara-movie-review-aneet-padda-ahaan-panday-show-spark-but-this-is-no-aashiqui-3-10134555/",
        "source_id": "CRITICS_INDIANEXPRESS"
    },
    {
        "review_id": "CRITIC_008",
        "film_id": "FILM_008",
        "film_name": "Sitaare Zameen Par",
        "imdb_id": "tt27235410",
        "publication": "The Times of India",
        "critic_name": "Dhaval Roy",
        "review_date": "2025-06-20",
        "rating_raw": "3.5/5",
        "rating_scale": "5",
        "review_url": "https://timesofindia.indiatimes.com/entertainment/hindi/movie-reviews/sitaare-zameen-par/movie-review/121968627.cms",
        "source_id": "CRITICS_TOI"
    }
]

df = pd.DataFrame(REVIEWS)

# Normalize published ratings to a common 10-point scale.
df["rating_normalized"] = (
    df["rating_raw"]
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
    .astype(float)
    / 5 * 10
)

df["review_text"] = ""
df["collection_date"] = COLLECTION_DATE
df["collection_method"] = "manual_source_verification"

columns = [
    "review_id", "film_id", "film_name", "imdb_id",
    "publication", "critic_name", "review_date",
    "rating_raw", "rating_scale", "rating_normalized",
    "review_text", "review_url", "collection_date",
    "collection_method", "source_id"
]

df = df[columns]

raw_file = RAW_DIR / "eight_films_critic_reviews.csv"
staging_file = STAGING_DIR / "eight_films_critic_reviews.csv"

df.to_csv(raw_file, index=False, encoding="utf-8")
df.to_csv(staging_file, index=False, encoding="utf-8")

print("========== CRITIC COLLECTION ==========")
print(f"Reviews prepared: {len(df)}")
print(f"Distinct films: {df['film_id'].nunique()}")
print(f"Raw file: {raw_file}")
print(f"Staging file: {staging_file}")
print("\nReview ratings:")
print(df[["film_name", "publication", "rating_raw",
          "rating_normalized"]].to_string(index=False))
print("\nReview excerpts are intentionally blank pending source capture.")
