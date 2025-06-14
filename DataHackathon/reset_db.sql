-- reset_db.sql
DROP DATABASE IF EXISTS myprojectdb;
CREATE DATABASE myprojectdb;

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

GRANT ALL PRIVILEGES ON DATABASE myprojectdb TO myuser;

-- Connect to myprojectdb and grant schema privileges
\connect myprojectdb
GRANT ALL ON SCHEMA public TO myuser;
