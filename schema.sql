-- schema.sql

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS flask_app_db;

-- Use the newly created database
USE flask_app_db;

-- Create the 'items' table if it doesn't exist
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Insert some sample data (uncomment to use)
-- INSERT INTO items (name) VALUES ('Sample Item 1');
-- INSERT INTO items (name) VALUES ('Another Item');
-- INSERT INTO items (name) VALUES ('Third Example');
