CREATE TABLE IF NOT EXISTS Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT,
  phone TEXT,
  street_address TEXT,
  city TEXT,
  state TEXT,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  date_created TEXT,
  active INTEGER DEFAULT 1
);