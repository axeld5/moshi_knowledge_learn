FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p files audios upsampled_audios eval_audios upsampled_eval_audios

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the workflow
CMD ["sh", "-c", "python generate_qa.py && python generate_set.py && python validate_set.py"] 