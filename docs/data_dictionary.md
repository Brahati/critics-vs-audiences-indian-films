# Data Dictionary — Toxic 2026 Movie Data Pipeline

**Project ID:** TOXIC_2026 | **IMDb ID:** tt27530512  
**Version:** 1.0 | **Date:** 2026-11-20

---

## 1. MySQL Tables

### 1.1 `films`

Canonical film identity record. One row per film; this project has exactly one row.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `film_id` | VARCHAR(50) | NO | Primary key. `TOXIC_2026` for this project. |
| `imdb_id` | VARCHAR(20) | NO | IMDb title identifier. Must be `tt27530512`. Unique. |
| `canonical_title` | VARCHAR(500) | NO | Authoritative title: "Toxic: A Fairytale for Grown-Ups". |
| `primary_title` | VARCHAR(500) | YES | IMDb `primaryTitle` field value (populated from IMDb snapshot). |
| `original_title` | VARCHAR(500) | YES | IMDb `originalTitle` field value. |
| `release_year` | SMALLINT | YES | Release year from IMDb (`startYear`). `2026`. |
| `director` | VARCHAR(255) | YES | Director name. `Geetu Mohandas`. |
| `starring` | VARCHAR(500) | YES | Lead actor(s). `Yash`. |
| `genres` | VARCHAR(255) | YES | Comma-separated genres from IMDb. |
| `runtime_minutes` | SMALLINT | YES | Running time in minutes from IMDb. |
| `created_at` | TIMESTAMP | NO | Row creation timestamp (auto). |
| `updated_at` | TIMESTAMP | NO | Row last-updated timestamp (auto). |

---

### 1.2 `critic_reviews`

One row per professional critic review of the film.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `review_id` | VARCHAR(100) | NO | Primary key. Format: `{SOURCE_ID}_{NN}`, e.g. `CRITICS_THEHINDU_01`. |
| `film_id` | VARCHAR(50) | NO | Foreign key → `films.film_id`. Always `TOXIC_2026`. |
| `publication` | VARCHAR(255) | YES | Name of the publication, e.g. `The Hindu`. |
| `critic_name` | VARCHAR(255) | YES | Name of the critic, e.g. `Vivek M.V.`. NULL only if unknown. |
| `review_date` | DATE | YES | Date the review was published. NULL if unknown. |
| `rating_raw` | VARCHAR(50) | YES | Rating exactly as it appears in the source, e.g. `3`, `3/5`, `B+`. NULL if no rating. |
| `rating_scale` | VARCHAR(50) | YES | Rating scale identifier: `5star`, `4star`, `10point`, `100point`, `lettergrade`. NULL if unknown. |
| `rating_normalized` | DECIMAL(5,2) | YES | Rating normalised to 0–10 scale. NULL if `rating_scale` is unknown or not normalisable. **Never inferred from review text.** |
| `review_text` | LONGTEXT | YES | Full review text as entered manually. NULL if unavailable. |
| `review_url` | VARCHAR(1000) | YES | Direct URL to the original review page. |
| `collection_date` | DATE | YES | Date the row was entered into the template. |
| `collection_method` | VARCHAR(100) | YES | Always `manual_entry` for this project. |
| `source_id` | VARCHAR(50) | YES | Corresponds to `source_register.source_id`. |
| `match_status` | VARCHAR(50) | YES | `verified`, `ambiguous`. Records with `ambiguous` are not loaded into MySQL without manual review. |
| `created_at` | TIMESTAMP | NO | Row creation timestamp (auto). |

**Rating normalisation rules:**

| `rating_scale` | Normalisation formula |
|---|---|
| `5star` | `(raw / 5) × 10` |
| `4star` | `(raw / 4) × 10` |
| `10point` | `raw` (no change) |
| `100point` | `raw / 10` |
| `lettergrade` | Not normalised — `rating_normalized` = NULL |
| NULL / unknown | Not normalised — `rating_normalized` = NULL |

---

### 1.3 `imdb_snapshots`

