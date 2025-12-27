#!/usr/bin/env python3
"""
Migration Script - Move old flat structure to Pretty Good team folder

Moves from:
  data/
    players.json
    seasons/
    games/
    records.json
    games_index.json
    seasons_meta.json

To:
  data/pretty-good/
    players.json
    seasons/
    games/
    records.json
    games_index.json
    seasons_meta.json
"""

import shutil
from pathlib import Path

def migrate():
    base = Path('data')
    target = base / 'pretty-good'
    
    # Check if old structure exists
    old_files = ['players.json', 'records.json', 'games_index.json', 'seasons_meta.json']
    old_dirs = ['seasons', 'games']
    
    has_old = any((base / f).exists() for f in old_files) or any((base / d).exists() for d in old_dirs)
    
    if not has_old:
        print("No old structure found. Nothing to migrate.")
        return
    
    # Create target directory
    target.mkdir(parents=True, exist_ok=True)
    
    # Move files
    for f in old_files:
        src = base / f
        if src.exists():
            dst = target / f
            if not dst.exists():
                shutil.copy(src, dst)
                print(f"✓ Copied {f}")
            else:
                print(f"⚠ Skipped {f} (already exists in target)")
    
    # Move directories
    for d in old_dirs:
        src = base / d
        if src.exists() and src.is_dir():
            dst = target / d
            if not dst.exists():
                shutil.copytree(src, dst)
                print(f"✓ Copied {d}/")
            else:
                print(f"⚠ Skipped {d}/ (already exists in target)")
    
    print("\n" + "="*50)
    print("Migration complete!")
    print("="*50)
    print(f"\nData copied to: {target}")
    print("\nYou can delete the old files after verifying:")
    for f in old_files:
        if (base / f).exists():
            print(f"  rm data/{f}")
    for d in old_dirs:
        if (base / d).exists():
            print(f"  rm -rf data/{d}")


if __name__ == '__main__':
    migrate()
