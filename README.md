# AI-on-Chips
A Step-by-Step guide for creating your first AI, working entirely on a MicroController

---

## Table of Contents

1. [Arduino IDE](#1-arduino-ide)
2. [Python 3.15](#3-python-315)
3. [Installing pyserial](#4-installing-pyserial)
4. [Quick Verification](#5-quick-verification)

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

## 2. Python 3.15

| Item | Link |
|------|------|
| **Python 3.15.0 download page** | <https://www.python.org/downloads/release/python-3150/> |

> **Note:** Python 3.15 is a brand-new release. If the final 3.15.0 page is not
> available for your platform yet, use the release candidate link above.
> Some third-party packages may not support 3.15 yet. If `pyserial` or other
> tools give errors, a stable version like **3.13** or **3.14** is a safer choice.

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

> **Tip:** Note it is `--force-reinstall` (one word, double dash). Writing
> `--force - install` will not work.

### If `python` is not recognised

| OS | Try this instead |
|----|------------------|
| Windows | `py -m pip install pyserial` |
| Linux / macOS | `python3 -m pip install pyserial` |

### Other useful commands

```bash
# Upgrade pip itself
python -m pip install --upgrade pip

# Upgrade pyserial
python -m pip install --upgrade pyserial

# Check the installed version
python -m pip show pyserial
```

---

## 5. Quick Verification

```bash
python --version
python -c "import serial; print(serial.__version__)"
```

List available serial ports (to find your ESP32):

```bash
python -m serial.tools.list_ports
```

---

## Troubleshooting

- **Port not showing up:** install the USB driver for your board's chip
  (CP210x or CH340) and try a different data-capable USB cable.
- **Permission denied on Linux:** add yourself to the `dialout` group:

  ```bash
  sudo usermod -a -G dialout $USER
  ```

  Then log out and back in.
- **`pip` not found:** use `python -m pip ...` instead.
