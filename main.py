#!/usr/bin/env python3
"""Entry program — THE MONDAY HERALD (news-image-20261123, akun13 G4).

One page, one day: Monday 23 November 2026. The Herald leads with
Alcaraz's first ATP Finals title and carries forty dated stories,
each pinned, sourced and certainty-tagged on the sheet.

The program is stdlib-only and copy-only: it verifies the bundled
entry.png against a pinned size and digest, then writes it to the
output directory unchanged.
"""

import hashlib
import os
import sys

PINNED_BYTES = 119913
PINNED_SHA256 = "3efbdf9266381dfd03797367973342064aea1952ff41c008e9b93c0e55c95bda"
MAGIC = b"\x89PNG\r\n\x1a\n"
CEILING = 1048576


def load_page():
    # The verified page sits beside this program in the repository.
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "entry.png")
    with open(path, "rb") as handle:
        return handle.read()


def verify_page(blob):
    if len(blob) == 0:
        sys.exit("entry.png kosong")
    if blob[:8] != MAGIC:
        sys.exit("entry.png bukan PNG")
    if len(blob) > CEILING:
        sys.exit("entry.png melewati 1 MiB: %d" % len(blob))
    if len(blob) != PINNED_BYTES:
        sys.exit("ukuran entry.png tidak cocok: %d" % len(blob))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != PINNED_SHA256:
        sys.exit("sha256 entry.png tidak cocok: %s" % digest)
    return digest


def main():
    blob = load_page()
    digest = verify_page(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as handle:
        handle.write(blob)
    sys.stderr.write("entry.png terkirim: %d byte, sha256=%s\n" % (len(blob), digest))


if __name__ == "__main__":
    main()
