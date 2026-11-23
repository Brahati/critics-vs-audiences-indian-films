# Limitations — Toxic 2026 Movie Data Pipeline

**Project ID:** TOXIC_2026 | **IMDb ID:** tt27530512  
**Version:** 1.0 | **Date:** 2026-11-20

---

## 1. Critics Data Limitations

### 1.1 No public scraping API
No major film review aggregator (Rotten Tomatoes, Metacritic, Letterboxd) provides
a public API for academic scraping. Rotten Tomatoes (Fandango) explicitly prohibits
automated bots, spiders, and data extractors in its Terms of Service. All critic data
in this project must be entered manually.

### 1.2 Automated scraping prohibited
Every source identified for this film (The Hindu, NDTV, THR India, Galatta Plus,
IGN, Hindustan Times, Indian Express, Firstpost, Deccan Chronicle) prohibits
automated reproduction of content in its Terms of Service or robots.txt. The manual
collection workflow respects these restrictions.

### 1.3 Paywall restrictions
Some publications (e.g. The Hindu in certain regions) may require a subscription
to access the full review text. Paywalled reviews where full text is inaccessible
are excluded; only publicly accessible text is transcribed.

### 1.4 Sample size
Target: 10–20 reviews. This is a small sample determined entirely by the number
of publicly accessible, manually collectible reviews — not a statistical sample.
No reviews are invented to meet a quota.

### 1.5 Language
All confirmed reviews are in English. Kannada, Hindi, or other-language reviews
may exist but are not included in this iteration because translation is outside
the scope of this data engineering project.

### 1.6 Rotten Tomatoes Tomatometer
The RT film page exists and shows approximately 21% Tomatometer at the time of
research (2026-11-20). However, RT's methodology (what qualifies as a "fresh"
review, which publications are eligible) is not fully transparent. The aggregate
percentage is noted in source_register.csv but is not loaded as individual
review data because individual RT critic reviews are not accessible via API.

### 1.7 Rating scale heterogeneity
Different publications use different scales (5-star, 4-star, 10-point, prose only).
Ratings are normalised to 0–10 only when the original scale is known and documented.
Where the scale is ambiguous or absent, `rating_normalized` is NULL.

### 1.8 Manual entry errors
Transcription of review text and ratings by a human researcher introduces the
possibility of typographical errors. Each row in the manual template should be
verified against the original URL.

---

## 2. IMDb Data Limitations

### 2.1 Aggregate rating only
The IMDb Non-Commercial Datasets provide only the aggregate weighted average
rating (`averageRating`) and vote count (`numVotes`). Individual user review
text is not available via the official datasets. Scraping IMDb review pages
is explicitly prohibited.

### 2.2 Low vote count for new release
As of the collection date (2026-11-20), the film was released in 2026 and may
have a relatively small number of votes. IMDb requires a minimum number of votes
before a rating appears in `title.ratings.tsv.gz`. If the minimum threshold has
not been reached, `average_rating` and `num_votes` will be NULL.

### 2.3 Non-commercial use restriction
The IMDb Non-Commercial Datasets are licensed for personal and non-commercial
use only. This project must not use the data for commercial purposes. Attribution
is required: "Information courtesy of IMDb (https://www.imdb.com). Used with permission."

### 2.4 Snapshot-only data
Each download captures a point-in-time snapshot. The rating and vote count will
change over time. The dataset download timestamp is preserved in every record.
Multiple snapshots over time are stored to track changes.

### 2.5 No demographic breakdown
IMDb does not provide vote breakdowns by age, gender, region, or other demographics
in the non-commercial datasets.

---

## 3. Reddit Data Limitations

### 3.1 OAuth credentials required
Reddit API v2 (post-2023 policy) requires a registered developer application and
OAuth2 credentials. The collector script will not run without these credentials.
Contact: https://www.reddit.com/prefs/apps to register.

### 3.2 Academic access is not instant
Reddit's academic/research access program requires a formal application, description
of use case, and institutional documentation. Approval is not guaranteed and not
instantaneous.

### 3.3 Pushshift is fully shut down
Pushshift, previously used for bulk historical Reddit data, is **no longer publicly
accessible** as of mid-2023. It is now restricted to Reddit's internal moderation
tools. PSAW (the Python wrapper for Pushshift) is therefore also non-functional.
Alternative: Arctic Shift (community-maintained) may provide some historical data
but is not an official Reddit product and its availability and terms are uncertain.

### 3.4 Historical data incompleteness
PRAW's real-time search API does not guarantee complete coverage of all historical
posts. Some relevant threads may not appear in search results. Coverage is limited
to the date range from Reddit app registration onwards in terms of real-time retrieval.

### 3.5 Deleted and removed content
Reddit posts and comments that have been deleted by users or removed by moderators
are irrecoverable. These are captured as `is_deleted = 1` with `comment_text = NULL`.
The rate of deletion/removal creates a non-random gap in the dataset — controversial
content is more likely to be removed.

### 3.6 Subreddit scope
Only English-language subreddits (r/bollywood, r/tollywood, r/india, r/movies,
r/worldcinema, r/netflix) are searched. South Indian language-specific communities
are not included.

### 3.7 No usernames collected
Reddit usernames are intentionally not collected or stored, consistent with privacy
best practices for academic research. This means user-level analysis (tracking the
same user across posts) is not possible.

### 3.8 Rate limits
Reddit API free tier: 100 QPM (queries per minute). The collector script enforces
a configurable delay between requests (default: 2 seconds). Large collections
may take several hours.

---

## 4. General Limitations

### 4.1 Data engineering only
This project is a data engineering case study. No sentiment analysis, topic
modelling, opinion mining, visualisation, or conclusions about the film are
drawn from the data.

### 4.2 Data completeness
The dataset is **not** complete. Critics data depends on manual entry; Reddit
data requires credentials; IMDb data may show NULL ratings for a new release.
The final delivery status of each component is documented in `docs/data_quality_report.md`.

### 4.3 Temporal dependency
Data collection is a point-in-time operation. Ratings, vote counts, and Reddit
discussion volume change continuously. All records include retrieval timestamps
to make this explicit.

### 4.4 Film identity ambiguity
"Toxic" is not a unique film title. All records must be verified against
`imdb_id = tt27530512`. Records matched only on the word "Toxic" are flagged
`match_status = 'ambiguous'` and excluded from the main dataset.

### 4.5 English-language bias
Most collected data (all critic reviews, all Reddit posts) is in English.
This may under-represent the views of non-English-speaking audiences, including
the film's core Kannada-speaking audience.
