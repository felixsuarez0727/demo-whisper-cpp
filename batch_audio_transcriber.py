import os
import time
from whispercpp import Whisper
from tabulate import tabulate

w = Whisper("small")  # Options: "tiny", "small", "base", "medium", "large"

# Directory containing audio files for testing
audio_folder = "./audios_for_testing"

# List all files in the directory
audio_files = os.listdir(audio_folder)

results = []

# Iterate over each audio file
for audio_file in audio_files:
    file_start_time = time.time()

    # Perform transcription
    result = w.transcribe(os.path.join(audio_folder, audio_file))

    # Check if transcription was successful
    if result == 0:
        # Extract transcribed text
        text = w.extract_text(result)

        # Print audio file name
        print(f"Transcribed text for {audio_file}:")

        # Print transcribed text with proper spacing
        print("\n\n".join(text))
    else:
        # Transcription failed
        print(f"Transcription of {audio_file} failed with error code:", result)

    file_end_time = time.time()
    file_processing_time_seconds = file_end_time - file_start_time

    # Calculate hours, minutes, and remaining seconds
    file_hours = int(file_processing_time_seconds // 3600)
    file_minutes = int((file_processing_time_seconds % 3600) // 60)
    file_seconds = int(file_processing_time_seconds % 60)

    results.append([audio_file, file_hours, file_minutes, file_seconds])

# Print a newline before printing the table
print()

# Print processing time for each file in a table
print(tabulate(results, headers=["Audio File", "Hours", "Minutes", "Seconds"]))

# Calculate total processing time
total_processing_time_seconds = sum(
    file[1] * 3600 + file[2] * 60 + file[3] for file in results)
total_hours = int(total_processing_time_seconds // 3600)
total_minutes = int((total_processing_time_seconds % 3600) // 60)
total_seconds = int(total_processing_time_seconds % 60)

print("\nTotal Processing Time: %d hours, %d minutes, %d seconds" %
      (total_hours, total_minutes, total_seconds))

# Add a delay to keep the container running for a while
time.sleep(5)  # Adjust the delay time as needed
