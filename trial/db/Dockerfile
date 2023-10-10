# Use the official MySQL image as the base image
FROM mysql:8.0

# Copy your SQL script to the container's initialization directory
# COPY ./db.sql /sql_script/db.sql
# Copy the SQL script(s) to the docker-entrypoint-initdb.d directory
COPY ./db.sql/ /docker-entrypoint-initdb.d/
