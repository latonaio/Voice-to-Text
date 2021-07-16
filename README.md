# Voice-to-Text
Voice-to-Textは、Google API(Speech-to-Text)を用いて、音声ファイルをテキストへと変換する音声変換ツールです。
# 概要
Voice-to-Textは、音声ファイルのファイルパスを受け取ることで音声ファイル(.wav)を読み込み、テキストへ変換して出力する音声変換ツールです。  
日本語音声のみに対応しています。また、録音時間が1分以内の音声データに限ります。
同期音声認識であるため、すべての音声が送信・処理された後、結果を受け取ることができます。  
Voice-to-Textには、pythonライブラリーであるspeech-to-textが入っており、jobとして実行され、単一の音声ファイルをテキスト変換するmain_with_kanbanと、pod上での運用を前提としたmain_with_kanban_itrが含まれます。

# Speech-to-Text(Google Cloud API)
Speech-to-Textは、Google Cloud Platformが提供している音声認識APIです。音声ファイルを送信することで処理結果を得ることができます。
本ツールでは同期認識を採用しているため、リクエストは録音時間が1分以内の音声データに制限されます。

# 動作環境
本アプリケーションはaion-core上での動作を前提としており、以下の環境が必要です。  

- AIONリソース
- OS : Linux
- CPU: Intel64/AMD64/ARM64
- kubernetes

# 認証情報
クレデンシャル情報の含まれたJSONファイルを、GCPの「APIとサービス」ページからダウンロードし、コンテナ内の`/var/lib/aion/default/Data/speech-to-text_1`ディレクトリ配下に配置されるよう設定してください。  
aion-core内部では、`/var/lib/aion/default/Data`ディレクトリは`/var/lib/aion/Data`ディレクトリにマウントされるため、特別な設定は不要です。

# 環境変数
| 環境変数名      | 備考                             | 
| :-------------: | :------------------------------: | 
| API_JSON_FILE   | 認証情報を格納したファイルの名前  | 
| DEVICE_NAME     | デバイス名                       | 
| audio_file_path | 音声ファイルのpath               |   


# 起動方法
以下のコマンドを入力してdockerイメージを作成してください。
```
$ /path/to/voice-to-text/SpeechToText
$ make docker-build
```

# Input
音声ファイル(.wav)のファイルパスをプロパティ―として持つkanbanを受け取ります。音声ファイルは日本語で録音されたものにのみ対応しています。

# Output
処理結果(bool型)と、音声ファイルを文字に起こしたテキスト、および音声ファイルのファイルパスをプロパティ―として持つkanbanを出力します。

# リファレンス
- googleapis/python-speech  
https://github.com/googleapis/python-speech
- Speech-to-Text クライアント ライブラリ  
https://cloud.google.com/speech-to-text/docs/reference/libraries
- Python Client for Cloud Speech API  
https://googleapis.dev/python/speech/latest/index.html