# Use a lightweight official Python runtime as the parent image.
FROM python:3.12-slim

# Set environment variables
# Prevents Python from writing pyc files to disk
#ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
#ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . /app

# Expose the port Django runs on
EXPOSE 8000

# Command to run the application using Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
