
from pathlib import Path
import os
import logging
from datetime import datetime, timezone

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

FILM_IDS = [
    "FILM_001", "FILM_002", "FILM_003", "FILM_004",
    "FILM_005", "FILM_006", "FILM_007", "FILM_008"
]

IMDB_FILE = ROOT / "data/processed/imdb/eight_films_imdb.csv"
CRITIC_FILE = ROOT / "data/processed/critics/eight_films_critic_reviews_clean.csv"
WIKI_FILE = ROOT / "data/processed/wikipedia/eight_films_wikipedia_clean.csv"


def get_engine():
    """Create MySQL connection using environment variables."""
    required = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise EnvironmentError(
            f"Missing MySQL environment variables: {missing}"
        )

    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE"),
        query={"charset": "utf8mb4"},
    )

    return create_engine(url, pool_pre_ping=True)


def clean_value(value):
    """Convert pandas missing values to Python None."""
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    return value


def to_date(value):
    value = clean_value(value)
    if value is None:
        return None
    return pd.to_datetime(value, errors="coerce").date()


def to_datetime(value):
    value = clean_value(value)
    if value is None:
        return None

    timestamp = pd.to_datetime(value, errors="coerce", utc=True)

    if pd.isna(timestamp):
        return None

    return timestamp.tz_convert(None).to_pydatetime()


def to_int(value):
    value = clean_value(value)
    if value is None:
        return None

    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return None

    return int(number)


def to_float(value):
    value = clean_value(value)
    if value is None:
        return None

    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return None

    return float(number)


def load_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


def upsert_films(conn, imdb_df, critic_df):
    """Insert or update the eight canonical film records."""

    mapping = (
        critic_df[["film_id", "film_name", "imdb_id"]]
        .drop_duplicates(subset=["film_id"])
    )

    imdb_lookup = imdb_df.set_index("imdb_id").to_dict("index")

    sql = text("""
        INSERT INTO films (
            film_id, imdb_id, canonical_title,
            primary_title, original_title,
            release_year, genres, runtime_minutes
        )
        VALUES (
            :film_id, :imdb_id, :canonical_title,
            :primary_title, :original_title,
            :release_year, :genres, :runtime_minutes
        )
        ON DUPLICATE KEY UPDATE
            imdb_id = VALUES(imdb_id),
            canonical_title = VALUES(canonical_title),
            primary_title = VALUES(primary_title),
            original_title = VALUES(original_title),
            release_year = VALUES(release_year),
            genres = VALUES(genres),
            runtime_minutes = VALUES(runtime_minutes)
    """)

    for _, row in mapping.iterrows():
        imdb_id = row["imdb_id"]
        imdb = imdb_lookup.get(imdb_id)

        if imdb is None:
            raise ValueError(f"IMDb data missing for {imdb_id}")

        record = {
            "film_id": row["film_id"],
            "imdb_id": imdb_id,
            "canonical_title": row["film_name"],
            "primary_title": clean_value(imdb.get("primary_title")),
            "original_title": clean_value(imdb.get("original_title")),
            "release_year": to_int(imdb.get("release_year")),
            "genres": clean_value(imdb.get("genres")),
            "runtime_minutes": to_int(imdb.get("runtime_minutes")),
        }

        conn.execute(sql, record)

    logging.info("Inserted/updated %d film records.", len(mapping))


def replace_imdb_snapshots(conn, imdb_df, critic_df):
    """Replace the current IMDb snapshots for these eight films."""

    film_map = (
        critic_df[["film_id", "imdb_id"]]
        .drop_duplicates(subset=["film_id"])
        .set_index("imdb_id")["film_id"]
        .to_dict()
    )

    # Remove previous snapshots for these eight film IDs.
    conn.execute(
        text("""
            DELETE FROM imdb_snapshots
            WHERE film_id IN :film_ids
        """).bindparams(),
        {"film_ids": tuple(FILM_IDS)}
    )

    sql = text("""
        INSERT INTO imdb_snapshots (
            film_id, imdb_id, average_rating, num_votes,
            primary_title, original_title, release_year,
            genres, runtime_minutes,
            source_file_basics, source_file_ratings,
            dataset_download_timestamp, retrieval_timestamp
        )
        VALUES (
            :film_id, :imdb_id, :average_rating, :num_votes,
            :primary_title, :original_title, :release_year,
            :genres, :runtime_minutes,
            :source_file_basics, :source_file_ratings,
            :dataset_download_timestamp, :retrieval_timestamp
        )
    """)

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for _, row in imdb_df.iterrows():
        imdb_id = row["imdb_id"]
        film_id = film_map.get(imdb_id)

        if film_id is None:
            continue

        record = {
            "film_id": film_id,
            "imdb_id": imdb_id,
            "average_rating": to_float(row.get("imdb_rating")),
            "num_votes": to_int(row.get("imdb_votes")),
            "primary_title": clean_value(row.get("primary_title")),
            "original_title": clean_value(row.get("original_title")),
            "release_year": to_int(row.get("release_year")),
            "genres": clean_value(row.get("genres")),
            "runtime_minutes": to_int(row.get("runtime_minutes")),
            "source_file_basics": "title.basics.tsv.gz",
            "source_file_ratings": "title.ratings.tsv.gz",
            "dataset_download_timestamp": None,
            "retrieval_timestamp": now,
        }

        conn.execute(sql, record)

    logging.info("Loaded IMDb snapshots for %d films.", len(film_map))


