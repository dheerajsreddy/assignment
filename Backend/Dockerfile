# Use the official Python 3.9 image as the base image
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code into the container
COPY . /app

# Install the required Python packages
RUN pip install -r requirements.txt

# Install Redis server inside the container (if your app requires it)
RUN apt-get update && apt-get install -y redis-server

# Expose the ports for Flask, PostgreSQL, and Redis
EXPOSE 5000
EXPOSE 5432
EXPOSE 6379

# Set environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Create a startup script to run Redis server and the Flask application concurrently
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Command to start the startup script
CMD ["/start.sh"]
