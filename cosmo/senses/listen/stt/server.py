#!/usr/bin/env python3
import asyncio
import websockets
import wave
import subprocess
import time
from pathlib import Path
from io import BytesIO

# ================== Config ==================
WHISPER_CLI = "./build/bin/whisper-cli"
MODEL_PATH = "models/ggml-tiny.en.bin"
THREADS = "2"

SAVE_DIR = Path("/home/ai/whisper_chunks")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit PCM
PROCESS_INTERVAL = 5.0  # seconds per chunk
# ============================================


async def handle_client(websocket):
    client_addr = websocket.remote_address
    print(f"[INFO] Client connected: {client_addr}")

    # Per-client sequence generator
    def make_seq_gen():
        n = 0
        while True:
            n += 1
            yield n
    seq_gen = make_seq_gen()

    buffer = BytesIO()
    last_process_time = time.time()
    send_lock = asyncio.Lock()  # ensure sequence order
    tasks = set()  # track pending tasks for this client

    def write_wav(filename: Path, pcm_bytes: bytes):
        """Save raw PCM bytes to WAV file"""
        with wave.open(str(filename), "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(SAMPLE_WIDTH)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(pcm_bytes)

    async def process_buffer(pcm_bytes: bytes):
        """Process PCM and send transcription to client"""
        if not pcm_bytes or pcm_bytes == b"\x00" * len(pcm_bytes):
            print(f"[INFO] Skipped empty audio from {client_addr}")
            return

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        wav_file = SAVE_DIR / f"{timestamp}_{client_addr[1]}.wav"

        try:
            write_wav(wav_file, pcm_bytes)
        except Exception as e:
            print(f"[ERROR] Failed to write WAV: {e}")
            return

        whisper_cmd = [
            WHISPER_CLI,
            "-f", str(wav_file),
            "-m", MODEL_PATH,
            "-t", THREADS,
            "-ng",
            "-np",
            "-nt"
        ]

        try:
            result = subprocess.run(whisper_cmd, capture_output=True, text=True)
            transcription = result.stdout.strip()
            if transcription and transcription != "[BLANK_AUDIO]":
                seq = next(seq_gen)
                message = f"SEQ{seq}:{transcription}"
                async with send_lock:
                    # check websocket state instead of .closed
                    if websocket.state != websockets.protocol.State.OPEN:
                        print(f"[INFO] Client {client_addr} not open, skipping send")
                        return
                    await websocket.send(message)
                    print(f"[TRANSCRIBE] {client_addr}: {transcription}")
            else:
                print(f"[INFO] Skipped blank audio from {client_addr}")

        except Exception as e:
            print(f"[ERROR] Whisper failed: {e}")

    async def process_buffer_safe(pcm_bytes: bytes):
        """Wrapper to safely process buffer and catch disconnects"""
        try:
            await process_buffer(pcm_bytes)
        except websockets.ConnectionClosed:
            print(f"[INFO] Client {client_addr} disconnected, task canceled")
        except Exception as e:
            print(f"[ERROR] Exception in task for {client_addr}: {e}")

    try:
        async for message in websocket:
            if isinstance(message, str):
                message = message.encode("utf-8")

            buffer.write(message)
            now = time.time()

            if now - last_process_time >= PROCESS_INTERVAL:
                pcm_data = buffer.getvalue()
                buffer = BytesIO()  # reset buffer
                last_process_time = now
                task = asyncio.create_task(process_buffer_safe(pcm_data))
                tasks.add(task)
                task.add_done_callback(lambda t: tasks.discard(t))

    except websockets.ConnectionClosed:
        print(f"[INFO] Client disconnected: {client_addr}")
    except Exception as e:
        print(f"[ERROR] Client {client_addr} exception: {e}")
    finally:
        # Cancel any pending tasks for this client
        for t in tasks:
            t.cancel()
        print(f"[INFO] Cleaned up {len(tasks)} pending tasks for {client_addr}")


async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8181):
        print("[INFO] Server listening on ws://0.0.0.0:8181")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user")
