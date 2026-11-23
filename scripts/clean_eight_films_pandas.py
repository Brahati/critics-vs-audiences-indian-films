
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data/processed/imdb/eight_films_imdb.csv"
OUTPUT_FILE = ROOT / "data/processed/imdb/eight_films_pandas_clean.csv"
LOG_FILE = ROOT / "docs/eight_films_pandas_cleaning_log.csv"

# Load original data
df = pd.read_csv(INPUT_FILE, dtype={"imdb_id": "string"})

initial_rows = len(df)

# 1. Remove duplicate records
df = df.drop_duplicates()

# 2. Remove leading/trailing whitespace from text columns
text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# 3. Convert numeric columns
numeric_columns = [
    "release_year",
    "runtime_minutes",
    "imdb_rating",
    "imdb_votes"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 4. Check missing values
missing_values = int(df.isnull().sum().sum())

# 5. Validate ratings
invalid_ratings = int(
    (~df["imdb_rating"].between(0, 10)).sum()
)

# 6. Validate vote counts
invalid_votes = int((df["imdb_votes"] < 0).sum())

# 7. Save cleaned dataset
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

# 8. Generate cleaning log
log = pd.DataFrame([
    ["Duplicate check", "Duplicates removed", initial_rows - len(df)],
    ["Whitespace cleaning", "Text fields trimmed", "Applied"],
    ["Numeric conversion", "Numeric columns converted", "Applied"],
    ["Missing values", "Total missing values after cleaning", missing_values],
    ["Rating validation", "Invalid IMDb ratings", invalid_ratings],
    ["Vote validation", "Invalid vote counts", invalid_votes],
    ["Final row count", "Records retained", len(df)]
], columns=["Operation", "Description", "Result"])

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
log.to_csv(LOG_FILE, index=False)

print("PANDAS CLEANING COMPLETED")
print("--------------------------------")
print(f"Initial records: {initial_rows}")
print(f"Final records: {len(df)}")
print(f"Missing values: {missing_values}")
print(f"Invalid ratings: {invalid_ratings}")
print(f"Invalid vote counts: {invalid_votes}")
print(f"\nCleaned file: {OUTPUT_FILE}")
print(f"Cleaning log: {LOG_FILE}")
print("\nData types:")
print(df.dtypes)
