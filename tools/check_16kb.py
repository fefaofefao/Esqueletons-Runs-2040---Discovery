#!/usr/bin/env python3
"""Confere se as bibliotecas nativas (.so) de um APK/AAB estão alinhadas a 16 KB
(segmentos LOAD com p_align >= 16384), exigência do Google Play para Android 15+.

Uso: python3 tools/check_16kb.py build/esqueletons-debug.apk
"""
import struct
import sys
import zipfile

PAGE = 16384


def load_alignments(data: bytes):
    if data[:4] != b"\x7fELF":
        return None
    is64 = data[4] == 2
    little = data[5] == 1
    e = "<" if little else ">"
    if is64:
        phoff = struct.unpack_from(e + "Q", data, 0x20)[0]
        phentsize, phnum = struct.unpack_from(e + "HH", data, 0x36)
    else:
        phoff = struct.unpack_from(e + "I", data, 0x1C)[0]
        phentsize, phnum = struct.unpack_from(e + "HH", data, 0x2A)
    aligns = []
    for i in range(phnum):
        off = phoff + i * phentsize
        p_type = struct.unpack_from(e + "I", data, off)[0]
        if p_type != 1:  # PT_LOAD
            continue
        if is64:
            p_align = struct.unpack_from(e + "Q", data, off + 0x30)[0]
        else:
            p_align = struct.unpack_from(e + "I", data, off + 0x1C)[0]
        aligns.append(p_align)
    return aligns


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    bad = []
    checked = 0
    with zipfile.ZipFile(sys.argv[1]) as z:
        for info in z.infolist():
            if not info.filename.endswith(".so"):
                continue
            if "arm64-v8a" not in info.filename and "x86_64" not in info.filename:
                continue  # 16 KB só é exigido em ABIs de 64 bits
            aligns = load_alignments(z.read(info))
            if aligns is None:
                continue
            checked += 1
            if min(aligns) < PAGE:
                bad.append(f"{info.filename}: alinhamento {min(aligns)}")
    if checked == 0:
        print("check_16kb: nenhuma .so de 64 bits encontrada")
        return 1
    if bad:
        for b in bad:
            print("ERRO", b)
        return 1
    print(f"check_16kb: OK ({checked} bibliotecas de 64 bits alinhadas a 16 KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
