# Use the official Python image as the base image
FROM python:3.9.6

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the source code from the src folder to the container
COPY src /app/src

EXPOSE 5000

# Start the Flask app
CMD ["python3", "src/app.py"]
