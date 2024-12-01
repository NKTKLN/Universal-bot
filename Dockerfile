# Use the official Python image as the base image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files into the container
COPY requirements.txt .

# Install dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the local directory to the container
COPY . .

# Specify the Python path
ENV PYTHONPATH=/app

# Set the default command to run the Python script
CMD ["python", "bot/main.py"]
