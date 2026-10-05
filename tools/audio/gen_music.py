#!/usr/bin/env python3
"""Músicas chiptune originais do jogo (seção 15 do AGENTS.md).

Quatro canais no estilo dos consoles portáteis: dois pulsos (melodia e
arpejo/contracanto), triângulo (baixo) e ruído (bateria). Cada faixa é escrita
aqui em notação de graus da escala e renderizada com numpy; o ffmpeg converte
para OGG Vorbis (assets/music/<id>.ogg). As faixas de mapa e batalha fecham o
laço sem emenda: a cauda do último compasso volta para o começo.

Notação da melodia: um compasso por "|", 8 colcheias por compasso.
  1..7   grau da escala do modo da faixa   ' = oitava acima, , = oitava abaixo
  b / #  bemol / sustenido antes do grau   (ex.: b2, #4')
  .      prolonga a nota anterior          -  pausa
Acordes: "<semitons a partir da tônica><M|m|d>" (M maior, m menor, d diminuto),
um por compasso. Bateria: 16 semicolcheias por compasso (k bumbo, s caixa,
h chimbal, - nada).

Uso: python3 tools/audio/gen_music.py [id ...]
"""
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/music"
SR = 32000

MODES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "harmonic": [0, 2, 3, 5, 7, 8, 11],
    "phrygian_dom": [0, 1, 4, 5, 7, 8, 10],
}
QUAL = {"M": [0, 4, 7], "m": [0, 3, 7], "d": [0, 3, 6]}
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}

