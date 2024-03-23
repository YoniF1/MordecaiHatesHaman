CREATE DATABASE comments;

\c comments;

CREATE TABLE comments(
    id SERIAL PRIMARY KEY,
    text VARCHAR,
    author VARCHAR(50),
    comment_id TEXT
)

SELECT * FROM comments;

DROP TABLE comments;