# Use the official Python image for Windows as base image
FROM python:3.11-windowsservercore

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "Auction.asgi:application"]
