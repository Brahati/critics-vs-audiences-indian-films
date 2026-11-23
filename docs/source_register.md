# Source Register
## Critics vs Audiences: A Comparative Analysis of 8 Indian Films (2025)

### 1. Overview

The project uses multiple data sources to collect film metadata, audience ratings, professional critic ratings, film-related information and review text for large-scale processing.

The following register records the sources, collection methods, formats and limitations.

### 2. Source Register

| Source ID | Source | Data Collected | Format | Access Method |
|---|---|---|---|---|
| SRC_IMDB | IMDb Non-Commercial Datasets | Film metadata, ratings and vote counts | TSV | Public dataset download |
| SRC_CRITICS | Indian Express, Times of India, Hindustan Times | One critic review and rating per film | Web pages / CSV | Manual collection of publicly accessible review information |
| SRC_WIKI | Wikipedia REST API | Film extracts, page metadata and revision information | JSON | REST API requests |
| SRC_STANFORD | Stanford IMDb Large Movie Review Dataset | 50,000 labelled movie reviews | TXT | Public dataset download |

### 3. Source Details

#### 3.1 IMDb Non-Commercial Datasets

- Website: https://datasets.imdbws.com/
- Data files: `title.basics.tsv.gz` and `title.ratings.tsv.gz`
- Data collected: Film identifiers, titles, release years, runtime, genres, average ratings and vote counts.
- Access method: Public downloadable datasets.
- Processing: Python and pandas.
- Limitation: The dataset provides aggregate ratings and vote counts, not individual audience reviews.

#### 3.2 Professional Critic Publications

Publicly accessible critic reviews were collected from:
- The Indian Express
- The Times of India
- Hindustan Times

Data collected included film title, publication, critic name, review date, original rating, rating scale, normalized rating and review URL.

- Access method: Manual collection from publicly accessible review pages.
- Processing: CSV staging and pandas cleaning.
- Limitation: One critic review was collected per film. This is a small descriptive sample and does not represent the complete opinion of a publication or the wider critic community.

The individual article URLs are retained in the critic review dataset and MySQL records.

#### 3.3 Wikipedia REST API

- API documentation: https://en.wikipedia.org/api/rest_v1/
- Access method: REST API requests.
- Format: JSON.
- Data collected: Page identifiers, page titles, revision metadata and available article extracts.
- Processing: JSON responses were flattened using `pandas.json_normalize()`.
- Limitation: Wikipedia is a collaboratively edited source. Its content may change over time and is not treated as an authoritative source of audience or critic ratings.

#### 3.4 Stanford IMDb Large Movie Review Dataset

- Dataset: IMDb Large Movie Review Dataset v1.0
- Source: Stanford AI Lab
- Download URL: https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
- Format: Text files organised by training/testing split and sentiment label.
- Size: 50,000 labelled reviews.
- Access method: Public dataset download.
- Processing: Python-based local file ingestion and PySpark transformations and aggregations.
- Limitation: This dataset is independent of the eight selected 2025 films. It is used only for demonstrating large-scale text processing.

### 4. Data Collection and Ethical Considerations

The project follows these data collection principles:

1. Publicly accessible datasets and API responses were used.
2. Critic review information was collected from publicly accessible pages.
3. No behind-login content was accessed.
4. No private user information was required for the analysis.
5. IMDb aggregate ratings and vote counts were not represented as individual review records.
6. The separate Stanford dataset was not misrepresented as reviews of the eight selected films.
7. Source URLs, collection dates and limitations were retained wherever available.
8. The project does not claim that the selected critic reviews represent the complete opinions of professional critics.

### 5. Reproducibility

The project maintains separate folders for raw, staging and processed data.

- `data/raw/` stores downloaded datasets and original API responses.
- `data/staging/` stores intermediate extracted and flattened datasets.
- `data/processed/` stores cleaned datasets and analysis outputs.
- `scripts/` contains the collection, cleaning, database loading, chart generation and PySpark scripts.
- `sql/` contains the database schema and analysis queries.
- `docs/` contains documentation, charts and evidence.

This organisation supports reproducibility and makes it possible to trace processed outputs back to their original sources.

### 6. Conclusion

The project combines publicly accessible datasets, a REST API and publicly accessible critic review information. Recording source details, collection methods and limitations improves transparency, reproducibility and responsible data use.