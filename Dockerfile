FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Install required system dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "VolumeHandController.py"]

