#!/usr/bin/env python3
"""THE DAILY MERIDIAN — entry akun13 untuk news-image-20261123.

Halaman depan koran satu halaman (putih gading, tinta marun, abu arang)
yang merangkum berita dunia Senin 23 November 2026: lead kriket India
720/9d di Wellington, 14 kartu utama berilustrasi, peta titik bernomor,
timeline UTC, kolom ALSO ON sampai 40 cerita, dan kotak DATE CHECK.

Program ini STDLIB-ONLY dan COPY-ONLY: ia menyalin entry.png yang berada
di folder yang sama ke folder keluaran ($MAKEFUN_OUTPUT_DIR atau
/output), sesudah memeriksa magic PNG, batas 1 MiB, ukuran pasti, dan
sha256 pasti dari berkas final. Dua kali jalan = byte yang sama persis.
"""

import hashlib
import os
import struct
import sys

EXPECTED_BYTES = 323952
EXPECTED_SHA256 = "8617678cfe31888225342e5a22cd136c6d2174025ad9dfb845b35265de530092"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HARD_LIMIT = 1048576  # 1 MiB, batas kompetisi


def load_entry():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as fh:
        return fh.read()


def check_entry(data):
    if not data:
        sys.exit("entry.png kosong")
    if data[:8] != PNG_SIGNATURE:
        sys.exit("entry.png bukan berkas PNG")
    if len(data) > HARD_LIMIT:
        sys.exit("entry.png melewati 1 MiB: %d byte" % len(data))
    if len(data) != EXPECTED_BYTES:
        sys.exit("ukuran entry.png %d byte, seharusnya %d"
                 % (len(data), EXPECTED_BYTES))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("sha256 entry.png tidak cocok: %s" % digest)
    return digest


def check_dimensions(data):
    """Verifikasi kedua: IHDR PNG harus tepat 1024x1024 piksel."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        sys.exit("chunk IHDR tidak ditemukan")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        sys.exit("dimensi entry.png %dx%d, seharusnya 1024x1024"
                 % (width, height))


def main():
    data = load_entry()
    digest = check_entry(data)
    check_dimensions(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)
    sys.stderr.write("entry.png tersalin: %d byte sha256=%s\n"
                     % (len(data), digest))


if __name__ == "__main__":
    main()