# ----------------------------------------------------------------------------- faixas
# key: tônica (a melodia fica na 5ª oitava; o baixo duas oitavas abaixo)
TRACKS = {
    "titulo": dict(
        bpm=112, key="D", mode="major", loop=True,
        chords="0M 7M 9m 5M 0M 7M 5M 7M",
        melody="1 . 3 . 5 . 3 5 | 5 . 4 3 2 . 7, . | 6 . 5 6 1' . 6 . | 5 . 4 . 3 . - - |"
               "1 . 3 . 5 . 1' . | 7 . 5 . 2' . 1' 7 | 6 . . 4 6 . 1' . | 7 . . . 5 . - -",
        bass="rootfifth", arp="up16", drums="k---h---s---h-h-", duty=0.5),
    "praia": dict(
        bpm=96, key="F", mode="major", loop=True,
        chords="0M 9m 5M 7M 0M 9m 5M 7M",
        melody="3 . 2 1 . 5, 1 2 | 3 . . 1 6, . - - | 4 . 3 4 6 . 5 4 | 2 . 7, . 5, . - - |"
               "3 . 2 1 . 5, 1 2 | 3 . 5 . 6 . 5 3 | 4 . 6 . 1' . 6 4 | 2 . 3 . 1 . - -",
        bass="half", arp="up8", drums="k-------s---h---", duty=0.25),
    "bosque": dict(
        bpm=104, key="D", mode="dorian", loop=True,
        chords="0m 5M 0m 10M 0m 5M 10M 0m",
        melody="1 . 2 3 5 . 3 2 | 4 . 3 4 6 . 5 4 | 3 . 1 . 5 . 6 5 | 4 . 2 . 7, . - - |"
               "1' . 7 6 5 . 6 7 | 1' . 6 . 4 . 6 . | 7 . 5 . 4 . 2 . | 1 . . . 5, . - -",
        bass="walk", arp="up8", drums="k---h-h-s---h---", duty=0.25),
    "minas": dict(
        bpm=116, key="E", mode="minor", loop=True,
        chords="0m 0m 8M 10M 0m 5m 8M 10M",
        melody="1 . - 1 3 . 2 1 | 5, . - 5, 7, . 1 . | 3 . - 3 6 . 5 3 | 4 . 2 . 7, . 2 . |"
               "1 . 3 . 5 . 7 . | 6 . 4 . 1' . 6 . | 5 . 3 . 6 . 5 3 | 2 . . . 7, . - -",
        bass="root8", arp="none", drums="k-k-s---k-k-s-h-", duty=0.5),
    "pantano": dict(
        bpm=88, key="C", mode="phrygian", loop=True,
        chords="0m 1M 0m 10m 5m 1M 8M 1M",
        melody="1 . 2 1 7, . 1 . | 2 . 4 . 6 . 4 2 | 3 . 1 . 5 . 3 1 | 7, . 2 . 4 . - - |"
               "4 . 6 . 1' . 6 4 | 2' . 1' . 6 . 4 . | 6 . 1' . 3' . 1' 6 | 2 . 1 . 7, . 1 .",
        bass="half", arp="up16", drums="k-----h-s-----h-", duty=0.125),
    "ossorio": dict(
        bpm=120, key="Bb", mode="major", loop=True,
        chords="0M 5M 7M 0M 9m 5M 7M 0M",
        melody="1 . 1 1 3 . 1 . | 4 . 4 4 6 . 4 . | 5 . 5 6 7 . 5 . | 1' . . . 5 . - - |"
               "6 . 6 5 6 . 1' . | 4 . 6 . 1' . 6 4 | 2' . 1' 7 2' . 7 5 | 1' . . . - - - -",
        bass="rootfifth", arp="none", drums="k---s-s-k---s-ss", duty=0.5),
    "picos": dict(
        bpm=80, key="A", mode="minor", loop=True,
        chords="0m 8M 3M 10M 0m 5m 8M 10M",
        melody="5 . . 6 5 . 3 . | 1 . . 3 6 . 5 . | 5 . . 3 2 . 1 . | 2 . . . - - - - |"
               "1' . . 7 6 . 5 . | 6 . . 4 1' . 6 . | 5 . 3 . 1 . 3 . | 2 . . . 7, . - -",
        bass="half", arp="up16", drums="----------------", duty=0.25),
    "deserto": dict(
        bpm=100, key="E", mode="phrygian_dom", loop=True,
        chords="0M 1M 0M 10m 5m 5m 1M 0M",
        melody="1 . 2 3 2 . 1 . | 2 . 3 4 3 . 2 . | 5 . 6 5 3 . 2 3 | 4 . 2 . 7, . - - |"
               "4 . 5 6 5 . 4 . | 1' . 7 6 5 . 6 . | 6 . 4 . 2 . 4 . | 3 . 2 . 1 . - -",
        bass="gallop", arp="none", drums="k--hk-s-k--hk-s-", duty=0.25),
    "castelo": dict(
        bpm=92, key="C", mode="harmonic", loop=True,
        chords="0m 5m 7M 0m 8M 5m 7M 0m",
        melody="1 . 3 . 5 . 1' . | 1' . 6 . 4 . 6 . | 7 . 2' . 5 . 7 . | 1' . . . 5 . - - |"
               "6 . 1' . 3' . 1' 6 | 4 . 6 . 1' . 6 4 | 2' . 1' 7 2' . 5 7 | 1' . . . - - - -",
        bass="half", arp="up16", drums="k-------k---s---", duty=0.5),
    "batalha": dict(
        bpm=150, key="A", mode="minor", loop=True,
        chords="0m 8M 10M 0m 0m 8M 5m 10M",
        melody="1 . 1 5, 1 . 3 . | 3 . 1 3 6 . 5 . | 4 . 2 4 7 . 6 5 | 5 . . . 3 2 1 . |"
               "1' . 7 6 5 . 6 7 | 1' . 6 . 3 . 1 3 | 4 . 6 . 1' . 6 4 | 2 . 4 . 7 . 2' .",
        bass="root8", arp="up16", drums="k-h-s-h-k-h-s-hk", duty=0.5),
    "chefe": dict(
        bpm=160, key="D", mode="harmonic", loop=True,
        chords="0m 0m 1M 0m 5m 5m 7M 7M",
        melody="1 . 1 . 5 . 4 3 | 2 . 1 . 7, . 1 . | b2 . 4 . 6 . 4 b2 | 1 . . . - 5, 7, 1 |"
               "4 . 3 4 6 . 4 . | 1' . 7 6 4 . 6 . | 7 . 6 7 2' . 7 . | 5 . 7 . 2' . 7 5",
        bass="gallop", arp="up16", drums="k-hsk-hsk-hsk-ss", duty=0.5),
    "rei": dict(
        bpm=140, key="C", mode="harmonic", loop=True,
        chords="0m 0m 8M 7M 5m 8M 7M 7M",
        melody="1' . 7 1' 5 . 3 . | 1 . 3 5 1' . 3' . | 3' . 1' 6 3 . 6 . | 7 . . . 5 . 7 . |"
               "4' . 3' 4' 1' . 6 . | 3' . 1' . 6 . 3 . | 2' . 7 . 5 . 2' . | 7 . 5 . 2 . 7, .",
        bass="root8", arp="up16", drums="k-s-k-s-k-s-kkss", duty=0.5),
    # vinhetas (sem laço)
    "aniversario": dict(
        bpm=140, key="C", mode="major", loop=False,
        chords="0M 7M 0M",
        melody="5 . 1' . 3' . 1' 5 | 7 . 2' . 5' . 4' 2' | 1'' . . . . . - -",
        bass="half", arp="up8", drums="k---s---k---s-s-", duty=0.25),
    "golden": dict(
        bpm=168, key="E", mode="major", loop=False,
        chords="0M 5M 0M",
        melody="1 3 5 1' 3' 5' 1'' . | 6' . 4' 6' 1'' . 3'' . | 1'' . . . . . - -",
        bass="half", arp="up16", drums="----h-h-s-h-hhhh", duty=0.125),
}


