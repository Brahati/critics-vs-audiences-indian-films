
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data/staging/critics/eight_films_critic_reviews.csv"
OUTPUT = ROOT / "data/processed/critics/eight_films_critic_reviews_clean.csv"
LOG = ROOT / "docs/eight_film_cleaning_log.md"

REQUIRED_COLUMNS = [
    "review_id",
    "film_id",
    "film_name",
    "publication",
    "critic_name",
    "review_date",
    "rating_raw",
    "rating_scale",
    "rating_normalized",
    "review_url",
]

def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT}")

    df = pd.read_csv(INPUT)
    initial_rows = len(df)
    actions = []

    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Remove duplicate review records.
    duplicate_count = int(df["review_id"].duplicated().sum())
    df = df.drop_duplicates(subset=["review_id"], keep="first")
    actions.append(f"Removed {duplicate_count} duplicate review IDs.")

    # Convert dates.
    df["review_date"] = pd.to_datetime(
        df["review_date"], errors="coerce"
    )
    invalid_dates = int(df["review_date"].isna().sum())
    actions.append(f"Invalid or missing review dates: {invalid_dates}.")

    # Convert rating fields to numeric.
    df["rating_scale"] = pd.to_numeric(
        df["rating_scale"], errors="coerce"
    )
    df["rating_normalized"] = pd.to_numeric(
        df["rating_normalized"], errors="coerce"
    )

    invalid_ratings = (
        df["rating_normalized"].isna()
        | (df["rating_normalized"] < 0)
        | (df["rating_normalized"] > 10)
    )
    invalid_rating_count = int(invalid_ratings.sum())

    # Recalculate normalized ratings from the raw rating and scale.
    parsed_rating = df["rating_raw"].astype(str).str.extract(
        r"(\d+(?:\.\d+)?)"
    )[0]
    parsed_rating = pd.to_numeric(parsed_rating, errors="coerce")

    valid_scale = df["rating_scale"].gt(0)
    valid_rating = parsed_rating.notna() & valid_scale

    df.loc[valid_rating, "rating_normalized"] = (
        parsed_rating[valid_rating]
        / df.loc[valid_rating, "rating_scale"]
        * 10
    )

    actions.append(
        f"Found {invalid_rating_count} invalid normalized ratings "
        "before recalculation."
    )
    actions.append(
        "Recalculated normalized ratings on a 0–10 scale using "
        "the raw rating divided by its original scale."
    )

    # Preserve missing review excerpts; do not fabricate text.
    if "review_text" in df.columns:
        missing_text = int(
            df["review_text"].isna().sum()
            + df["review_text"].astype(str).str.strip().eq("").sum()
        )
        actions.append(
            f"Review text is blank for {missing_text} rows; "
            "left missing rather than inventing excerpts."
        )

    # Standardize text fields.
    for col in ["film_name", "publication", "critic_name"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Retain rows with valid normalized ratings.
    before_filter = len(df)
    df = df[
        df["rating_normalized"].notna()
        & df["rating_normalized"].between(0, 10)
    ].copy()
    removed = before_filter - len(df)
    actions.append(f"Removed {removed} rows with invalid final ratings.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)

    LOG.parent.mkdir(parents=True, exist_ok=True)
    log_text = [
        "# Eight-Film Study: Critic Dataset Cleaning Log",
        "",
        f"- Input rows: {initial_rows}",
        f"- Output rows: {len(df)}",
        f"- Rows removed: {initial_rows - len(df)}",
        "",
        "## Cleaning actions",
        "",
    ]
    log_text.extend(f"- {action}" for action in actions)
    log_text.extend([
        "",
        "## Missing-data decision",
        "",
        "Blank review excerpts are retained as missing values. "
        "No review text has been fabricated.",
        "",
    ])
    LOG.write_text("\n".join(log_text), encoding="utf-8")

    print("========== CRITIC CLEANING ==========")
    print(f"Input rows: {initial_rows}")
    print(f"Output rows: {len(df)}")
    print(f"Output file: {OUTPUT}")
    print(f"Cleaning log: {LOG}")
    print("\nCleaned ratings:")
    print(
        df[["film_name", "publication", "rating_raw",
            "rating_normalized"]].to_string(index=False)
    )

if __name__ == "__main__":
    main()
