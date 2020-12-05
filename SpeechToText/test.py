import sys
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.api_core.exceptions import InvalidArgument

# filename = "mono2.wav"
filename = "whatstheweatherlike3.wav"

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    filename)

# Loads the audio into memory
with open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    audio_channel_count=1,
    enable_separate_recognition_per_channel=True,
    language_code='ja-JP')

# Detects speech in the audio file
try:
    response = client.recognize(config=config, audio=audio)
except InvalidArgument:
    print("Error: WAV file is invalid")
    sys.exit(2)

if not response.results:
    print("Error: response is Null")
    sys.exit(1)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
