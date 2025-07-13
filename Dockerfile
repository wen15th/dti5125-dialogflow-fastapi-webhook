# Use a lightweight base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy dependency file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8080

# Start the FastAPI application (main.py is under the app directory)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
