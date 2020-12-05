# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import time
import os
import sys

from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.logger import lprint, initialize_logger
from .speech2text import speechRecognize


SERVICE_NAME = os.environ.get("SERVICE", "speech-to-text")
SLEEP_TIME = os.environ.get("SLEEP_TIME", "0.5")
DEVICE_NAME = os.environ.get("DEVICE_NAME")
LOOP_COUNT = os.environ.get("LOOP_COUNT", "10")
initialize_logger(SERVICE_NAME)


@main_decorator(SERVICE_NAME)
def main_with_kanban(opt: Options):
    lprint("start main_with_kanban()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban = conn.get_one_kanban(SERVICE_NAME, num)

    metadata = kanban.get_metadata()
    audio_path = metadata.get('audio_file_path')
    if not audio_path:
        lprint("no found audio file path")
        sys.exit(1)

    # get output data path
    # data_path = kanban.get_data_path()
    # get previous service list
    # service_list = kanban.get_services()

    ######### main function #############
    client = speechRecognize()
    client.speech_recognize_from_file(audio_path)
    lprint(client.get_result_status)
    lprint(client.get_result_text)

    # output after kanban
    conn.output_kanban(
        result=client.get_result_status,
        metadata={"transcript": client.get_result_text,
                  "audio_file": audio_path},
    )


@main_decorator(SERVICE_NAME)
def main_without_kanban(opt: Options):
    lprint("start main_without_kanban()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)

    # get output data path
    data_path = kanban.get_data_path()
    # get previous service list
    service_list = kanban.get_services()
    print(service_list)

    ######### main function #############
    audio_path = '/var/lib/aion/Data/capture-audio-from-mic_1/20200902013745000.wav'
    client = speechRecognize()
    client.speech_recognize_from_file(audio_path)
    lprint('status: ', client.get_result_status)
    lprint('transcript: ', client.get_result_text)

    # output after kanban
    conn.output_kanban(
        result=client.get_result_status,
        metadata={"transcript": client.get_result_text,
                  "audio_file": audio_path},
    )

@main_decorator(SERVICE_NAME)
def main_with_kanban_itr(opt: Options):
    lprint("start main_with_kanban_itr()")
    # get cache kanban
    conn = opt.get_conn()
    num = int(opt.get_number())
    try:
        client = speechRecognize()
        for kanban in conn.get_kanban_itr(SERVICE_NAME, num):
            metadata = kanban.get_metadata()
            lprint(metadata)
            metadata = kanban.get_metadata()
            audio_path = metadata.get('audio_file_path')
            if not audio_path:
                lprint("no found audio file path")
                continue
           
            client.speech_recognize_from_file(audio_path)
            lprint(client.get_result_status)
            lprint(client.get_result_text)
            # output after kanban
            conn.output_kanban(
                    result=client.get_result_status,
                    metadata={
                        "transcript": client.get_result_text,
                        "audio_file": audio_path
                    },
            )
    except Exception as e:
        lprint(str(e))
    finally:
        pass


@main_decorator(SERVICE_NAME)
def send_kanbans_at_highspeed(opt: Options):
    lprint("start send_kanbans_at_highspeed()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)
    data_path = kanban.get_data_path()

    index = 0
    while True:
        if index > int(LOOP_COUNT):
            lprint("break loop")
            break

        conn.output_kanban(
            result=True,
            connection_key="default",
            output_data_path=data_path,
            metadata={
                "data": {
                    "key": index,
                    "dataForm": "normal",
                    "robotData": [
                        {
                            "robotStatus": 0,
                            "sample": "いしい",
                        },
                    ],
                    "arrayNo": 1,
                }
            },
            process_number=num,
            device_name=DEVICE_NAME,
        )
        index = index + 1
        time.sleep(float(SLEEP_TIME))
