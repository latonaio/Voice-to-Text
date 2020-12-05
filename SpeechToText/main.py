#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

# from StatusJsonPythonModule import StatusJsonRest
import os
import sys
import wave

# Check existing azure speechsdk
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
API_JSON_FILE = "ToyotaPE-f9f77659690a.json"
BASE_PATH = os.path.dirname(os.path.join(os.getcwd(), 'api_key'))
print(BASE_PATH)
GCOURD_API_KEY_JSON_PATH = os.path.join(os.getcwd(), 'api_key', API_JSON_FILE)
print(GCOURD_API_KEY_JSON_PATH)
# set gcloud credential
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCOURD_API_KEY_JSON_PATH


# speech recognized class
class speechRecognize():
    def __init__(self):
        self.client = speech.SpeechClient()

    def speech_recognize_from_file(self, filename):
        print(">>> Start speech recognize from file <<<")
        self.result_status = False
        self.result_text = ""

        # wav file checker
        try:
            with wave.open(filename, 'r') as f:
                framerate = f.getframerate()
                mono_flag = True if f.getnchannels() == 1 else False
        except EOFError:
            print("Error: wave file is broken... (" + filename + ")")
            return
        except FileNotFoundError:
            print("Error: file not found... (" + filename + ")")
            return

        # check monoral
        if not mono_flag:
            print("Error: This wave file is not monoral... (" + filename + ")")
            return

        # open file
        with open(filename, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=framerate,
            audio_channel_count=1,
            enable_separate_recognition_per_channel=True,
            language_code='ja-JP')

        # Detects speech in the audio file
        try:
            response = self.client.recognize(config=config, audio=audio, retry=None, timeout=58)
        except InvalidArgument:
            print("Error: wav file is invalid (" + filename + ")")
            return
        except DeadlineExceeded:
            print("Error: wav file processing time exceeded (" + filename + ")")
            return

        # check result
        if not response.results:
            print("Error: recognize response is Null")
            return

        # import pdb; pdb.set_trace()
        print(response.results)
        transcript = ""
        for ret in response.results:
            transcript += ret.alternatives[0].transcript
        # transcript = response.results[0].alternatives[0].transcript
        if transcript is None:
            print("Error recognize response is NoMatch")
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


def main():
    # read status json file
    # statusObj = StatusJsonRest.StatusJsonRest(os.getcwd(), __file__)
    # statusObj.initializeStatusJson()
    # input_file_path = statusObj.getInputFileNameFromJson()
    # if input_file_path is None:
    #     print("Critical Error: cant get input file path")
    #     sys.exit(2)

    # speech recognize
    # input_file_path = "/var/lib/aion/Data/capture-audio-from-mic_1/20200831113157000.wav"
    input_file_path = '/var/lib/aion/default/Data/capture-audio-from-mic_1/20200902092715000.wav'
    input_file_path = '/var/lib/aion/default/Data/capture-audio-from-mic_1/20200902092444000.wav'
    SpeechRec = speechRecognize()
    SpeechRec.speech_recognize_from_file(input_file_path)
    print(SpeechRec.get_result_status)
    print(SpeechRec.get_result_text)
    # statusObj.setResultStatus(SpeechRec.get_result_status())

    # statusObj.setNextService(
    #    "GoogleTranslationFromJapaneseToEnglish",
    #    "/home/latona/tartarus/Runtime/google-translation-from-japanese-to-english/GoogleTranslationFromJapaneseToEnglish",
    #    "python", "main.py", "bluetooth_audio_test")

    # if result is True ; json file is outputted
    # if SpeechRec.get_result_status():
        # initialized jsonfile for recognized text
    #    statusObj.setMetadataValue("transcript", SpeechRec.get_result_text())
    # statusObj.outputJsonFile()


if __name__ == "__main__":
    main()
