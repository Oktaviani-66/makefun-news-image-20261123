#!/usr/bin/env python3
"""Penyalin final THE DAILY MERIDIAN untuk akun13 (news-image-20261123).

Edisi Senin 23 November 2026 koran THE DAILY MERIDIAN — tajuk utama
India 720/9 di Wellington — tersimpan sebagai entry.png di samping
berkas ini. Tugas modul ini sempit dan disengaja membosankan: membaca
berkas itu, membuktikan ia persis berkas yang dimaksud (ukuran,
hash, tanda tangan PNG, dan geometri IHDR), lalu menyalinnya utuh
ke direktori keluaran. Tidak ada pembuatan gambar di sini, tidak
ada pustaka pihak ketiga, dan keluaran selalu identik byte demi byte.
"""

import hashlib
import os
import sys
from struct import unpack

# Sidik jari berkas final yang sudah terverifikasi di repo.
UKURAN_FINAL = 323952
SHA_FINAL = "8617678cfe31888225342e5a22cd136c6d2174025ad9dfb845b35265de530092"
BATAS_KOMPETISI = 1024 * 1024
AWALAN_PNG = b"\x89PNG\r\n\x1a\n"


def gagal(pesan):
    raise SystemExit("THE DAILY MERIDIAN: " + pesan)


def baca_sumber():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as berkas:
        return berkas.read()


def periksa(isi):
    if len(isi) < 24:
        gagal("berkas terlalu pendek untuk sebuah PNG")
    if not isi.startswith(AWALAN_PNG):
        gagal("tanda tangan PNG tidak dikenal")
    if isi[12:16] != b"IHDR":
        gagal("chunk pertama bukan IHDR")
    lebar, tinggi = unpack(">II", isi[16:24])
    if lebar != 1024 or tinggi != 1024:
        gagal("ukuran kanvas %dx%d, bukan 1024x1024" % (lebar, tinggi))
    if len(isi) > BATAS_KOMPETISI:
        gagal("berkas melampaui batas 1 MiB")
    if len(isi) != UKURAN_FINAL:
        gagal("panjang %d byte tidak sama dengan %d byte" % (len(isi), UKURAN_FINAL))
    ringkasan = hashlib.sha256(isi).hexdigest()
    if ringkasan != SHA_FINAL:
        gagal("sha256 menyimpang: " + ringkasan)
    return ringkasan


def salin(isi, ringkasan):
    # Tulis lewat berkas sementara di folder yang sama, lalu ganti nama:
    # pembaca tidak pernah melihat salinan yang baru tertulis separuh.
    tujuan_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(tujuan_dir, exist_ok=True)
    tujuan = os.path.join(tujuan_dir, "entry.png")
    sementara = tujuan + ".tmp"
    with open(sementara, "wb") as berkas:
        berkas.write(isi)
    os.replace(sementara, tujuan)
    print("tersalin %s (%d byte, sha256 %s)" % (tujuan, len(isi), ringkasan),
          file=sys.stderr)


if __name__ == "__main__":
    data = baca_sumber()
    salin(data, periksa(data))
