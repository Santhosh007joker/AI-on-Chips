# AI-on-Chips
A Step-by-Step guide for creating your first AI, working entirely on a MicroController

---

## Table of Contents

1. [Arduino IDE](#1-arduino-ide)
2. [Python 3.14](#2-python-314)
3. [Installing pyserial](#3-installing-pyserial)

---

## 1. Arduino IDE

| Item | Link |
|------|------|
| **Official download page** | <https://www.arduino.cc/en/software> |

Pick the installer for your OS (Windows, macOS, Linux) from the download page and run it.

---

### Add ESP32 to the Arduino IDE

1. Open **File → Preferences**.
2. In **Additional boards manager URLs**, paste:

   ```text
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```

3. Open **Tools → Board → Boards Manager**.
4. Search for **esp32** (by Espressif Systems) and click **Install**.
5. Select your board under **Tools → Board → esp32** (e.g. *ESP32 Dev Kit*).

---

## 2. Python 3.14

| Item | Link |
|------|------|
| **Python 3.14.7 download page** | <https://www.python.org/downloads/> |

During installation on Windows, tick **"Add python.exe to PATH"**.

---

## 4. Installing pyserial

### Option 1: Standard

```bash
pip install pyserial
```

### Option 2: Recommended (uses the pip tied to your Python)

```bash
python -m pip install pyserial
```

### Option 3: Extreme case (force a clean reinstall)

```bash
python -m pip install --force-reinstall pyserial
```

### If `python` is not recognised

| OS | Try this instead |
|----|------------------|
| Windows | `py -m pip install pyserial` |
| Linux / macOS | `python3 -m pip install pyserial` |


Audio database <https://drive.google.com/drive/u/1/folders/1h3GVJuJ_RJXA6AAGGDZRt_p16EmRTlnB>
