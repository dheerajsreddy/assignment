# Use the official Python 3.9 image as the base image
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code into the container
COPY . /app
# Install the required Python packages
RUN pip3 install -r requirements.txt

# Expose the ports for Flask, PostgreSQL, and Redis
EXPOSE 5000
EXPOSE 5432
EXPOSE 6379

# Set environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Command to start the startup script
CMD ["python3","app.py"]
