import re
import time
import webbrowser

import serial
from serial.tools import list_ports

# ---------------- SETTINGS ----------------
PORT = None            # e.g. "COM24". None = auto-detect
BAUD = 115200
THRESHOLD = 0.80       # minimum confidence to trigger
GLOBAL_LOCKOUT = 0.5       # seconds: after ANY site opens, no other site can open
DEFAULT_COOLDOWN = 3   # seconds, for any keyword not listed below
DEBUG = False          # True = print every score

# ---------------- KEYWORD -> WEBSITE ----------------
# If a label CONTAINS the keyword (case-insensitive), the action runs.
ACTIONS = {
    "wifi":     lambda: webbrowser.open("https://internet.iitb.ac.in/"),
    "internet": lambda: webbrowser.open("https://internet.iitb.ac.in/"),
    "mail":     lambda: webbrowser.open("https://webmail.iitb.ac.in/?_task=mail&_mbox=INBOX"),
    "moodle":   lambda: webbrowser.open("https://moodle.iitb.ac.in/login/index.php"),
}

# Minimum seconds before the SAME site can open again
COOLDOWNS = {
    "wifi":     3,
    "internet": 5,
    "mail":     7,
    "moodle":   5,
}

# ---------------- INTERNALS ----------------
LINE_RE = re.compile(r"^\s+(.+?):\s*(-?\d+(?:\.\d+)?)\s*$")
last_fired = {}        # per keyword: time it last opened
last_any_fired = 0     # time any site last opened
armed = {}             # per keyword: True = ready to fire
seen_labels = set()


def find_port():
    if PORT:
        return PORT
    for p in list_ports.comports():
        desc = (p.description or "").lower()
        if any(k in desc for k in ("cp210", "ch340", "ch910", "usb serial", "usb-serial")):
            return p.device
    ports = list_ports.comports()
    return ports[0].device if ports else None


def handle(label, score):
    global last_any_fired

    if DEBUG:
        print(f"{label}: {score:.2f}")

    if label not in seen_labels:
        seen_labels.add(label)
        print(f"[seen label] '{label}'")

    key = next((k for k in ACTIONS if k in label.lower()), None)
    if key is None:
        return

    if score < THRESHOLD:
        armed[key] = True          # label went quiet, re-arm it
        return

    if not armed.get(key, True):
        return                     # same utterance still going, ignore
    armed[key] = False             # used up for this utterance, fired or not

    now = time.time()

    # global lockout: some site opened very recently
    if now - last_any_fired < GLOBAL_LOCKOUT:
        return

    # per-site cooldown
    if now - last_fired.get(key, 0) < COOLDOWNS.get(key, DEFAULT_COOLDOWN):
        return

    last_fired[key] = now
    last_any_fired = now

    print(f"[TRIGGER] {label} ({score:.2f}) -> {key}")
    try:
        ACTIONS[key]()
    except Exception as e:
        print(f"[ERROR] {key} failed: {e}")


def open_and_reset(port):
    """Open the port with DTR/RTS in a safe state, then pulse a clean reset."""
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = BAUD
    ser.timeout = 1
    ser.dtr = False        # GPIO0 high = normal boot, not download mode
    ser.rts = False        # EN high = not held in reset
    ser.open()
    ser.rts = True         # pulse EN low = reset the board
    time.sleep(0.1)
    ser.rts = False
    ser.reset_input_buffer()
    return ser


def main():
    while True:
        port = find_port()
        if not port:
            print("No serial port found, retrying in 3s...")
            time.sleep(3)
            continue

        ser = None
        try:
            print(f"Connecting to {port}...")
            ser = open_and_reset(port)
            armed.clear()
            print("Listening. Ctrl+C to stop. (ESP32 takes ~5-10 s to start printing)")
            while True:
                raw = ser.readline().decode(errors="ignore")
                m = LINE_RE.match(raw)
                if m:
                    handle(m.group(1), float(m.group(2)))
        except serial.SerialException as e:
            print(f"Serial error: {e}. Reconnecting in 3s...")
            time.sleep(3)
        except KeyboardInterrupt:
            print("Stopped.")
            break
        finally:
            if ser is not None and ser.is_open:
                ser.close()


if __name__ == "__main__":
    main()
