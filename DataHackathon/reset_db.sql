-- Drop the database if it exists
DROP DATABASE IF EXISTS myprojectdb;

-- Create the database
CREATE DATABASE myprojectdb;

-- Create the user with a password
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'myuser'
   ) THEN
      CREATE USER myuser WITH PASSWORD 'mypassword';
   END IF;
END
$$;

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE myprojectdb TO myuser;
