# Use the official Python image as the base image
FROM python:3.9

# Install ffmpeg and handle missing packages
RUN apt-get update --fix-missing && apt-get install -y --fix-missing ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install tabulate==0.9.0 \
    && pip install git+https://github.com/stlukey/whispercpp.py@7af678159c29edb3bc2a51a72665073d58f2352f

# Command to run the Python script
CMD ["python", "batch_audio_transcriber.py"]
