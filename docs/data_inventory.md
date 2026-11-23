# Data Inventory
## Critics vs Audiences: A Comparative Analysis of 8 Indian Films (2025)

### 1. Project Overview

This project examines differences between professional critics' ratings and general audience ratings for eight Indian films released in 2025.

The study combines structured IMDb data, semi-structured Wikipedia REST API responses, critic review information, and an independent large-scale IMDb review corpus used for PySpark processing.

### 2. Data Inventory

| Dataset | Source | Format | Data Type | Records |
|---|---|---|---|---:|
| Film metadata and ratings | IMDb Non-Commercial Datasets | TSV (compressed) | Structured | 8 selected films |
| Critic reviews and ratings | Indian Express, Times of India, Hindustan Times | CSV | Structured / Unstructured excerpts | 8 reviews |
| Film information | Wikipedia REST API | JSON | Semi-structured | 8 API responses |
| Large movie review corpus | Stanford IMDb Large Movie Review Dataset | TXT | Unstructured text with labels | 50,000 reviews |

### 3. Dataset Descriptions

#### 3.1 IMDb Dataset

IMDb title basics and title ratings datasets were used to retrieve film metadata, average audience ratings and vote counts.

Important fields:
- IMDb ID
- Film title
- Release year
- Runtime
- Genres
- Average IMDb rating
- Number of IMDb votes

The study uses aggregate ratings and vote counts, not individual audience review text.

#### 3.2 Professional Critic Reviews

Eight critic review records were collected, with one review selected for each film.

Sources included:
- The Indian Express
- The Times of India
- Hindustan Times

Important fields:
- Film ID
- Publication
- Critic name
- Review date
- Original rating
- Rating scale
- Normalized rating out of 10
- Review URL
- Collection date

The collected review text excerpts were not populated. Therefore, the critic-audience comparison is based on numerical ratings rather than textual sentiment analysis.

#### 3.3 Wikipedia REST API Dataset

Wikipedia REST API responses were collected for all eight films.

The original JSON responses were flattened using `pandas.json_normalize()`.

Important fields:
- Page ID
- Page title
- Page URL
- Revision ID
- Revision timestamp
- Full extract
- Critical response text
- Reception text
- Retrieval timestamp

#### 3.4 Stanford IMDb Large Movie Review Dataset

The Stanford IMDb Large Movie Review Dataset was used as a separate large-scale text-processing demonstration.

It contains 50,000 labelled movie reviews:
- 25,000 training reviews
- 25,000 testing reviews
- Positive and negative sentiment labels

This dataset is independent of the eight selected 2025 films. It was not used to infer audience sentiment for those eight films.

### 4. Data Formats and Categories

| Category | Data Used | Characteristics |
|---|---|---|
| Structured | IMDb ratings, critic ratings, relational database tables | Rows and columns with defined fields |
| Semi-structured | Wikipedia API JSON | Nested key-value structure |
| Unstructured | Movie review text corpus | Natural language text requiring processing |

### 5. Data Processing and Storage

- Raw source files were stored under `data/raw/`.
- Intermediate datasets were stored under `data/staging/`.
- Cleaned datasets were stored under `data/processed/`.
- Relational data was loaded into MySQL database `toxic_case_study`.
- SQL analysis queries were maintained in `sql/eight_film_analysis_queries.sql`.
- PySpark outputs were stored under `data/processed/imdb_reviews/`.
- Visualisations were generated under `docs/charts/`.

### 6. Data Limitations

1. Only eight films were included in the comparative study.
2. Only one critic review was collected per film; the results are descriptive and not representative of all professional critics.
3. IMDb ratings are aggregate audience scores and do not provide individual audience review text.
4. Critic review text excerpts were not collected for textual sentiment analysis.
5. The Stanford 50,000-review corpus is separate from the eight-film dataset.
6. Genre-wise comparisons have small sample sizes and should be interpreted cautiously.

### 7. Conclusion

The project integrates multiple data formats and sources to demonstrate data collection, transformation, cleaning, relational storage, SQL analysis, visualisation and large-scale text processing. The limitations of each dataset are explicitly considered to maintain transparency and reproducibility.