def upsert_critic_reviews(conn, critic_df):
    """Insert or update critic reviews without creating duplicates."""

    sql = text("""
        INSERT INTO critic_reviews (
            review_id, film_id, publication, critic_name,
            review_date, rating_raw, rating_scale,
            rating_normalized, review_text, review_url,
            collection_date, collection_method, source_id,
            match_status
        )
        VALUES (
            :review_id, :film_id, :publication, :critic_name,
            :review_date, :rating_raw, :rating_scale,
            :rating_normalized, :review_text, :review_url,
            :collection_date, :collection_method, :source_id,
            'verified'
        )
        ON DUPLICATE KEY UPDATE
            publication = VALUES(publication),
            critic_name = VALUES(critic_name),
            review_date = VALUES(review_date),
            rating_raw = VALUES(rating_raw),
            rating_scale = VALUES(rating_scale),
            rating_normalized = VALUES(rating_normalized),
            review_text = VALUES(review_text),
            review_url = VALUES(review_url),
            collection_date = VALUES(collection_date),
            collection_method = VALUES(collection_method),
            source_id = VALUES(source_id)
    """)

    for _, row in critic_df.iterrows():
        record = {
            "review_id": row["review_id"],
            "film_id": row["film_id"],
            "publication": clean_value(row.get("publication")),
            "critic_name": clean_value(row.get("critic_name")),
            "review_date": to_date(row.get("review_date")),
            "rating_raw": clean_value(row.get("rating_raw")),
            "rating_scale": str(clean_value(row.get("rating_scale")) or ""),
            "rating_normalized": to_float(row.get("rating_normalized")),
            "review_text": clean_value(row.get("review_text")),
            "review_url": clean_value(row.get("review_url")),
            "collection_date": to_date(row.get("collection_date")),
            "collection_method": clean_value(row.get("collection_method")),
            "source_id": clean_value(row.get("source_id")),
        }

        conn.execute(sql, record)

    logging.info("Inserted/updated %d critic reviews.", len(critic_df))


def replace_wikipedia_snapshots(conn, wiki_df):
    """Replace Wikipedia snapshots for the eight study films."""

    conn.execute(
        text("""
            DELETE FROM wikipedia_snapshots
            WHERE film_id IN :film_ids
        """).bindparams(),
        {"film_ids": tuple(FILM_IDS)}
    )

    sql = text("""
        INSERT INTO wikipedia_snapshots (
            film_id, page_id, page_title, page_url,
            revision_id, revision_timestamp,
            full_extract, reception_text,
            critical_response_text, retrieval_timestamp
        )
        VALUES (
            :film_id, :page_id, :page_title, :page_url,
            :revision_id, :revision_timestamp,
            :full_extract, :reception_text,
            :critical_response_text, :retrieval_timestamp
        )
    """)

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for _, row in wiki_df.iterrows():
        if row["film_id"] not in FILM_IDS:
            continue

        record = {
            "film_id": row["film_id"],
            "page_id": to_int(row.get("pageid")),
            "page_title": clean_value(row.get("title")),
            "page_url": clean_value(
                row.get("content_urls_desktop_page")
            ),
            "revision_id": to_int(row.get("revision")),
            "revision_timestamp": to_datetime(row.get("timestamp")),
            "full_extract": clean_value(row.get("extract")),
            "reception_text": None,
            "critical_response_text": None,
            "retrieval_timestamp": now,
        }

        if record["page_id"] is None or record["page_title"] is None:
            raise ValueError(
                f"Missing required Wikipedia fields for {row['film_id']}"
            )

        conn.execute(sql, record)

    logging.info("Loaded %d Wikipedia snapshots.", len(wiki_df))


