"""Rebuild the import-ready textbook bundle from reviewed local inputs."""

import subprocess
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "shuju" / "cleaned" / "history_book_01"
PDF = ROOT / "shuju" / "普通高中教科书·历史必修_中外历史纲要（上）.pdf"
CROPS = BOOK / "finalization" / "image_crops"
EXPORTS = BOOK / "finalization" / "image_exports"
ASSETS = ROOT / "public" / "textbook-assets"
FINAL = ROOT / "public" / "data" / "history_book_01.json"
FACT = BOOK / "all_fact_cleaned.json"
MAP_LABELS = BOOK / "finalization" / "map_labels.json"


def run(script, *args):
    command = [sys.executable, "-X", "utf8", str(ROOT / "scripts" / script), *map(str, args)]
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    # Once reviewed recleaning is published, rebuild from those reviewed inputs.
    # Replaying legacy inputs here would silently discard newer source corrections.
    if FINAL.exists() and json.loads(FINAL.read_text(encoding='utf8')).get('reclean_report'):
        run('finalize_reclean_textbook.py','--publish')
        return
    manifests = sorted(CROPS.glob("b???.json"))
    if len(manifests) != 24:
        raise ValueError(f"Need 24 reviewed manifests; found {len(manifests)}")
    for manifest in manifests:
        run("export_textbook_assets.py", "--pdf", PDF, "--data", FACT,
            "--manifest", manifest, "--out-dir", ASSETS,
            "--report", EXPORTS / manifest.name,
            "--xobject-overrides", BOOK / "finalization" / "xobject_overrides.json")
    run("digitize_map_labels.py", "--pdf", PDF, "--data", FACT,
        "--reports-dir", EXPORTS, "--out", MAP_LABELS)
    run("build_textbook_package.py", "--data", FACT, "--reports-dir", EXPORTS,
        "--crops-dir", CROPS, "--map-labels", MAP_LABELS,
        "--map-points", BOOK / "finalization" / "verified_map_points.json", "--out", FINAL)
    run("validate_pdf_cleaning.py", FINAL)
    run("validate_textbook_package.py", "--package", FINAL, "--public-dir", ROOT / "public")
    print(f"Ready: {FINAL}")


if __name__ == "__main__":
    main()