# ----------------------------------------------------------------------------- partitura
def parse_melody(text, mode, key_midi):
    """Devolve [(início_em_colcheias, duração_em_colcheias, midi)]."""
    tokens = []
    for bar in text.split("|"):
        bt = bar.split()
        if not bt:
            continue
        assert len(bt) == 8, f"compasso com {len(bt)} colcheias: {bar}"
        tokens += bt
    notes = []
    for i, tok in enumerate(tokens):
        if tok == ".":
            if notes and notes[-1][0] + notes[-1][1] == i:
                s, d, m = notes[-1]
                notes[-1] = (s, d + 1, m)
            continue
        if tok == "-":
            continue
        acc = 0
        while tok[0] in "b#":
            acc += -1 if tok[0] == "b" else 1
            tok = tok[1:]
        deg = int(tok[0])
        octv = tok.count("'") - tok.count(",")
        midi = key_midi + MODES[mode][deg - 1] + acc + 12 * octv
        notes.append((i, 1, midi))
    return notes, len(tokens)


def chord_tones(spec, key_midi):
    root = key_midi + int(spec[:-1])
    return root, [root + q for q in QUAL[spec[-1]]]


def harmonize(notes, mode, key_midi):
    """Contracanto: a nota da escala uma terça abaixo da melodia."""
    scale = MODES[mode]
    out = []
    for s, d, m in notes:
        rel = (m - key_midi) % 12
        octv = (m - key_midi) // 12
        if rel in scale:
            i = scale.index(rel) - 2
            o = octv + (i // 7)
            out.append((s, d, key_midi + scale[i % 7] + 12 * o))
        else:
            out.append((s, d, m - 3))
    return out


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ----------------------------------------------------------------------------- síntese
def env(n, attack=0.004, decay=0.12, sustain=0.65, release=0.02):
    e = np.ones(n)
    a = max(1, int(attack * SR))
    d = max(1, int(decay * SR))
    r = max(1, int(release * SR))
    e[:a] = np.linspace(0, 1, a)[: min(a, n)] if n >= a else np.linspace(0, 1, n)
    if n > a:
        k = min(d, n - a)
        e[a:a + k] = np.linspace(1, sustain, d)[:k]
        e[a + k:] = sustain
    if n > r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def osc(kind, freq, n, duty=0.5, vibrato=False):
    t = np.arange(n) / SR
    f = np.full(n, freq)
    if vibrato and n > SR * 0.25:
        start = int(SR * 0.18)
        f[start:] *= 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t[start:])
    phase = np.cumsum(f) / SR
    frac = phase % 1.0
    if kind == "pulse":
        return np.where(frac < duty, 1.0, -1.0)
    if kind == "tri":
        tri = 4 * np.abs(frac - 0.5) - 1
        return np.round(tri * 7.5) / 7.5  # 16 degraus, como o canal do console
    raise ValueError(kind)


def noise(n, seed, bright=1.0):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n)
    if bright > 1.0:
        x = np.diff(np.concatenate([[0.0], x]))  # mais agudo
    return x


def drum(kind, seed):
    if kind == "k":
        n = int(0.14 * SR)
        t = np.arange(n) / SR
        f = 120 * np.exp(-t * 28) + 42
        body = np.sin(2 * np.pi * np.cumsum(f) / SR)
        return (body * np.exp(-t * 22) + 0.15 * noise(n, seed) * np.exp(-t * 90)) * 1.1
    if kind == "s":
        n = int(0.16 * SR)
        t = np.arange(n) / SR
        return noise(n, seed) * np.exp(-t * 26) * 0.75 + 0.25 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 35)
    if kind == "h":
        n = int(0.04 * SR)
        t = np.arange(n) / SR
        return noise(n, seed, bright=2.0) * np.exp(-t * 110) * 0.45
    return np.zeros(1)


