# COSMO 2 ❤
COSMO 2 Project (COSMO, living in my son’s phone) 😉❤❤❤

![Logo](../../cosmo2.jpg)

# What you get 
    Fewer questions from your son that you can’t answer
    A smarter son, empowered with a coolest phone
    
# Usage
    shake phone and magic happends... 😉❤❤❤ 

# Usage 2 (replace IP with your own)
    curl -X GET http://192.168.1.109:1888/ask4

# Usage STT (Speech-to-Text)
    Open 'client.html' in the Firefox browser to observe near real-time speech-to-text conversion.

# What you need
    Android phone
    Tasker app
    ChatGPT API key
    --
    Optional: VPS server for STT using Whisper.cpp 
    Bonus: GPU Server for Whisper.cpp for real time STT

Prototype with phone: 
1. The cosmo_end_talk.xls file needs to be in your Google Drive folder, and you can update with your own short personality prefixes that will be added at 'end talk'. It need to be shared with link as on picture below.
2. The cosmo.csv file needs to be in your GoogleDrive folder so it can store and be updated with logs of questions, answers, and timestamps.
![Logo](config_screenshots/c16.jpg)


## Bonus: Speech to Text (STT) at home using [Whisper STT](https://openai.com/index/whisper/) library [C++ implementation](https://github.com/ggml-org/whisper.cpp)

### If you’d like to run your own server and test speech-to-text functionality
    git clone https://github.com/ggml-org/whisper.cpp.git

    # Download models start from tiny, base
    cd whisper.cpp
    sh ./models/download-ggml-model.sh tiny.en
    sh ./models/download-ggml-model.sh base.en
    sh ./models/download-ggml-model.sh small.en
    sh ./models/download-ggml-model.sh medium.en
    sh ./models/download-ggml-model.sh large-v3-turbo-q5_0
    
    # Build
    apt install cmake build-essential
    cmake -B build
    cmake --build build -j --config Release

    # Test performance and ensure that transcription of a sample (e.g., JFK speech) completes in under 1 second. 
    # Choose the appropriate model — tiny, base, small, or medium — depending on your CPU capabilities. 
    # If you are running on a GPU, transcription will be extremely fast, often around 0.1 seconds.
    ./build/bin/whisper-cli -f samples/jfk.wav -m models/ggml-tiny.en.bin
    ./build/bin/whisper-cli -f samples/jfk.wav -m models/ggml-base.en.bin

    # Install Python
    apt install python3 python3-pip portaudio19-dev python3-dev python3.13-venv ffmpeg -y

    # Add PIP
    python3 -m venv ~/cosmo
    source ~/cosmo/bin/activate
    pip install websockets pydub

    # Start Server Side
    python server.py

    # Adjust IP in stream.js in line: ws = new WebSocket("ws://46.224.122.101:8181");
    open client.html, it will connect to your server

# Current Architecture
    Client side (client.html):
    1. Records microphone audio
    2. Splits audio into chunks (streaming)
    3. Converts to PCM (16 kHz, mono) and sends via WebSocket/HTTP to server
    4. Receives transcribed text and displays it in real-time

    Server side (server.py):
    1. Whisper STT library C++ implementation.
    2. Python script receives PCM stream and constructs wav file
    3. C++ Whisper model performs STT.
    4. Returns text to client in real-time.

### Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad. It is an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've listened before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

![Logo](https://cosmo.yes.app/poster_eng.jpg)

![Logo](https://cosmo.yes.app/promotion_eng.jpg)
![Logo](https://cosmo.yes.app/bonus_eng.jpg)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.