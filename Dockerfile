# Use an official Python image as the base
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY ./trial/ /app/

# Install any dependencies using pip
RUN pip install mysql-connector-python

# Command to run the Python script
CMD ["python3", "/app/web/app.py"]

