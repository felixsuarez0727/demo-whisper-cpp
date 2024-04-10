import time
from whispercpp import Whisper

w = Whisper("tiny") # Options: "tiny", "small", "base", "medium", "large"

# Record start time
start_time = time.time()

# Perform transcription
result = w.transcribe("./audios_for_testing/gb0.wav")

# Check if transcription was successful
if result == 0:
    # Extract and print transcribed text
    text = w.extract_text(result)
    print("\n".join(text))
else:
    # Transcription failed
    print("Transcription failed with error code:", result)

# Record end time
end_time = time.time()

# Calculate processing time
processing_time_seconds = end_time - start_time

# Calculate hours, minutes, and remaining seconds
hours = int(processing_time_seconds // 3600)
minutes = int((processing_time_seconds % 3600) // 60)
seconds = int(processing_time_seconds % 60)

# Print processing time
print("\nProcessing time: %d hours, %d minutes, %d seconds" %
      (hours, minutes, seconds))
