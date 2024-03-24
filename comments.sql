CREATE DATABASE comments

\c comments;

CREATE TABLE comments(
    id SERIAL PRIMARY KEY,
    text VARCHAR,
    author VARCHAR(50),
    video_id TEXT,
    comment_id TEXT,
    potentially_antisemitic BOOLEAN DEFAULT FALSE
)

SELECT * FROM comments;

TRUNCATE TABLE comments;

SELECT * FROM comments WHERE potentially_antisemitic=True