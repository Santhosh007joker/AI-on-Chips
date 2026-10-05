import serial
import wave
import time
import threading

PORT = "COM24"
BAUD = 921600
SAMPLE_RATE = 16000

print("Opening serial port...")
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.setDTR(False)
ser.setRTS(False)

print("Waiting for ESP32 to boot...")
time.sleep(2.5)
ser.reset_input_buffer()

print("Setup complete. Ready to record.\n")

while True:
    filename_input = input("Enter a name for this recording (or type 'quit' to exit): ").strip()

    if filename_input.lower() == "quit":
        print("Exiting program.")
        break

    filename = filename_input + ".wav"

    audio_data = bytearray()
    stop_flag = False

    def read_loop():
        global audio_data
        while not stop_flag:
            chunk = ser.read(1024)
            if chunk:
                audio_data.extend(chunk)

    ser.write(b'r')
    reader_thread = threading.Thread(target=read_loop)
    reader_thread.start()
    start_time = time.time()

    print("Recording... Press ENTER to stop.")
    input()

    ser.write(b's')
    time.sleep(0.5)
    stop_flag = True
    reader_thread.join()
    elapsed = time.time() - start_time

    num_bytes = len(audio_data)

    print(f"Bytes collected: {num_bytes}")
    print(f"Duration: {elapsed:.2f} seconds")
    print(f"Filename: {filename}")

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(bytes(audio_data))
    wf.close()

    print(f"Successfully saved: {filename}\n")
    ser.reset_input_buffer()
