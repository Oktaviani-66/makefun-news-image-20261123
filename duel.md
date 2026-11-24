# DUEL VARIAN — NI23 G3 · akun13 · THE DAILY MERIDIAN

## Tiga varian yang dibangun (satu compose.py, argumen A/B/C)

- **A — Putih Gading Klasik.** Palet akun: latar putih gading, tinta marun,
  aksen abu arang; masthead marun di atas gading, strip angka marun di atas
  gading, kartu panel terang berbingkai halus.
- **B — Meja Arang.** Latar arang gelap, panel lebih gelap, teks gading,
  aksen marun terang (terakota). Susunan sama, suasana "edisi malam".
- **C — Pita Marun.** Masthead gading di atas pita marun penuh + strip angka
  gading di atas pita marun; sisanya palet terang seperti A.

## Penilaian

- **Kontras:** A tertinggi (tinta gelap di atas gading di semua zona).
  B paling lemah di kicker dan deck kartu pada ukuran kecil; C kuat di
  masthead tetapi strip angka gading-di-marun sedikit di bawah A.
- **Keterbacaan 300px:** A dan C lulus; pada A masthead, tanggal, 6 angka,
  judul lead dan 13 judul kartu mini semua terbaca. B terbaca tetapi
  lebih redup, terutama ALSO ON dan legenda peta.
- **Kepadatan data:** sama di ketiga varian (40 cerita, 14 kartu, 6 angka,
  6 slot timeline, 8 buangan DATE CHECK) — pembeda murni palet/presentasi.

## Pemenang: A — Putih Gading Klasik

Alasan: kontras maksimum untuk juri yang membaca di ±300px, identitas
koran paling jelas (masthead marun Playfair Black 64px di atas gading),
dan sesuai palet resmi akun (putih gading, tinta marun, aksen abu arang).

## Uji 300px (pemenang A)

entry.png diperkecil ke 300×300 dan diperiksa: masthead "THE DAILY
MERIDIAN" terbaca, tanggal "Monday 23 November 2026" terbaca, keenam
angka strip terbaca, judul lead "India Post Record 720/9 at Wellington"
terbaca, dan judul ke-14 kartu utama terbaca. **LULUS.**

## Kenapa lebih kuat dari entry G2 ("Piringan Hitam", lead G2 #14 Inggris–UE)

G2 memakai konsep piringan hitam (dekoratif, bukan halaman koran lurus)
dengan lead kesepakatan Inggris–UE. G3 adalah halaman depan koran lurus
yang sesungguhnya: masthead raksasa + tanggal besar, lead diganti ke
rekor kriket India 720/9d di Wellington (pool #25, angka paling mencolok
hari itu) sebagai kartu #1 terbesar dengan ilustrasi lapangan + papan
skor, teks besar yang tetap terbaca di 300px, 40 cerita dari 8 region,
peta titik bernomor pin, dan kotak DATE CHECK bernama + bertanggal.

## Trio lead

1. **#25 India 720/9d di Wellington** (lead akun, kartu #1)
2. **#43 Demokrat menangi DPR AS 258–173** (kartu #2)
3. **#7 COP31 berakhir tanpa kesepakatan** (kartu #3)

## Verifikasi teknis

- entry.png: 1024×1024 (IHDR terbaca struct), 323.952 byte,
  sha256 8617678cfe31888225342e5a22cd136c6d2174025ad9dfb845b35265de530092
- Margin checker: **13/13 LOLOS** (14 kartu, ilustrasi 100%, tag sumber
  100%, 6 angka semua mengikat, pin peta 14/14, DATE CHECK 8 bernama,
  timeline 6 slot, 40 cerita, brief segar 58%)
- main.py: stdlib-only copy-only, dua kali jalan byte-identik.
