# Critics vs Audiences: A Comparative Analysis of Eight Indian Films (2025)

## 1. Project Overview

Do professional film critics and general audiences evaluate films differently?

This project explores this question through a comparative analysis of eight Indian films released in 2025. It examines professional critic ratings alongside aggregate IMDb audience ratings to identify similarities and differences in their evaluations.

The project demonstrates an end-to-end data analytics workflow involving multi-source data collection, data cleaning, JSON processing, relational database management, SQL analysis, PySpark processing and data visualisation.

## 2. Research Question

**Do professional critics and general audiences evaluate recent Indian films differently?**

The study compares critic ratings (normalised to a 10-point scale) with aggregate IMDb audience ratings for eight selected films.

## 3. Films Included

| Film | IMDb ID |
|---|---|
| Chhaava | tt27922706 |
| Coolie | tt27441481 |
| Deva | tt27852049 |
| Dragon | tt32080876 |
| Kantara: A Legend - Chapter 1 | tt26439764 |
| Lokah Chapter One: Chandra | tt33372494 |
| Saiyaara | tt28037987 |
| Sitaare Zameen Par | tt27235410 |

## 4. Data Sources

The project integrates data from multiple sources and formats:

- **IMDb Datasets:** Film metadata, aggregate ratings and vote counts.
- **Professional Film Reviews:** Selected critic ratings and review metadata from publication websites.
- **Wikipedia REST API:** Structured page metadata and article extracts retrieved in JSON format.
- **Stanford IMDb Large Movie Review Dataset:** 50,000 labelled movie reviews used for an independent PySpark text-processing demonstration.

The 50,000-review dataset is separate from the eight-film comparative study. It demonstrates large-scale text processing and is not used as audience-review data for the selected films.

## 5. Methodology

The project follows a structured data analytics pipeline:

1. **Data Collection:** Collect film metadata and aggregate IMDb ratings, selected critic reviews, and Wikipedia article information.
2. **JSON Processing:** Retrieve Wikipedia data through its REST API and flatten nested JSON using `pandas.json_normalize()`.
3. **Data Cleaning:** Perform data validation, duplicate checks, missing-value checks, type conversion and normalisation using Excel and Python/pandas.
4. **Database Management:** Design relational tables and load the cleaned datasets into MySQL.
5. **SQL Analysis:** Perform JOIN operations, GROUP BY aggregations and comparative queries.
6. **Big Data Processing:** Use PySpark to process 50,000 labelled IMDb review text files.
7. **Data Visualisation:** Generate comparative charts to communicate findings and patterns.

## 6. Key Analytical Outputs

Six visualisations were developed:

1. Critics vs Audience Ratings – Comparative bar chart.
2. IMDb Vote Counts – Bar chart.
3. Genre-wise IMDb Ratings – Comparative genre analysis.
4. Critics vs Audience Ratings – Dumbbell chart.
5. IMDb Vote Counts – Lollipop chart.
6. IMDb Rating vs Vote Count – Scatter plot.

All visualisations are available in `docs/charts/`.

## 7. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | pandas, NumPy |
| Visualisation | Matplotlib |
| Database | MySQL |
| Querying | SQL |
| Big Data Processing | Apache Spark, PySpark |
| Data Formats | CSV, JSON, TSV |
| API Integration | Wikipedia REST API |
| Spreadsheet Processing | Microsoft Excel |
| Version Control | Git, GitHub |

## 8. Repository Structure

```text
critics-vs-audiences-indian-films/
│
├── data/
│   ├── raw/
│   ├── staging/
│   └── processed/
│
├── docs/
│   ├── charts/
│   └── evidence/
│
├── scripts/
│
├── sql/
│   ├── schema.sql
│   └── eight_film_analysis_queries.sql
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 9. Reproducing the Project

### Prerequisites

- Python 3.12 or compatible version
- Java installation compatible with the selected PySpark version
- MySQL Server
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Brahati/critics-vs-audiences-indian-films.git

cd critics-vs-audiences-indian-films
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Obtain IMDb Source Data

The original IMDb bulk datasets are not committed to this repository because of their size.

Download the required files from:

https://datasets.imdbws.com/

Required files:

- `title.basics.tsv.gz`
- `title.ratings.tsv.gz`

Place them in:

`data/raw/imdb/`

### Step 5: Configure MySQL

Use `.env.example` as a reference to create a local `.env` file with your own database credentials.

Run `sql/schema.sql` to create the relational database tables before executing the MySQL loading script.

**Do not commit your `.env` file or database credentials.**

### Step 6: Run the PySpark Demonstration

Download the Stanford IMDb Large Movie Review Dataset:

https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz

Extract the dataset under:

`data/raw/imdb_reviews/`

Run:

```bash
python scripts/run_pyspark_imdb50k.py
```

The script processes 50,000 labelled review files and generates summary outputs.

## 10. Key Findings and Limitations

The analysis identifies differences between critic ratings and aggregate IMDb audience ratings across the eight selected films.

Some key observations include:

- Deva and Lokah received slightly higher critic ratings than their IMDb audience ratings.
- Coolie, Saiyaara, Chhaava and Kantara showed larger differences, with critic ratings lower than audience ratings.
- Kantara had the highest IMDb rating in the selected sample.
- Saiyaara recorded the highest IMDb vote count, indicating the highest audience voting engagement among the selected films.

**Research limitations:**

- The comparative study covers only eight films.
- Only one professional critic review rating was collected per film. These ratings cannot represent the opinions of all critics.
- IMDb ratings are aggregate audience scores, not individual audience-review text.
- IMDb vote counts measure engagement and do not directly indicate positive or negative sentiment.
- Genre-wise comparisons have small sample sizes.
- The 50,000-review PySpark demonstration uses an independent dataset and is not sentiment analysis of the eight selected films.

The findings are descriptive and exploratory, and should not be interpreted as statistically generalisable conclusions.

## 11. Responsible Data Collection

The project uses publicly accessible datasets, API responses and selected professional review information.

It does not claim access to private or behind-login user data. Personal reviewer identifiers and profile links are not required for the comparative analysis.

Source limitations and collection details are documented in the project documentation.

## 12. Project Status

**Completed components:**

- Multi-source data collection
- JSON flattening and processing
- Excel and pandas data cleaning
- MySQL relational database design and loading
- SQL-based analysis
- PySpark processing of 50,000 reviews
- Six original data visualisations
- Data inventory, source register and cleaning documentation

**Future scope:**

- Expand the number of films and critic publications.
- Collect a larger sample of professional reviews per film.
- Incorporate individual audience-review text for a more representative sentiment comparison.
- Explore statistical methods to assess rating differences.

---

*Developed as part of the Data and Storytelling project.*