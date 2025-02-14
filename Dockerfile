# Use the latest Python image
FROM python:3.11

# Install FFmpeg and required system packages
RUN apt-get update && apt-get install -y ffmpeg libffi-dev

# Set the working directory
WORKDIR /bot

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files into the container
COPY . .

# Run the bot
CMD ["python", "main.py"]