def upsert_source_register(conn):
    """Register the source groups used by the eight-film study."""

    sources = [
        {
            "source_id": "SRC_IMDB_BULK",
            "source_group": "Audience",
            "source_name": "IMDb Non-Commercial Datasets",
            "source_url": "https://datasets.imdbws.com/",
            "source_type": "Official dataset",
            "data_format": "TSV",
            "access_method": "Bulk download",
            "access_status": "Collected",
            "permission_or_terms_notes": (
                "Use subject to IMDb dataset terms; non-commercial use."
            ),
            "fields_available": (
                "IMDb ID, title, year, runtime, genres, average rating, votes"
            ),
            "limitations": (
                "Aggregate ratings and vote counts; no individual review text."
            ),
            "notes": "Snapshot used for the eight selected 2025 films.",
        },
        {
            "source_id": "SRC_WIKIPEDIA_API",
            "source_group": "Reference",
            "source_name": "Wikipedia REST API",
            "source_url": "https://en.wikipedia.org/api/rest_v1/",
            "source_type": "Public API",
            "data_format": "JSON",
            "access_method": "HTTP GET",
            "access_status": "Collected",
            "permission_or_terms_notes": (
                "Respect Wikimedia API policies and applicable article licenses."
            ),
            "fields_available": (
                "Page title, page ID, description, extract, revision metadata, URL"
            ),
            "limitations": (
                "Introductory summaries are not a standardized measure of reception."
            ),
            "notes": "JSON flattened with pandas.json_normalize().",
        },
        {
            "source_id": "SRC_INDIAN_EXPRESS",
            "source_group": "Critic",
            "source_name": "The Indian Express",
            "source_url": "https://indianexpress.com/",
            "source_type": "Published film reviews",
            "data_format": "HTML / manually recorded metadata",
            "access_method": "Manual source verification",
            "access_status": "Collected",
            "permission_or_terms_notes": (
                "Only review metadata and ratings recorded; no full article copied."
            ),
            "fields_available": (
                "Film, publication, critic, date, rating, review URL"
            ),
            "limitations": "Selected review sample, not all published reviews.",
            "notes": "Used for Chhaava, Coolie, Lokah and Saiyaara.",
        },
        {
            "source_id": "SRC_TIMES_OF_INDIA",
            "source_group": "Critic",
            "source_name": "The Times of India",
            "source_url": "https://timesofindia.indiatimes.com/",
            "source_type": "Published film reviews",
            "data_format": "HTML / manually recorded metadata",
            "access_method": "Manual source verification",
            "access_status": "Collected",
            "permission_or_terms_notes": (
                "Only review metadata and ratings recorded; no full article copied."
            ),
            "fields_available": (
                "Film, publication, critic, date, rating, review URL"
            ),
            "limitations": "Selected review sample, not all published reviews.",
            "notes": "Used for Deva, Dragon and Sitaare Zameen Par.",
        },
        {
            "source_id": "SRC_HINDUSTAN_TIMES",
            "source_group": "Critic",
            "source_name": "Hindustan Times",
            "source_url": "https://www.hindustantimes.com/",
            "source_type": "Published film reviews",
            "data_format": "HTML / manually recorded metadata",
            "access_method": "Manual source verification",
            "access_status": "Collected",
            "permission_or_terms_notes": (
                "Only review metadata and ratings recorded; no full article copied."
            ),
            "fields_available": (
                "Film, publication, critic, date, rating, review URL"
            ),
            "limitations": "One selected review in this study.",
            "notes": "Used for Kantara: A Legend - Chapter 1.",
        },
    ]

    sql = text("""
        INSERT INTO source_register (
            source_id, source_group, source_name, source_url,
            source_type, data_format, access_method, access_status,
            permission_or_terms_notes, fields_available,
            retrieval_date, limitations, notes
        )
        VALUES (
            :source_id, :source_group, :source_name, :source_url,
            :source_type, :data_format, :access_method, :access_status,
            :permission_or_terms_notes, :fields_available,
            :retrieval_date, :limitations, :notes
        )
        ON DUPLICATE KEY UPDATE
            source_name = VALUES(source_name),
            source_url = VALUES(source_url),
            source_type = VALUES(source_type),
            data_format = VALUES(data_format),
            access_method = VALUES(access_method),
            access_status = VALUES(access_status),
            permission_or_terms_notes = VALUES(permission_or_terms_notes),
            fields_available = VALUES(fields_available),
            retrieval_date = VALUES(retrieval_date),
            limitations = VALUES(limitations),
            notes = VALUES(notes)
    """)

    today = datetime.now(timezone.utc).date()

    for source in sources:
        source["retrieval_date"] = today
        conn.execute(sql, source)

    logging.info("Registered %d source records.", len(sources))


