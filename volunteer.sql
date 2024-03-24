-- Active: 1710676755686@@127.0.0.1@5432@comments@public

CREATE TABLE our_volunteers(
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    chat_id bigint
)

DROP TABLE our_volunteers;
SELECT * FROM our_volunteers;