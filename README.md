# Whisper Offline Voice Assistant

Offline voice assistant for Linux using **Whisper.cpp** with **CUDA acceleration**.  
This project provides fully offline speech recognition and voice-controlled command execution through KDE utilities such as `xdotool` and `qdbus`.

---

## 🚀 Features

- **100% offline**: no API keys, no cloud services, no internet required.  
- **GPU acceleration** via Whisper.cpp compiled with CUDA.  
- **Temporary in-memory audio processing** — no persistent files are written to disk.  
- **Voice command automation** for KDE (open applications, control system, etc.).  
- **Optimized for Spanish**, using the `ggml-medium` model.  
- Works seamlessly on **Debian KDE** and other Linux distributions.

---

## 🧩 Requirements

- NVIDIA GPU with CUDA 12+
- GCC, CMake, and Git
- Conda or Python 3.11+
- `sox` and `xdotool` installed system-wide

---

## 🧰 Setup

### 1. Create a virtual environment

```bash
conda create -n whisper python=3.11
conda activate whisper
```

### 2. Install Python dependencies

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install sounddevice numpy
```

### 3. Build Whisper.cpp with CUDA

```bash
cd /opt
sudo git clone https://github.com/ggerganov/whisper.cpp
sudo chown -R $USER:$USER whisper.cpp
cd whisper.cpp
mkdir build && cd build
cmake -DGGML_CUDA=ON ..
make -j$(nproc)
```

### 4. Download the model

```bash
cd /opt/whisper.cpp
bash ./models/download-ggml-model.sh medium
```

---

## 🧠 How It Works

The assistant continuously records short 5-second audio blocks using the system microphone,  
transcribes them through `whisper-cli` (CUDA backend), and executes KDE commands according to recognized phrases.

All audio processing happens **in memory** — only short-lived temporary files are used for Whisper.cpp input and are deleted immediately after processing.

The available commands are **easily configurable** inside the Python script (`assistant.py`).  
You can add or modify any phrase–action pair to launch programs, simulate key presses, or control system functions.

Example commands supported:
- “abrir firefox”
- “abrir dolphin”
- “abrir correo”
- “abrir mezcla” / “dj”
- “abrir editor”
- “cerrar sesión”
- “reiniciar”
- “apagar”
- “escanear” → simula `Ctrl+S`
- “guardar” → simula `Return`
- “salir” → termina el asistente

---

## ⚡ Performance

| Model | Size | Speed (approx) | Accuracy |
|--------|------|----------------|-----------|
| tiny / tiny.en | 75 MB | 32× real time | low |
| base / base.en | 142 MB | 16× real time | medium |
| small / small.en | 466 MB | 6× real time | good |
| **medium** | **1.5 GB** | **2× real time** | **high** |
| large-v3 | 3 GB | 1× real time | very high |

---

## 🧾 License

This project includes two main components under different licenses:

### 1. Whisper.cpp
Originally developed by **Georgi Gerganov**, licensed under the [MIT License](https://github.com/ggerganov/whisper.cpp/blob/master/LICENSE).

### 2. Voice Assistant Code (this repository)
All original Python and integration code — including the voice assistant logic, command automation, and configuration —  
is © 2025 **X Software** and released under the **MIT License**.

You are free to use, modify, and redistribute the software provided that:
- Attribution to **X Software** is maintained.
- The license text is included with any distributed version.
- Whisper.cpp retains its original author and license notice.

---

## 🧑‍💻 Author

Developed by **X Software**  
Linux software development, web solutions, and system automation.
