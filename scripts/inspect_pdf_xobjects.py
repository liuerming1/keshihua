"""Diagnostic extraction of page XObjects to inspect composite backgrounds."""

import argparse
from pathlib import Path

from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--page", type=int, action="append", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    reader = PdfReader(str(args.pdf))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for page_number in args.page:
        for index, image in enumerate(reader.pages[page_number - 1].images):
            suffix = Path(image.name).suffix.lower()
            path = args.out_dir / f"p{page_number:04d}_im{index:02d}{suffix}"
            path.write_bytes(image.data)
            print(f"{page_number} {index} {path} {len(image.data)}")


if __name__ == "__main__":
    main()