Each run of `download_imdb.py` appends one row. Historical snapshots are never overwritten.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `snapshot_id` | INT AUTO_INCREMENT | NO | Primary key. |
| `film_id` | VARCHAR(50) | NO | Foreign key → `films.film_id`. |
| `imdb_id` | VARCHAR(20) | NO | `tt27530512`. |
| `average_rating` | DECIMAL(3,1) | YES | Weighted average rating on 1.0–10.0 scale. NULL if film has fewer than the IMDb minimum vote threshold. |
| `num_votes` | INT | YES | Total number of votes at download time. NULL if below threshold. |
| `primary_title` | VARCHAR(500) | YES | From `title.basics.tsv.gz`. |
| `original_title` | VARCHAR(500) | YES | From `title.basics.tsv.gz`. |
| `release_year` | SMALLINT | YES | From `startYear` in `title.basics.tsv.gz`. |
| `genres` | VARCHAR(255) | YES | Comma-separated genres. |
| `runtime_minutes` | SMALLINT | YES | From `runtimeMinutes`. NULL = `\N` in source. |
| `source_file_basics` | VARCHAR(255) | YES | Filename of the basics file used (e.g. `title.basics.tsv.gz`). |
| `source_file_ratings` | VARCHAR(255) | YES | Filename of the ratings file used. NULL if no ratings record found. |
| `dataset_download_timestamp` | DATETIME | YES | UTC timestamp when download was initiated. |
| `retrieval_timestamp` | DATETIME | YES | UTC timestamp when the record was extracted. |
| `created_at` | TIMESTAMP | NO | Row creation timestamp (auto). |

> **Note:** `average_rating` is an aggregate — it does not represent any individual user's rating.
> Individual IMDb user review text is **not** available via the official non-commercial datasets.

---

### 1.4 `reddit_posts`

One row per Reddit thread (submission) collected via the PRAW API.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `post_id` | VARCHAR(20) | NO | Reddit post ID (base-36 string). Primary key. |
| `film_id` | VARCHAR(50) | NO | Foreign key → `films.film_id`. |
| `thread_id` | VARCHAR(20) | YES | Same as `post_id` for top-level threads. |
| `subreddit` | VARCHAR(100) | YES | Subreddit name without `r/` prefix. |
| `post_title` | VARCHAR(1000) | YES | Full post title. |
| `post_text` | LONGTEXT | YES | Post body text (selftext). NULL for link posts, deleted, or removed. |
| `post_score` | INT | YES | Net upvote score at retrieval time. |
| `comment_count` | INT | YES | Number of comments at retrieval time. |
| `thread_url` | VARCHAR(1000) | YES | Full Reddit permalink URL. |
| `post_timestamp` | DATETIME | YES | UTC datetime of post creation (from `created_utc`). |
| `retrieval_timestamp` | DATETIME | YES | UTC datetime when this record was retrieved. |
| `is_deleted` | TINYINT(1) | YES | `1` if post text was `[deleted]` or `[removed]`. |
| `match_status` | VARCHAR(50) | YES | `verified` = confirmed related to `tt27530512`. |
| `created_at` | TIMESTAMP | NO | Row creation timestamp (auto). |

> **Privacy note:** `author` (Reddit username) is intentionally NOT collected or stored.

---

### 1.5 `reddit_comments`

One row per Reddit comment collected from threads in `reddit_posts`.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `comment_id` | VARCHAR(20) | NO | Reddit comment ID. Primary key. |
| `post_id` | VARCHAR(20) | NO | Foreign key → `reddit_posts.post_id`. |
| `film_id` | VARCHAR(50) | NO | Foreign key → `films.film_id`. |
| `parent_id` | VARCHAR(20) | YES | Parent ID (prefixed `t1_` for comment, `t3_` for post). |
| `subreddit` | VARCHAR(100) | YES | Subreddit name. |
| `comment_text` | LONGTEXT | YES | Comment body. NULL if deleted or removed. |
| `comment_score` | INT | YES | Net upvote score at retrieval time. |
| `comment_timestamp` | DATETIME | YES | UTC datetime of comment creation. |
| `retrieval_timestamp` | DATETIME | YES | UTC datetime of retrieval. |
| `is_deleted` | TINYINT(1) | YES | `1` if body was `[deleted]` or `[removed]`. |
| `created_at` | TIMESTAMP | NO | Row creation timestamp (auto). |

> **Privacy note:** `author` (Reddit username) is intentionally NOT collected or stored.

---

### 1.6 `wikipedia_snapshots`

