"""Build the static site into dist/ for Cloudflare Pages."""

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT, check=True)

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

for page in ROOT.glob("*.html"):
    shutil.copy2(page, DIST / page.name)

shutil.copytree(ROOT / "assets", DIST / "assets")
shutil.copy2(ROOT / "_headers", DIST / "_headers")

print(f"Prepared Cloudflare Pages output in {DIST}.")
