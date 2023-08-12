# Use an official Python runtime as the base image
FROM python:3.11.4

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory within the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gettext \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*





# Copy the current directory contents into the container at /app/
COPY . /app/



# Expose the port the application runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