Each run of `collect_wikipedia.py` stores a point-in-time snapshot of the Wikipedia article.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `snapshot_id` | INT AUTO_INCREMENT | NO | Primary key. |
| `film_id` | VARCHAR(50) | NO | Foreign key → `films.film_id`. Always `TOXIC_2026`. |
| `page_id` | INT | NO | Wikipedia MediaWiki Page ID (`78832995`). |
| `page_title` | VARCHAR(500) | NO | Canonical article title: `Toxic (2026 film)`. |
| `page_url` | VARCHAR(1000) | YES | Canonical article permalink. |
| `revision_id` | BIGINT | YES | MediaWiki revision ID at time of collection. |
| `revision_timestamp` | DATETIME | YES | UTC datetime of the revision. |
| `full_extract` | LONGTEXT | YES | Complete plain-text article extract. |
| `reception_text` | LONGTEXT | YES | Extracted 'Reception' section plain text. |
| `critical_response_text` | LONGTEXT | YES | Extracted 'Critical response' section plain text. |
| `retrieval_timestamp` | DATETIME | YES | UTC datetime when this snapshot was retrieved via API. |
| `created_at` | TIMESTAMP | NO | Row creation timestamp (auto). |

---

### 1.7 `source_register`

Mirrors `docs/source_register.csv`. One row per data source.

| Column | Type | Description |
|---|---|---|
| `source_id` | VARCHAR(50) | Primary key, e.g. `CRITICS_THEHINDU`. |
| `source_group` | VARCHAR(50) | `critics`, `imdb`, or `reddit`. |
| `source_name` | VARCHAR(255) | Human-readable source name. |
| `source_url` | VARCHAR(1000) | URL of source or API endpoint. |
| `source_type` | VARCHAR(100) | `bulk_dataset`, `api`, `manual_collection`, etc. |
| `data_format` | VARCHAR(50) | `TSV.GZ`, `JSON`, `CSV`, `web_page`. |
| `access_method` | VARCHAR(100) | `direct_download`, `oauth2`, `manual_web_review`, etc. |
| `access_status` | VARCHAR(50) | `accessible`, `accessible_manual`, `requires_credentials`, `unconfirmed`. |
| `permission_or_terms_notes` | TEXT | Licence / ToS summary. |
| `fields_available` | TEXT | Comma-separated field names available from this source. |
| `retrieval_date` | DATE | Date data was retrieved (NULL if not yet collected). |
| `limitations` | TEXT | Key limitations of this source. |
| `notes` | TEXT | Additional notes. |
| `created_at` | TIMESTAMP | Row creation timestamp (auto). |

---

## 2. CSV Files

### 2.1 `data/raw/critics/manual_entry_template.csv`

The entry template for manually collected critic reviews.
All columns match `critic_reviews` table.

| Field | Required | Notes |
|---|---|---|
| `review_id` | YES | Must be unique; format `{SOURCE_ID}_{NN}` |
| `film_id` | YES | Must be `TOXIC_2026` |
| `publication` | YES | Full name of publication |
| `critic_name` | YES | Full name of reviewer |
| `review_date` | YES | ISO 8601 date `YYYY-MM-DD` |
| `rating_raw` | NO | Raw rating string from source |
| `rating_scale` | NO | `5star`, `4star`, `10point`, `100point`, `lettergrade` |
| `rating_normalized` | NO | Leave blank — script will compute if scale is known |
| `review_text` | NO | Full review text transcribed from publication |
| `review_url` | YES | Direct URL to the review |
| `collection_date` | YES | Date you entered this row `YYYY-MM-DD` |
| `collection_method` | YES | `manual_entry` |
| `source_id` | YES | From `docs/source_register.csv` |

---

## 3. NULL Handling Strategy

| Situation | Action |
|---|---|
| Unknown numeric value | `NULL` / `NaN` — never zero |
| Missing text | `NULL` — record retained if other metadata present |
| Deleted Reddit content | `NULL` text + `is_deleted = 1` |
| Unknown rating scale | `rating_normalized = NULL` — raw rating preserved |
| Ambiguous film match | `match_status = 'ambiguous'` — excluded from main load |
| IMDb `\N` values | Converted to `NULL` during cleaning |

---

## 4. File Format Summary

| Stage | Critics | IMDb | Reddit | Wikipedia |
|---|---|---|---|---|
| Raw | CSV template | TSV.GZ (original, unchanged) | JSONL (incremental) | JSON (native API response) |
| Staging | CSV | JSON + CSV | CSV | JSON + CSV |
| Processed | CSV | JSON + CSV | Parquet | JSON + CSV |
