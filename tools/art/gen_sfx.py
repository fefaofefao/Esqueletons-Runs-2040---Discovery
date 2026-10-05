#!/usr/bin/env python3
"""Sintetiza os efeitos sonoros chiptune originais (WAV 16 bits, mono, 22050 Hz)."""
import math
import random
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RATE = 22050


def square(freq, t, duty=0.5):
    return 1.0 if (t * freq) % 1.0 < duty else -1.0


def tri(freq, t):
    p = (t * freq) % 1.0
    return 4 * abs(p - 0.5) - 1


def render(notes, wave_fn="square", volume=0.35, duty=0.5):
    """notes: lista de (freq_inicial, freq_final, duração, ataque, decaimento)."""
    out = []
    rnd = random.Random(7)
    for (f0, f1, dur, att, dec) in notes:
        n = int(dur * RATE)
        noise_val = 0.0
        for i in range(n):
            t = i / RATE
            k = i / max(1, n - 1)
            f = f0 + (f1 - f0) * k
            if wave_fn == "square":
                s = square(f, t, duty)
            elif wave_fn == "tri":
                s = tri(f, t)
            else:
                if i % max(1, int(RATE / max(f, 1))) == 0:
                    noise_val = rnd.uniform(-1, 1)
                s = noise_val
            env = min(1.0, t / att) if att > 0 else 1.0
            env *= max(0.0, 1.0 - max(0.0, t - (dur - dec)) / dec) if dec > 0 else 1.0
            out.append(s * env * volume)
    return out


def save(name, samples):
    path = ROOT / "assets" / "sfx" / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in samples))


def main():
    save("cursor", render([(880, 880, 0.035, 0.001, 0.02)], duty=0.25, volume=0.25))
    save("confirm", render([(660, 660, 0.05, 0.001, 0.02), (990, 990, 0.08, 0.001, 0.05)], duty=0.25))
    save("cancel", render([(520, 520, 0.05, 0.001, 0.02), (330, 330, 0.08, 0.001, 0.05)], duty=0.5))
    save("text", render([(1200, 1200, 0.018, 0.001, 0.01)], duty=0.125, volume=0.12))
    save("bump", render([(110, 70, 0.09, 0.002, 0.06)], wave_fn="tri", volume=0.6))
    save("door", render([(400, 120, 0.18, 0.002, 0.15)], wave_fn="noise", volume=0.3))
    save("menu_open", render([(523, 523, 0.04, 0.001, 0.02), (659, 659, 0.04, 0.001, 0.02),
                              (784, 784, 0.07, 0.001, 0.05)], duty=0.25, volume=0.25))
    save("speed_on", render([(440, 880, 0.12, 0.002, 0.05)], duty=0.25, volume=0.25))
    save("speed_off", render([(880, 440, 0.12, 0.002, 0.05)], duty=0.25, volume=0.25))
    save("save", render([(784, 784, 0.06, 0.001, 0.03), (1047, 1047, 0.12, 0.001, 0.08)], wave_fn="tri", volume=0.4))
    # Golden: arpejo brilhante
    save("golden", render([(1047, 1047, 0.06, 0.001, 0.03), (1319, 1319, 0.06, 0.001, 0.03),
                           (1568, 1568, 0.06, 0.001, 0.03), (2093, 2093, 0.22, 0.001, 0.18)], duty=0.125, volume=0.3))
    # Aniversário: melodia curta original (não é a canção tradicional)
    notes = [(523, 0.12), (659, 0.12), (784, 0.12), (1047, 0.24), (880, 0.12), (988, 0.12), (1047, 0.36)]
    save("birthday", render([(f, f, d, 0.004, d * 0.5) for f, d in notes], wave_fn="tri", volume=0.45))
    save("grow_flash", render([(200, 1800, 0.5, 0.01, 0.2)], duty=0.5, volume=0.25))
    save("blow", render([(900, 300, 0.35, 0.02, 0.25)], wave_fn="noise", volume=0.25))
    save("recruit", render([(659, 659, 0.08, 0.001, 0.04), (784, 784, 0.08, 0.001, 0.04), (1047, 1047, 0.2, 0.001, 0.15)], duty=0.25, volume=0.3))
    print("sfx gerados")


if __name__ == "__main__":
    main()
