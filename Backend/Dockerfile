# Use the official Python 3.8 image as the base image
FROM python:3.9.6

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . /app/

# Expose the port used by the Flask app (assuming it runs on port 5000)
EXPOSE 5000

# Command to run the Flask app using Python 3
CMD ["python3", "app.py"]
