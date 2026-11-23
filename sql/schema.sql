CREATE DATABASE IF NOT EXISTS toxic_case_study CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE toxic_case_study;

CREATE TABLE IF NOT EXISTS films (
    film_id VARCHAR(50) PRIMARY KEY,
    imdb_id VARCHAR(20) UNIQUE NOT NULL,
    canonical_title VARCHAR(500) NOT NULL,
    primary_title VARCHAR(500),
    original_title VARCHAR(500),
    release_year SMALLINT,
    director VARCHAR(255),
    starring VARCHAR(500),
    genres VARCHAR(255),
    runtime_minutes SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS critic_reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    film_id VARCHAR(50) NOT NULL,
    publication VARCHAR(255),
    critic_name VARCHAR(255),
    review_date DATE,
    rating_raw VARCHAR(50),
    rating_scale VARCHAR(50),
    rating_normalized DECIMAL(5,2),
    review_text LONGTEXT,
    review_url VARCHAR(1000),
    collection_date DATE,
    collection_method VARCHAR(100),
    source_id VARCHAR(50),
    match_status VARCHAR(50) DEFAULT 'verified',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_id) REFERENCES films(film_id)
);

CREATE TABLE IF NOT EXISTS imdb_snapshots (
    snapshot_id INT AUTO_INCREMENT PRIMARY KEY,
    film_id VARCHAR(50) NOT NULL,
    imdb_id VARCHAR(20) NOT NULL,
    average_rating DECIMAL(3,1),
    num_votes INT,
    primary_title VARCHAR(500),
    original_title VARCHAR(500),
    release_year SMALLINT,
    genres VARCHAR(255),
    runtime_minutes SMALLINT,
    source_file_basics VARCHAR(255),
    source_file_ratings VARCHAR(255),
    dataset_download_timestamp DATETIME,
    retrieval_timestamp DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_id) REFERENCES films(film_id)
);

CREATE TABLE IF NOT EXISTS reddit_posts (
    post_id VARCHAR(20) PRIMARY KEY,
    film_id VARCHAR(50) NOT NULL,
    thread_id VARCHAR(20),
    subreddit VARCHAR(100),
    post_title VARCHAR(1000),
    post_text LONGTEXT,
    post_score INT,
    comment_count INT,
    thread_url VARCHAR(1000),
    post_timestamp DATETIME,
    retrieval_timestamp DATETIME,
    is_deleted TINYINT(1) DEFAULT 0,
    match_status VARCHAR(50) DEFAULT 'verified',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_id) REFERENCES films(film_id)
);

CREATE TABLE IF NOT EXISTS reddit_comments (
    comment_id VARCHAR(20) PRIMARY KEY,
    post_id VARCHAR(20) NOT NULL,
    film_id VARCHAR(50) NOT NULL,
    parent_id VARCHAR(20),
    subreddit VARCHAR(100),
    comment_text LONGTEXT,
    comment_score INT,
    comment_timestamp DATETIME,
    retrieval_timestamp DATETIME,
    is_deleted TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(post_id),
    FOREIGN KEY (film_id) REFERENCES films(film_id)
);

CREATE TABLE IF NOT EXISTS wikipedia_snapshots (
    snapshot_id INT AUTO_INCREMENT PRIMARY KEY,
    film_id VARCHAR(50) NOT NULL,
    page_id INT NOT NULL,
    page_title VARCHAR(500) NOT NULL,
    page_url VARCHAR(1000),
    revision_id BIGINT,
    revision_timestamp DATETIME,
    full_extract LONGTEXT,
    reception_text LONGTEXT,
    critical_response_text LONGTEXT,
    retrieval_timestamp DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_id) REFERENCES films(film_id)
);

CREATE TABLE IF NOT EXISTS source_register (
    source_id VARCHAR(50) PRIMARY KEY,
    source_group VARCHAR(50),
    source_name VARCHAR(255),
    source_url VARCHAR(1000),
    source_type VARCHAR(100),
    data_format VARCHAR(50),
    access_method VARCHAR(100),
    access_status VARCHAR(50),
    permission_or_terms_notes TEXT,
    fields_available TEXT,
    retrieval_date DATE,
    limitations TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_critic_film_id ON critic_reviews(film_id);
CREATE INDEX idx_critic_source_id ON critic_reviews(source_id);
CREATE INDEX idx_critic_review_date ON critic_reviews(review_date);
CREATE INDEX idx_imdb_film_id ON imdb_snapshots(film_id);
CREATE INDEX idx_imdb_imdb_id ON imdb_snapshots(imdb_id);
CREATE INDEX idx_imdb_retrieval ON imdb_snapshots(retrieval_timestamp);
CREATE INDEX idx_reddit_post_film_id ON reddit_posts(film_id);
CREATE INDEX idx_reddit_post_subreddit ON reddit_posts(subreddit);
CREATE INDEX idx_reddit_post_timestamp ON reddit_posts(post_timestamp);
CREATE INDEX idx_reddit_comment_post_id ON reddit_comments(post_id);
CREATE INDEX idx_reddit_comment_film_id ON reddit_comments(film_id);
CREATE INDEX idx_wikipedia_film_id ON wikipedia_snapshots(film_id);
CREATE INDEX idx_wikipedia_page_id ON wikipedia_snapshots(page_id);
CREATE INDEX idx_wikipedia_retrieval ON wikipedia_snapshots(retrieval_timestamp);
