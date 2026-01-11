import asyncio
import json
import time
from pathlib import Path
from aiohttp import ClientSession
from aioamazondevices.api import AmazonEchoApi
from fastapi import FastAPI, HTTPException, Query, Request
import uvicorn
import atexit
import socket
from contextlib import asynccontextmanager

# --------------------------
# Before running generate 'login_data.json' using:
# git clone https://github.com/chemelli74/aioamazondevices.git
# cd aioamazondevices/
# python library_test.py --email "your_amazon_alexa_email" --password "your_amazon_alexa_password"
#
# If OTP is not enabled in Alexa you will need to enable it:
# https://www.amazon.co.uk/gp/help/customer/display.html?nodeId=201962400
# https://www.amazon.co.uk/gp/css/account/info/view.html
# --------------------------

LOGIN_DATA_FILE = "login_data.json"

# --------------------------
# Globals
# --------------------------
API_INSTANCE = None
CLIENT_SESSION = None
DEVICES = []
SELECTED_DEVICE = None
SERVER_IP = None
SERVER_PORT = 8002  # default

# --------------------------
# Cleanup
# --------------------------
def close_client_session():
    global CLIENT_SESSION
    if CLIENT_SESSION and not CLIENT_SESSION.closed:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(CLIENT_SESSION.close())
            else:
                loop.run_until_complete(CLIENT_SESSION.close())
        except RuntimeError:
            pass
        print("[INFO] Client session closed")

atexit.register(close_client_session)

# --------------------------
# Helper: get LAN IP
# --------------------------
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# --------------------------
# FastAPI Lifespan
# --------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global SERVER_IP
    print("[INFO] Starting TTS COSMO Server...")
    SERVER_IP = get_lan_ip()
    await init_api()
    print("[INFO] Speech is ready")

    # --------------------------
    # Announce automatically on server start
    # --------------------------
    startup_message = "hmmmm, Finally, you got me talking! Took you long enough—almost ages!"
    await send_announcement(startup_message)

    print(f"COSMO API available. Try -> http://{SERVER_IP}:{SERVER_PORT}/speak?t=hi")
    yield

    # Optionally, cleanup after shutdown
    close_client_session()

app = FastAPI(title="COSMO TTS", lifespan=lifespan)

# --------------------------
# Initialize API & prompt device selection
# --------------------------
async def init_api():
    global API_INSTANCE, CLIENT_SESSION, DEVICES, SELECTED_DEVICE

    if API_INSTANCE:
        return API_INSTANCE

    if not Path(LOGIN_DATA_FILE).exists():
        raise RuntimeError(f"Login data not found: {LOGIN_DATA_FILE}")

    with open(LOGIN_DATA_FILE) as f:
        login_data = json.load(f)

    CLIENT_SESSION = ClientSession()
    API_INSTANCE = AmazonEchoApi(
        client_session=CLIENT_SESSION,
        login_email="",
        login_password="",
        login_data=login_data,
        save_to_file=None,
    )

    t0 = time.time()
    await API_INSTANCE.login.login_mode_stored_data()
    print(f"[INFO] Logged in ({time.time() - t0:.3f}s)")

    # --------------------------
    # Load devices
    # --------------------------
    devices_dict = await API_INSTANCE.get_devices_data()
    DEVICES = list(devices_dict.values())

    print("\nAvailable Alexa devices:")
    for i, d in enumerate(DEVICES):
        print(
            f" {i}. {d.account_name} | "
            f"serial='{d.serial_number}' | "
            f"type='{d.device_type}'"
        )

    # --------------------------
    # Prompt user selection
    # --------------------------
    while True:
        try:
            choice = input("\nSelect COSMO speech device: ").strip()
            index = int(choice)
            SELECTED_DEVICE = DEVICES[index]
            break
        except (ValueError, IndexError):
            print("Invalid selection, try again.")

    print(
        f"\n[INFO] Selected device → "
        f"{SELECTED_DEVICE.account_name} "
        f"({SELECTED_DEVICE.serial_number})\n"
    )

    return API_INSTANCE

# --------------------------
# Send announcement
# --------------------------
async def send_announcement(message: str):
    api = await init_api()
    t0 = time.time()
    await api.call_alexa_announcement(SELECTED_DEVICE, message)
    print(
        f"[INFO] COSMO speaks on "
        f"{SELECTED_DEVICE.account_name} "
        f"({time.time() - t0:.3f}s)"
    )

# --------------------------
# API endpoint (GET)
# --------------------------
@app.get("/speak")
async def announce(
    request: Request,
    t: str = Query(..., description="Text to speak"),
):
    if not t.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    spoken_text = t
    await send_announcement(spoken_text)

    return {
        "status": "success",
        "device": SELECTED_DEVICE.account_name,
        "message": t,
    }

# --------------------------
# Run
# --------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)