# Three Vs of Big Data Analysis
## Critics vs Audiences: A Comparative Analysis of 8 Indian Films (2025)

The three Vs — Volume, Variety and Velocity — describe important characteristics of data and help explain the challenges involved in collecting, storing and processing large and diverse datasets.

This project demonstrates these characteristics through multiple film-related data sources and a separate large-scale movie review corpus.

## 1. Volume

Volume refers to the quantity of data generated, collected and processed.

In this project, volume is demonstrated through two datasets:

- The comparative study contains data for eight Indian films released in 2025.
- The Stanford IMDb Large Movie Review Dataset contains 50,000 labelled movie reviews, consisting of 25,000 training reviews and 25,000 testing reviews.

The 50,000-review dataset was processed using PySpark. The job loaded the review text, performed text cleaning, calculated word counts and generated sentiment distribution summaries.

The processing results included:
- Total reviews processed: 50,000
- Positive reviews: 25,000
- Negative reviews: 25,000
- Average positive review word count: approximately 237.99
- Average negative review word count: approximately 235.04

This demonstrates the use of Spark DataFrames and distributed-data processing concepts for large-scale text analysis. The job was executed locally, not on a distributed cluster.

**Limitation:** The 50,000-review corpus is independent of the eight selected 2025 films and was used only to demonstrate large-scale text processing.

## 2. Variety

Variety refers to the different types, structures and formats of data collected from multiple sources.

This project incorporates three major data categories:

| Data Category | Source | Format |
|---|---|---|
| Structured | IMDb datasets | TSV / CSV |
| Semi-structured | Wikipedia REST API | JSON |
| Unstructured | Stanford IMDb review corpus | TXT |

### Structured Data

IMDb datasets provide clearly defined fields such as:
- IMDb ID
- Film title
- Release year
- Runtime
- Genres
- Average rating
- Number of votes

Critic ratings were also organized into structured records containing publication, critic name and normalized rating.

### Semi-structured Data

Wikipedia REST API responses were collected in JSON format.

The JSON responses contained nested key-value information, which was flattened using `pandas.json_normalize()` for further analysis and storage.

### Unstructured Data

The Stanford IMDb review corpus contains natural-language movie reviews stored as text files.

These reviews required text processing before aggregation. PySpark was used to clean the text and calculate word counts.

The integration of these different formats demonstrates the handling of data variety in a data analytics pipeline.

## 3. Velocity

Velocity refers to the speed at which data is generated, collected, updated and processed.

In this project, velocity is demonstrated through periodic or snapshot-based data collection and processing:

- IMDb ratings and vote counts represent an aggregate snapshot retrieved from the IMDb datasets.
- Wikipedia information was retrieved through REST API requests, with revision timestamps and retrieval timestamps retained.
- Critic review information was collected and recorded with review dates and collection dates.
- The 50,000-review corpus was processed through a PySpark pipeline to generate summaries.

The timestamp fields help distinguish when information was originally published or revised from when it was retrieved.

**Limitation:** This project does not implement real-time streaming or continuous monitoring of movie ratings. Velocity is demonstrated through data retrieval, timestamp tracking and batch processing rather than a live streaming system.

## 4. Summary

| V | Project Demonstration | Technology / Source |
|---|---|---|
| Volume | Processing 50,000 labelled movie reviews | PySpark |
| Variety | Combining TSV, CSV, JSON and TXT data | IMDb, Wikipedia API, critic sources, Stanford IMDb corpus |
| Velocity | Timestamped retrieval and batch processing | IMDb snapshots, Wikipedia REST API, Python pipeline |

## Conclusion

The project demonstrates all three characteristics of Big Data through the integration of multiple data sources, different data formats and large-scale text processing.

Although the comparative analysis focuses on eight films, the separate 50,000-review PySpark exercise demonstrates the ability to process a substantially larger text dataset. The project uses snapshot-based collection and batch processing rather than real-time streaming.