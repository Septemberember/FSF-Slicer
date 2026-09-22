#!/usr/bin/env python3
"""Build source/wheel distributions and a self-contained release archive."""
from pathlib import Path
import hashlib
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.venv', '__pycache__', '.pytest_cache', 'build', '.git'}


def release_files():
    for path in sorted(ROOT.rglob('*')):
        relative = path.relative_to(ROOT)
        if not path.is_file() or any(p in EXCLUDED or p.endswith('.egg-info') or p.endswith('-output') for p in relative.parts): continue
        if path.suffix in {'.pyc', '.class'} or path.name in {'.DS_Store', 'CHECKSUMS.sha256'}: continue
        if relative.parts[0] == 'dist' and path.suffix == '.zip': continue
        yield path, relative


def main():
    subprocess.run([sys.executable, '-m', 'build', '--no-isolation'], cwd=ROOT, check=True)
    files = list(release_files())
    lines = [f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative.as_posix()}' for path, relative in files]
    checksum = ROOT/'CHECKSUMS.sha256'
    checksum.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    from fsf_tool import __version__
    target=ROOT/'dist'/f'FSF-Slicer-Tool-{__version__}.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path, relative in files:
            archive.write(path, 'Tool/'+relative.as_posix())
        archive.write(checksum, 'Tool/CHECKSUMS.sha256')
    print(target)


if __name__ == '__main__': main()
