
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data/staging/wikipedia/eight_films_wikipedia_flat.csv"
OUTPUT = ROOT / "data/processed/wikipedia/eight_films_wikipedia_clean.csv"
LOG = ROOT / "docs/eight_film_wikipedia_cleaning_log.md"

def main():
    df = pd.read_csv(INPUT)
    initial_rows = len(df)
    actions = []

    # Remove duplicate film records.
    duplicates = int(df["film_id"].duplicated().sum())
    df = df.drop_duplicates(subset=["film_id"], keep="first")
    actions.append(f"Removed {duplicates} duplicate film records.")

    # Check collection status.
    if "collection_status" in df.columns:
        failed = int((df["collection_status"] != "success").sum())
        actions.append(f"Records with unsuccessful API status: {failed}.")
        df = df[df["collection_status"] == "success"].copy()

    # Normalize text fields.
    text_columns = [
        "film_name", "title", "description", "extract",
        "requested_title", "api_url"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
            df[col] = df[col].replace("", pd.NA)

    # Convert page ID to numeric where available.
    if "pageid" in df.columns:
        df["pageid"] = pd.to_numeric(df["pageid"], errors="coerce")

    # Identify missing values.
    missing_summary = df.isna().sum()
    actions.append(
        "Standardized text fields by trimming whitespace and "
        "converting empty strings to missing values."
    )
    actions.append(
        "Converted pageid to numeric where the field was available."
    )

    # Preserve the API extract as unstructured text.
    if "extract" in df.columns:
        missing_extracts = int(df["extract"].isna().sum())
        actions.append(
            f"Missing article extracts: {missing_extracts}."
        )

    # Save cleaned data.
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    # Create cleaning log.
    log = [
        "# Wikipedia Dataset Cleaning Log",
        "",
        f"- Input rows: {initial_rows}",
        f"- Output rows: {len(df)}",
        f"- Rows removed: {initial_rows - len(df)}",
        "",
        "## Cleaning actions",
        "",
    ]

    log.extend(f"- {action}" for action in actions)

    log.extend([
        "",
        "## Missing-value summary",
        "",
        "| Column | Missing values |",
        "|---|---:|",
    ])

    for column, count in missing_summary.items():
        log.append(f"| {column} | {count} |")

    log.extend([
        "",
        "## Data handling decisions",
        "",
        "- Original API JSON is preserved separately.",
        "- Flattened API fields are retained in the cleaned CSV.",
        "- Missing descriptions or extracts are not fabricated.",
        "- Article extracts are retained as text for later analysis.",
        "",
    ])

    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(log), encoding="utf-8")

    print("========== WIKIPEDIA CLEANING ==========")
    print(f"Input rows: {initial_rows}")
    print(f"Output rows: {len(df)}")
    print(f"Cleaned file: {OUTPUT}")
    print(f"Cleaning log: {LOG}")

    display_columns = [
        col for col in ["film_name", "title", "description", "pageid"]
        if col in df.columns
    ]

    print("\nCleaned records:")
    print(df[display_columns].to_string(index=False))

if __name__ == "__main__":
    main()
