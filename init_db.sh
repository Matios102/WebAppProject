#!/bin/bash

set -e

DB_NAME="dough"
DB_USER="user"
DB_PASSWORD="password"

# Connect to the database and create tables
psql -U $DB_USER -d $DB_NAME <<EOF
-- Create Tables
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    team_id INTEGER,
    is_approved BOOLEAN NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    category_id INTEGER NOT NULL,
    date DATE NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Insert Categories
INSERT INTO categories (name) VALUES 
    ('Food'), 
    ('Transportation'), 
    ('Utilities'), 
    ('Entertainment'), 
    ('Health'), 
    ('Default') 
ON CONFLICT (name) DO NOTHING;

-- Insert Users
INSERT INTO users (name, surname, email, password_hash, role, team_id, is_approved) VALUES 
    ('Admin', 'Admin', 'a@a.aaa', 'hashed_admin_password', 'admin', NULL, TRUE),
    ('Manager', 'One', 'm@m.mmm', 'hashed_manager1_password', 'manager', NULL, TRUE),
    ('Manager', 'Two', 'manager2@example.com', 'hashed_manager2_password', 'manager', NULL, TRUE),
    ('Approved', 'User1', 'u@u.uuu', 'hashed_user1_password', 'user', NULL, TRUE),
    ('Approved', 'User2', 'approved2@example.com', 'hashed_user2_password', 'user', NULL, TRUE),
    ('Approved', 'User3', 'approved3@example.com', 'hashed_user3_password', 'user', NULL, TRUE),
    ('Approved', 'User4', 'approved4@example.com', 'hashed_user4_password', 'user', NULL, TRUE),
    ('Approved', 'User5', 'approved5@example.com', 'hashed_user5_password', 'user', NULL, TRUE),
    ('Unapproved', 'User1', 'unapproved1@example.com', 'hashed_unapproved1_password', 'user', NULL, FALSE),
    ('Unapproved', 'User2', 'unapproved2@example.com', 'hashed_unapproved2_password', 'user', NULL, FALSE)
ON CONFLICT (email) DO NOTHING;

-- Insert Teams
INSERT INTO teams (name, manager_id) VALUES 
    ('Team One', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Team Two', (SELECT id FROM users WHERE email='manager2@example.com'))
ON CONFLICT (name) DO NOTHING;

-- Assign approved users to teams
UPDATE users SET team_id = (SELECT id FROM teams WHERE name='Team One') WHERE email IN ('u@u.uuu', 'approved2@example.com');
UPDATE users SET team_id = (SELECT id FROM teams WHERE name='Team Two') WHERE email IN ('approved3@example.com', 'approved4@example.com');

-- Insert Expenses for Managers and Approved Users
INSERT INTO expenses (name, amount, category_id, date, user_id) VALUES
    -- Expenses for Manager One
    ('Lunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2023-01-15', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Gym Membership', 15.00, (SELECT id FROM categories WHERE name='Health'), '2023-02-10', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Concert', 70.00, (SELECT id FROM categories WHERE name='Entertainment'), '2023-03-05', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Bill', 30.50, (SELECT id FROM categories WHERE name='Utilities'), '2023-04-15', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Lunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2023-05-15', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Taxi', 15.00, (SELECT id FROM categories WHERE name='Transportation'), '2023-06-10', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Concert', 70.00, (SELECT id FROM categories WHERE name='Entertainment'), '2023-07-05', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Tacos', 30.50, (SELECT id FROM categories WHERE name='Food'), '2023-08-15', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Tram', 7.00, (SELECT id FROM categories WHERE name='Transportation'), '2024-01-10', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Bill', 20.40, (SELECT id FROM categories WHERE name='Utilities'), '2024-02-05', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Brunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2024-03-15', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Bus', 10.00, (SELECT id FROM categories WHERE name='Transportation'), '2024-04-10', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Bowling', 40.00, (SELECT id FROM categories WHERE name='Entertainment'), '2024-05-05', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Bill', 7.00, (SELECT id FROM categories WHERE name='Utilities'), '2024-05-10', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Movies', 20.40, (SELECT id FROM categories WHERE name='Entertainment'), '2024-07-05', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Brunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2024-08-15', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Gym Membership', 10.00, (SELECT id FROM categories WHERE name='Health'), '2024-09-20', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Bowling', 40.00, (SELECT id FROM categories WHERE name='Entertainment'), '2024-10-05', (SELECT id FROM users WHERE email='m@m.mmm')),
    ('Gym Membership', 40.00, (SELECT id FROM categories WHERE name='Health'), '2024-10-20', (SELECT id FROM users WHERE email='m@m.mmm')),
    
    -- Expenses for Manager Two
    ('Lunch', 30.00, (SELECT id FROM categories WHERE name='Food'), '2023-01-20', (SELECT id FROM users WHERE email='manager2@example.com')),
    ('Bus Fare', 3.50, (SELECT id FROM categories WHERE name='Transportation'), '2023-02-15', (SELECT id FROM users WHERE email='manager2@example.com')),
    ('Movie', 12.00, (SELECT id FROM categories WHERE name='Entertainment'), '2023-03-10', (SELECT id FROM users WHERE email='manager2@example.com')),
    
    -- Expenses for Approved User1
    ('Lunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2023-01-15', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Gym Membership', 15.00, (SELECT id FROM categories WHERE name='Health'), '2023-02-10', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Concert', 70.00, (SELECT id FROM categories WHERE name='Entertainment'), '2023-03-05', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Bill', 30.50, (SELECT id FROM categories WHERE name='Utilities'), '2023-04-15', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Lunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2023-05-15', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Taxi', 15.00, (SELECT id FROM categories WHERE name='Transportation'), '2023-06-10', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Concert', 70.00, (SELECT id FROM categories WHERE name='Entertainment'), '2023-07-05', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Tacos', 30.50, (SELECT id FROM categories WHERE name='Food'), '2023-08-15', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Tram', 7.00, (SELECT id FROM categories WHERE name='Transportation'), '2024-01-10', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Bill', 20.40, (SELECT id FROM categories WHERE name='Utilities'), '2024-02-05', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Brunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2024-03-15', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Bus', 10.00, (SELECT id FROM categories WHERE name='Transportation'), '2024-04-10', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Bowling', 40.00, (SELECT id FROM categories WHERE name='Entertainment'), '2024-05-05', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Bill', 7.00, (SELECT id FROM categories WHERE name='Utilities'), '2024-05-10', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Movies', 20.40, (SELECT id FROM categories WHERE name='Entertainment'), '2024-07-05', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Brunch', 25.50, (SELECT id FROM categories WHERE name='Food'), '2024-08-15', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Gym Membership', 10.00, (SELECT id FROM categories WHERE name='Health'), '2024-09-20', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Bowling', 40.00, (SELECT id FROM categories WHERE name='Entertainment'), '2024-10-05', (SELECT id FROM users WHERE email='u@u.uuu')),
    ('Gym Membership', 40.00, (SELECT id FROM categories WHERE name='Health'), '2024-10-20', (SELECT id FROM users WHERE email='u@u.uuu'));

-- More expenses can be added similarly for other approved users
EOF

echo "Database setup completed."
