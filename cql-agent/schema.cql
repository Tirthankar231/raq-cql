CREATE KEYSPACE IF NOT EXISTS agent_demo
WITH replication = {'class':'SimpleStrategy','replication_factor':1};

USE agent_demo;

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_date DATE
);

INSERT INTO users (id, name, email, created_date)
VALUES (uuid(), 'Rahul', 'rahul@test.com', '2026-01-15');

INSERT INTO users (id, name, email, created_date)
VALUES (uuid(), 'Anita', 'anita@test.com', '2026-01-14');

INSERT INTO users (id, name, email, created_date)
VALUES (uuid(), 'Suresh', 'suresh@test.com', '2026-01-15');
