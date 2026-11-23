
USE toxic_case_study;

-- QUERY 1: Complete overview of all eight films
SELECT
    f.film_id,
    f.canonical_title,
    f.release_year,
    f.genres,
    i.average_rating AS imdb_rating,
    i.num_votes,
    c.rating_normalized AS critic_rating,
    c.publication
FROM films f
LEFT JOIN imdb_snapshots i ON f.film_id = i.film_id
LEFT JOIN critic_reviews c ON f.film_id = c.film_id
WHERE f.film_id LIKE 'FILM_%'
ORDER BY f.film_id;


-- QUERY 2: Critics vs audience ratings
SELECT
    f.canonical_title,
    i.average_rating AS imdb_rating,
    c.rating_normalized AS critic_rating,
    ROUND(c.rating_normalized - i.average_rating, 2)
        AS rating_difference
FROM films f
JOIN imdb_snapshots i ON f.film_id = i.film_id
JOIN critic_reviews c ON f.film_id = c.film_id
WHERE f.film_id LIKE 'FILM_%'
ORDER BY rating_difference DESC;


-- QUERY 3: Highest-rated films according to IMDb
SELECT
    f.canonical_title,
    i.average_rating,
    i.num_votes
FROM films f
JOIN imdb_snapshots i ON f.film_id = i.film_id
WHERE f.film_id LIKE 'FILM_%'
ORDER BY i.average_rating DESC
LIMIT 5;


-- QUERY 4: Average critic rating by publication
SELECT
    c.publication,
    COUNT(*) AS number_of_reviews,
    ROUND(AVG(c.rating_normalized), 2) AS average_critic_rating
FROM critic_reviews c
JOIN films f ON c.film_id = f.film_id
WHERE f.film_id LIKE 'FILM_%'
GROUP BY c.publication
ORDER BY average_critic_rating DESC;


-- QUERY 5: Genre-wise average IMDb rating
SELECT
    TRIM(SUBSTRING_INDEX(
        SUBSTRING_INDEX(f.genres, ',', numbers.n), ',', -1
    )) AS genre,
    COUNT(*) AS number_of_films,
    ROUND(AVG(i.average_rating), 2) AS average_imdb_rating
FROM films f
JOIN imdb_snapshots i ON f.film_id = i.film_id
JOIN (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3
) numbers
    ON numbers.n <= 1 + LENGTH(f.genres)
       - LENGTH(REPLACE(f.genres, ',', ''))
WHERE f.film_id LIKE 'FILM_%'
GROUP BY genre
ORDER BY average_imdb_rating DESC;


-- QUERY 6: IMDb popularity and ratings
SELECT
    f.canonical_title,
    i.average_rating,
    i.num_votes,
    CASE
        WHEN i.num_votes >= 50000 THEN 'High engagement'
        WHEN i.num_votes >= 30000 THEN 'Medium engagement'
        ELSE 'Lower engagement'
    END AS engagement_category
FROM films f
JOIN imdb_snapshots i ON f.film_id = i.film_id
WHERE f.film_id LIKE 'FILM_%'
ORDER BY i.num_votes DESC;
