#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

# from StatusJsonPythonModule import StatusJsonRest
import os
import sys
import wave
try:
    from aion.logger import lprint
except ImportError:
    lprint = print

try:
    from google.cloud import speech
    from google.api_core.exceptions import InvalidArgument, DeadlineExceeded
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://cloud.google.com/speech-to-text/docs/reference/libraries
    """)
    sys.exit(1)

# option
API_JSON_FILE = os.environ.get("API_JSON_FILE")
if not API_JSON_FILE:
    print("not found API FILE. exit.")
    sys.exit(1)

GCOURD_API_KEY_JSON_PATH = os.path.join("/var/lib/aion/Data/speech-to-text_1", API_JSON_FILE)
print(GCOURD_API_KEY_JSON_PATH)
# set gcloud credential
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCOURD_API_KEY_JSON_PATH


# speech recognized class
class speechRecognize():
    def __init__(self):
        self.client = speech.SpeechClient()

    def speech_recognize_from_file(self, filename):
        lprint(">>> Start speech recognize from file <<<")
        self.result_status = False
        self.result_text = ""

        # wav file checker
        try:
            with wave.open(filename, 'r') as f:
                framerate = f.getframerate()
                mono_flag = True if f.getnchannels() == 1 else False
        except EOFError:
            lprint("Error: wave file is broken... (" + filename + ")")
            return
        except FileNotFoundError:
            lprint("Error: file not found... (" + filename + ")")
            return

        # check monoral
        if not mono_flag:
            lprint("Error: This wave file is not monoral... (" + filename + ")")
            return

        # open file
        with open(filename, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        lprint(f"sample_rate_hertz: {framerate}")
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=framerate,
            audio_channel_count=1,
            enable_separate_recognition_per_channel=True,
            language_code='ja-JP')

        # Detects speech in the audio file
        try:
            # response = self.client.recognize(config=config, audio=audio, retry=None, timeout=58)
            response = self.client.recognize(config=config, audio=audio, retry=None, timeout=120)
        except InvalidArgument:
            lprint("Error: wav file is invalid (" + filename + ")")
            return
        except DeadlineExceeded:
            lprint("Error: wav file processing time exceeded (" + filename + ")")
            return

        # check result
        if not response.results:
            lprint("Error: recognize response is Null")
            return

        # lprint(response.results)
        transcript = ""
        for i in range(len(response.results)):
            transcript += response.results[i].alternatives[0].transcript
        # transcript = response.results[0].alternatives[0].transcript
        if not transcript:
            lprint("Error recognize response is NoMatch")
        else:
            self.result_status = True
            self.result_text = transcript

    # get result status ( True : Success )
    @property
    def get_result_status(self):
        return self.result_status

    @property
    def get_result_text(self):
        return self.result_text


if __name__ == "__main__":

    # speech recognize
    if len(sys.argv) > 1:
        # input_file_path = "/var/lib/aion/Data/capture-audio-from-mic_1/20200831113157000.wav"
        input_file_path = sys.argv[1]
    else:
        print("no input file path. exit")
        sys.exit(1)
    SpeechRec = speechRecognize()
    SpeechRec.speech_recognize_from_file(input_file_path)
    print(SpeechRec.get_result_status)
    print(SpeechRec.get_result_text)