def render(tid, tr):
    # tônicas de F# a B descem uma oitava para a melodia não ficar estridente
    key_midi = 60 + NOTE[tr["key"]] - (12 if NOTE[tr["key"]] > 6 else 0)
    mode = tr["mode"]
    eighth = 60.0 / tr["bpm"] / 2
    chords = tr["chords"].split()
    mel, steps = parse_melody(tr["melody"], mode, key_midi + 12)
    bars = steps // 8
    assert bars == len(chords), f"{tid}: {bars} compassos e {len(chords)} acordes"
    passes = 2 if tr["loop"] else 1
    total_steps = steps * passes
    tail = 1.0
    n_total = int(total_steps * eighth * SR) + int(tail * SR)
    mix = {c: np.zeros(n_total) for c in ["mel", "arp", "bass", "drum"]}

    def put(ch, start_s, sig):
        i = int(start_s * SR)
        j = min(n_total, i + len(sig))
        mix[ch][i:j] += sig[: j - i]

    for p in range(passes):
        off = p * steps
        # melodia (2ª passada: duty diferente, para variar a cor)
        duty = tr["duty"] if p == 0 else (0.25 if tr["duty"] != 0.25 else 0.5)
        for s, d, m in mel:
            n = int(d * eighth * SR * 0.95)
            sig = osc("pulse", midi_hz(m), n, duty, vibrato=d >= 3) * env(n, sustain=0.7)
            put("mel", (off + s) * eighth, sig)
        # 2ª passada: contracanto em terças no lugar do arpejo
        if p == 1:
            for s, d, m in harmonize(mel, mode, key_midi + 12):
                n = int(d * eighth * SR * 0.9)
                put("arp", (off + s) * eighth, osc("pulse", midi_hz(m - 12), n, 0.125) * env(n, sustain=0.5) * 0.9)
        for b, spec in enumerate(chords):
            root, tones = chord_tones(spec, key_midi)
            bar_t = (off + b * 8) * eighth
            # arpejo
            if p == 0 and tr["arp"] != "none":
                sub = 4 if tr["arp"] == "up16" else 2
                seq = tones + [tones[1]]
                for k in range(8 * sub // 2):
                    m = seq[k % len(seq)]
                    n = int(eighth / (sub / 2) * SR * 0.8)
                    put("arp", bar_t + k * eighth / (sub / 2), osc("pulse", midi_hz(m), n, 0.125) * env(n, decay=0.05, sustain=0.3))
            # baixo (triângulo, três oitavas abaixo da melodia: ~65–125 Hz)
            b0 = root - 24
            style = tr["bass"]
            if style == "root8":
                pat = [(i, 1, b0 if i % 4 != 3 else b0 + 12) for i in range(8)]
            elif style == "rootfifth":
                pat = [(0, 2, b0), (2, 2, b0 + 7), (4, 2, b0), (6, 2, b0 + 7)]
            elif style == "half":
                pat = [(0, 4, b0), (4, 4, b0 + 7)]
            elif style == "walk":
                pat = [(0, 2, b0), (2, 2, tones[1] - 24), (4, 2, b0 + 7), (6, 2, b0 + 12)]
            elif style == "gallop":
                pat = [(0, 1, b0), (1, 0.5, b0), (1.5, 0.5, b0), (2, 1, b0 + 7), (3, 0.5, b0), (3.5, 0.5, b0),
                       (4, 1, b0), (5, 0.5, b0), (5.5, 0.5, b0), (6, 1, b0 + 7), (7, 1, b0 + 12)]
            for s, d, m in pat:
                n = int(d * eighth * SR * 0.92)
                put("bass", bar_t + s * eighth, osc("tri", midi_hz(m), n) * env(n, decay=0.08, sustain=0.85))
            # bateria (na 1ª passada da faixa calma, só no fim do bloco; na 2ª, sempre)
            dr = tr["drums"]
            for k, c in enumerate(dr):
                if c != "-":
                    put("drum", bar_t + k * eighth / 2, drum(c, hash((tid, p, b, k)) % 2**31))

    out = 0.30 * mix["mel"] + 0.12 * mix["arp"] + 0.34 * mix["bass"] + 0.30 * mix["drum"]
    loop_n = int(total_steps * eighth * SR)
    if tr["loop"]:
        out[: n_total - loop_n] += out[loop_n:]  # a cauda volta para o começo: laço sem emenda
        out = out[:loop_n]
    else:
        out = out[: loop_n + int(0.6 * SR)]
        fade = int(0.3 * SR)
        out[-fade:] *= np.linspace(1, 0, fade)
    peak = np.max(np.abs(out))
    out = out / peak * 0.85
    return out


def write(tid, data):
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / f"{tid}.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((data * 32767).astype("<i2").tobytes())
        ogg = OUT / f"{tid}.ogg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "libvorbis", "-q:a", "3",
                        "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact", str(ogg)], check=True)
    return ogg


def main(ids):
    for tid in ids or TRACKS:
        tr = TRACKS[tid]
        data = render(tid, tr)
        ogg = write(tid, data)
        print(f"{tid}: {len(data) / SR:.1f} s, {ogg.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
