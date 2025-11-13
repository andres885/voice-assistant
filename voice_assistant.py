#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import subprocess
import tempfile
import os
import time

# Configuración
WHISPER_DIR = "/opt/whisper.cpp"
MODEL = f"{WHISPER_DIR}/models/ggml-medium.bin"
BIN = f"{WHISPER_DIR}/build/bin/whisper-cli"
LANG = "es"
SAMPLE_RATE = 16000
BLOCK_DURATION = 5  # segundos por bloque de audio

print("Asistente de voz iniciado (Ctrl+C para salir)...")

def transcribe_block(audio):
    """Guarda el bloque, lo envía a whisper-cli y devuelve texto"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        path = f.name
        # Guardar audio en formato WAV (16-bit PCM)
        subprocess.run([
            "sox", "-t", "raw", "-r", str(SAMPLE_RATE), "-b", "16",
            "-e", "signed-integer", "-c", "1", "-", path
        ], input=audio.tobytes())
    # Ejecutar Whisper.cpp
    result = subprocess.run(
        [BIN, "-m", MODEL, "-f", path, "-l", LANG, "--output-txt", "-otxt"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )
    os.remove(path)
    lines = result.stdout.strip().splitlines()
    return lines[-1].lower() if lines else ""

def execute_command(text):
    """Ejecuta comandos KDE según la frase reconocida"""
    print(f"Has dicho: {text}")

    if "abrir firefox" in text:
        subprocess.Popen(["firefox"])
    elif "abrir dolphin" in text:
        subprocess.Popen(["dolphin"])
    elif "abrir correo" in text:
        subprocess.Popen(["kmail"])
    elif "abrir mezcla" in text or "dj" in text:
        subprocess.Popen(["mixxx"])
    elif "abrir editor" in text or "código" in text:
        subprocess.Popen(["kate"])
    elif "cerrar sesión" in text:
        subprocess.Popen(["qdbus", "org.kde.ksmserver", "/KSMServer", "logout", "0", "0", "0"])
    elif "reiniciar" in text:
        subprocess.Popen(["systemctl", "reboot"])
    elif "apagar" in text:
        subprocess.Popen(["systemctl", "poweroff"])
    elif "escanear" in text:
        subprocess.run(["xdotool", "key", "ctrl+s"])
    elif "guardar" in text:
        subprocess.run(["xdotool", "key", "Return"])
    elif "salir" in text:
        print("Saliendo...")
        raise KeyboardInterrupt
    else:
        print("No se reconoce el comando.")

try:
    while True:
        print("🎙️  Escuchando...")
        audio = sd.rec(int(SAMPLE_RATE * BLOCK_DURATION), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
        sd.wait()
        text = transcribe_block(audio)
        if text.strip():
            execute_command(text)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nAsistente detenido.")
