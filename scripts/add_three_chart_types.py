
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Project root
ROOT = Path(__file__).resolve().parents[1]
CHART_DIR = ROOT / "docs" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Input files
imdb_path = ROOT / "data" / "processed" / "imdb" / "eight_films_pandas_clean.csv"
critic_path = ROOT / "data" / "processed" / "critics" / "eight_films_critic_reviews_clean.csv"

imdb = pd.read_csv(imdb_path)
critics = pd.read_csv(critic_path)

# Identify columns robustly
def find_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError(
        f"Could not find any of {candidates}. Available columns: {list(df.columns)}"
    )

film_col = find_column(imdb, ["project_film_name", "canonical_title", "primary_title"])
rating_col = find_column(imdb, ["imdb_rating", "average_rating"])
votes_col = find_column(imdb, ["imdb_votes", "num_votes"])
critic_rating_col = find_column(
    critics, ["rating_normalized", "critic_rating_normalized"]
)

# Merge audience and critic data
df = imdb.merge(
    critics[["imdb_id", critic_rating_col]],
    on="imdb_id",
    how="inner"
)

df[critic_rating_col] = pd.to_numeric(
    df[critic_rating_col], errors="coerce"
)
df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
df[votes_col] = pd.to_numeric(df[votes_col], errors="coerce")

df = df.dropna(
    subset=[film_col, rating_col, votes_col, critic_rating_col]
).copy()

plt.rcParams["figure.figsize"] = (11, 6)
plt.rcParams["axes.titlesize"] = 15
plt.rcParams["axes.labelsize"] = 11


# -------------------------------------------------
# CHART 4: DUMBBELL PLOT - CRITICS VS AUDIENCE
# -------------------------------------------------

plot_df = df.sort_values(rating_col).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(11, 6))

for i, row in plot_df.iterrows():
    audience = row[rating_col]
    critic = row[critic_rating_col]

    ax.plot(
        [audience, critic],
        [i, i],
        linewidth=2,
        alpha=0.7
    )
    ax.scatter(audience, i, s=85, label="IMDb audience" if i == 0 else "")
    ax.scatter(critic, i, s=85, marker="D",
               label="Professional critic" if i == 0 else "")

ax.set_yticks(range(len(plot_df)))
ax.set_yticklabels(plot_df[film_col])
ax.set_xlabel("Rating out of 10")
ax.set_title("Critics vs Audience: Rating Differences")
ax.set_xlim(0, 10)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.legend()
fig.tight_layout()

fig.savefig(
    CHART_DIR / "04_critics_vs_audience_dumbbell.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)


# -------------------------------------------------
# CHART 5: LOLLIPOP CHART - IMDb VOTE COUNTS
# -------------------------------------------------

plot_df = df.sort_values(votes_col).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(11, 6))

ax.hlines(
    y=range(len(plot_df)),
    xmin=0,
    xmax=plot_df[votes_col],
    linewidth=2
)
ax.scatter(
    plot_df[votes_col],
    range(len(plot_df)),
    s=100
)

ax.set_yticks(range(len(plot_df)))
ax.set_yticklabels(plot_df[film_col])
ax.set_xlabel("Number of IMDb votes")
ax.set_title("Audience Engagement Across Eight Films")
ax.grid(axis="x", linestyle="--", alpha=0.4)

for i, value in enumerate(plot_df[votes_col]):
    ax.annotate(
        f"{int(value):,}",
        (value, i),
        xytext=(7, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

fig.tight_layout()
fig.savefig(
    CHART_DIR / "05_imdb_vote_counts_lollipop.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)


# -------------------------------------------------
# CHART 6: SCATTER PLOT - RATING VS VOTE COUNTS
# -------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

ax.scatter(
    df[votes_col],
    df[rating_col],
    s=100,
    alpha=0.8
)

for _, row in df.iterrows():
    ax.annotate(
        row[film_col],
        (row[votes_col], row[rating_col]),
        xytext=(6, 6),
        textcoords="offset points",
        fontsize=8
    )

ax.set_xlabel("Number of IMDb votes")
ax.set_ylabel("IMDb audience rating (out of 10)")
ax.set_title("Relationship Between Audience Rating and Engagement")
ax.grid(linestyle="--", alpha=0.4)

fig.tight_layout()
fig.savefig(
    CHART_DIR / "06_rating_vs_vote_count_scatter.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)


print("\nTHREE ADDITIONAL CHARTS GENERATED SUCCESSFULLY!")
print(f"Output folder: {CHART_DIR}")

for filename in [
    "04_critics_vs_audience_dumbbell.png",
    "05_imdb_vote_counts_lollipop.png",
    "06_rating_vs_vote_count_scatter.png"
]:
    print(f" - {filename}")
