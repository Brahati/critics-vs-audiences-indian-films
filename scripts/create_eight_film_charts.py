
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
ROOT = Path(__file__).resolve().parents[1]

IMDB_FILE = ROOT / "data/processed/imdb/eight_films_pandas_clean.csv"
CRITICS_FILE = ROOT / "data/processed/critics/eight_films_critic_reviews_clean.csv"

CHART_DIR = ROOT / "docs/charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
imdb = pd.read_csv(IMDB_FILE)
critics = pd.read_csv(CRITICS_FILE)

# Merge audience and critic ratings using IMDb ID
merged = imdb.merge(
    critics[["imdb_id", "rating_normalized", "publication"]],
    on="imdb_id",
    how="inner"
)

merged = merged.sort_values("imdb_rating", ascending=True)

# Save merged chart data for reproducibility
merged.to_csv(CHART_DIR / "critics_vs_audience_chart_data.csv", index=False)

# -------------------------------------------------
# CHART 1: Critics vs Audience Ratings
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7))

y = range(len(merged))
height = 0.36

ax.barh(
    [i - height / 2 for i in y],
    merged["imdb_rating"],
    height=height,
    label="IMDb Audience Rating"
)

ax.barh(
    [i + height / 2 for i in y],
    merged["rating_normalized"],
    height=height,
    label="Critic Rating (one review per film)"
)

ax.set_yticks(list(y))
ax.set_yticklabels(merged["project_film_name"])
ax.set_xlim(0, 10)
ax.set_xlabel("Rating (out of 10)")
ax.set_title("Critics vs Audience Ratings: Eight Indian Films (2025)")
ax.legend()
ax.grid(axis="x", alpha=0.25)

fig.text(
    0.5, 0.01,
    "Source: IMDb aggregate ratings and one collected critic review per film. "
    "Descriptive comparison, not a representative critic consensus.",
    ha="center", fontsize=8, wrap=True
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(CHART_DIR / "01_critics_vs_audience.png", dpi=300)
plt.close()

# -------------------------------------------------
# CHART 2: IMDb Audience Engagement
# -------------------------------------------------
votes = imdb.sort_values("imdb_votes", ascending=True)

fig, ax = plt.subplots(figsize=(12, 7))

bars = ax.barh(
    votes["project_film_name"],
    votes["imdb_votes"]
)

ax.set_xlabel("Number of IMDb Votes")
ax.set_title("Audience Engagement Across Eight Indian Films (2025)")
ax.grid(axis="x", alpha=0.25)

for bar, value in zip(bars, votes["imdb_votes"]):
    ax.text(
        bar.get_width() + 500,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,}",
        va="center",
        fontsize=8
    )

plt.tight_layout()
plt.savefig(CHART_DIR / "02_imdb_vote_counts.png", dpi=300)
plt.close()

# -------------------------------------------------
# CHART 3: Genre-wise IMDb Ratings
# -------------------------------------------------
genre_data = imdb.assign(
    genre=imdb["genres"].str.split(",")
).explode("genre")

genre_data["genre"] = genre_data["genre"].str.strip()

genre_summary = (
    genre_data.groupby("genre")
    .agg(
        average_rating=("imdb_rating", "mean"),
        film_count=("project_film_name", "nunique")
    )
    .reset_index()
    .sort_values("average_rating")
)

genre_summary.to_csv(
    CHART_DIR / "genre_rating_summary.csv",
    index=False
)

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    genre_summary["genre"],
    genre_summary["average_rating"]
)

ax.set_xlim(0, 10)
ax.set_xlabel("Average IMDb Rating (out of 10)")
ax.set_title("Genre-wise Audience Ratings")
ax.grid(axis="x", alpha=0.25)

for bar, rating, count in zip(
    bars,
    genre_summary["average_rating"],
    genre_summary["film_count"]
):
    ax.text(
        rating + 0.08,
        bar.get_y() + bar.get_height() / 2,
        f"{rating:.2f} ({count} films)",
        va="center",
        fontsize=8
    )

plt.tight_layout()
plt.savefig(CHART_DIR / "03_genre_wise_ratings.png", dpi=300)
plt.close()

print("\nALL THREE CHARTS GENERATED SUCCESSFULLY!")
print("Chart directory:", CHART_DIR)

print("\nCRITICS VS AUDIENCE DATA:")
print(
    merged[
        ["project_film_name", "imdb_rating", "rating_normalized"]
    ].to_string(index=False)
)

print("\nGENRE SUMMARY:")
print(genre_summary.to_string(index=False))