def verify_database(engine):
    """Print record counts and a joined study overview."""

    queries = {
        "Films": "SELECT COUNT(*) FROM films WHERE film_id IN :ids",
        "IMDb snapshots": (
            "SELECT COUNT(*) FROM imdb_snapshots WHERE film_id IN :ids"
        ),
        "Critic reviews": (
            "SELECT COUNT(*) FROM critic_reviews WHERE film_id IN :ids"
        ),
        "Wikipedia snapshots": (
            "SELECT COUNT(*) FROM wikipedia_snapshots WHERE film_id IN :ids"
        ),
        "Sources": (
            "SELECT COUNT(*) FROM source_register "
            "WHERE source_id IN :ids"
        ),
    }

    with engine.connect() as conn:
        for label, query in queries.items():
            ids = (
                tuple([
                    "SRC_IMDB_BULK", "SRC_WIKIPEDIA_API",
                    "SRC_INDIAN_EXPRESS", "SRC_TIMES_OF_INDIA",
                    "SRC_HINDUSTAN_TIMES"
                ])
                if label == "Sources"
                else tuple(FILM_IDS)
            )

            count = conn.execute(
                text(query).bindparams(),
                {"ids": ids}
            ).scalar()

            print(f"{label}: {count}")

        overview = conn.execute(text("""
            SELECT
                f.film_id,
                f.canonical_title,
                i.average_rating AS imdb_rating,
                i.num_votes,
                c.rating_normalized AS critic_rating,
                w.page_title AS wikipedia_page
            FROM films f
            LEFT JOIN imdb_snapshots i
                ON f.film_id = i.film_id
            LEFT JOIN critic_reviews c
                ON f.film_id = c.film_id
            LEFT JOIN wikipedia_snapshots w
                ON f.film_id = w.film_id
            WHERE f.film_id IN (
                'FILM_001', 'FILM_002', 'FILM_003', 'FILM_004',
                'FILM_005', 'FILM_006', 'FILM_007', 'FILM_008'
            )
            ORDER BY f.film_id
        """))

        print("\nJoined study overview:")
        print(pd.DataFrame(overview.fetchall(), columns=overview.keys()).to_string(index=False))


def main():
    print("========== EIGHT-FILM MYSQL LOADER ==========")

    imdb_df = load_csv(IMDB_FILE)
    critic_df = load_csv(CRITIC_FILE)
    wiki_df = load_csv(WIKI_FILE)

    if critic_df["film_id"].nunique() != 8:
        raise ValueError("Expected exactly eight distinct critic film IDs.")

    if set(critic_df["film_id"].unique()) != set(FILM_IDS):
        raise ValueError("Critic dataset film IDs do not match the study IDs.")

    if wiki_df["film_id"].nunique() != 8:
        raise ValueError("Expected exactly eight distinct Wikipedia film IDs.")

    if imdb_df["imdb_id"].nunique() != 8:
        raise ValueError("Expected exactly eight distinct IMDb IDs.")

    engine = get_engine()

    # Check that the existing schema has been applied.
    with engine.connect() as conn:
        tables = conn.execute(text("SHOW TABLES")).fetchall()
        table_names = {row[0] for row in tables}

    required_tables = {
        "films", "imdb_snapshots", "critic_reviews",
        "wikipedia_snapshots", "source_register"
    }

    missing = required_tables - table_names
    if missing:
        raise RuntimeError(
            f"Missing MySQL tables: {sorted(missing)}. "
            "Apply sql/schema.sql first."
        )

    # All changes are committed together or rolled back together.
    with engine.begin() as conn:
        upsert_films(conn, imdb_df, critic_df)
        replace_imdb_snapshots(conn, imdb_df, critic_df)
        upsert_critic_reviews(conn, critic_df)
        replace_wikipedia_snapshots(conn, wiki_df)
        upsert_source_register(conn)

    print("\n========== DATABASE VERIFICATION ==========")
    verify_database(engine)

    engine.dispose()
    print("\nMySQL loading completed successfully.")


if __name__ == "__main__":
    main()
