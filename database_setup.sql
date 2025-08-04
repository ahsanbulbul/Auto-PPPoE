-- Auto-PPPoE Database Setup
-- This file contains the SQL commands to create and populate the credentials.db file

-- Create the router table
-- This stores your router's WiFi SSID and admin credentials
CREATE TABLE router (
    id INTEGER PRIMARY KEY,
    ssid TEXT,          -- Your WiFi network name
    username TEXT,      -- Router admin username
    password TEXT       -- Router admin password
);

-- Create the users table
-- This stores your PPPoE account credentials
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,   -- PPPoE username
    password TEXT          -- PPPoE password
);

-- Sample data insertion
-- Replace these values with your actual credentials

-- Router configuration (replace with your actual values)
INSERT INTO router VALUES (
    1, 
    'YourWiFiSSID',           -- Replace with your WiFi network name
    'router_admin_user',      -- Replace with your router admin username
    'router_admin_pass'       -- Replace with your router admin password
);

-- PPPoE user accounts (add as many as you have)
INSERT INTO users (username, password) VALUES 
    ('pppoe_user1', 'pppoe_pass1'),    -- Replace with actual PPPoE credentials
    ('pppoe_user2', 'pppoe_pass2'),    -- Add more users as needed
    ('pppoe_user3', 'pppoe_pass3');

-- To create your credentials.db file, run:
-- sqlite3 credentials.db < database_setup.sql

-- To verify your setup, run:
-- sqlite3 credentials.db "SELECT 'ROUTER:' as info; SELECT * FROM router; SELECT 'USERS:' as info; SELECT * FROM users;"
