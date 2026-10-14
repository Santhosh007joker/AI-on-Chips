import sys
import time
import wave
import threading

import serial
from serial.tools import list_ports

# ---------------- SETTINGS ----------------
PORT = None            # e.g. "COM24". None = auto-detect
BAUD = 921600
SAMPLE_RATE = 16000


# ---------------- PORT DETECTION ----------------
def find_port():
    if PORT:
        return PORT

    ports = list(list_ports.comports())

    # Prefer typical ESP32 USB-serial chips
    for p in ports:
        desc = (p.description or "").lower()
        if any(k in desc for k in ("cp210", "ch340", "ch910", "usb serial", "usb-serial")):
            return p.device

    # Fallback: first port found (may not be the ESP32)
    return ports[0].device if ports else None


def open_port(port):
    """Open with DTR/RTS low BEFORE opening, to avoid resetting/bootloader mode."""
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = BAUD
    ser.timeout = 1
    ser.dtr = False
    ser.rts = False
    ser.open()
    return ser


# ---------------- RECORDING ----------------
def record(ser, filename):
    audio_data = bytearray()
    stop_event = threading.Event()

    def read_loop():
        while not stop_event.is_set():
            chunk = ser.read(1024)
            if chunk:
                audio_data.extend(chunk)

    ser.reset_input_buffer()
    ser.write(b"r")
    reader = threading.Thread(target=read_loop, daemon=True)
    reader.start()
    start_time = time.time()

    print("Recording... Press ENTER to stop.")
    input()

    ser.write(b"s")
    time.sleep(0.5)          # let the last bytes arrive
    stop_event.set()
    reader.join()
    elapsed = time.time() - start_time

    # 16-bit samples -> keep an even number of bytes
    if len(audio_data) % 2:
        audio_data = audio_data[:-1]

    print(f"Bytes collected: {len(audio_data)}")
    print(f"Duration: {elapsed:.2f} seconds")
    print(f"Filename: {filename}")

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(bytes(audio_data))

    print(f"Successfully saved: {filename}\n")


def main():
    port = find_port()
    if not port:
        sys.exit("No serial port found. Is the ESP32 plugged in?")

    print(f"Opening serial port {port}...")
    try:
        ser = open_port(port)
    except serial.SerialException as e:
        sys.exit(f"Could not open {port}: {e}")

    try:
        print("Waiting for ESP32 to boot...")
        time.sleep(2.5)
        ser.reset_input_buffer()
        print("Setup complete. Ready to record.\n")

        while True:
            name = input("Enter a name for this recording (or type 'quit' to exit): ").strip()

            if name.lower() == "quit":
                print("Exiting program.")
                break
            if not name:
                print("Please enter a name.\n")
                continue

            record(ser, name + ".wav")

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        if ser.is_open:
            ser.close()


if __name__ == "__main__":
    main()
