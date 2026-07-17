#!/usr/bin/env python3
"""Scan a folder for MP3s with filename-encoded timeframes and truncate overlong files.

Usage:
    python fix_recordings.py <folder> [--dry-run] [--yes] [--tolerance-seconds N]

Uses `ffprobe` to measure actual duration and `ffmpeg` to truncate with `-c copy`.
When truncating, the script will leave the configured tolerance (seconds) as extra audio.
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

TIME_PATTERN = re.compile(r"\[(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\].*\[(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\]")
TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def parse_filename_for_times(fname: str) -> Optional[Tuple[datetime, datetime]]:
    m = TIME_PATTERN.search(fname)
    if not m:
        return None
    try:
        start = datetime.strptime(m.group(1), TIME_FORMAT)
        end = datetime.strptime(m.group(2), TIME_FORMAT)
        return start, end
    except ValueError:
        return None


def ffprobe_duration(path: Path) -> Optional[float]:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            print(f"ffprobe failed for {path}: {proc.stderr.strip()}")
            return None
        out = proc.stdout.strip()
        if not out:
            return None
        return float(out)
    except FileNotFoundError:
        print("ffprobe not found on PATH. Please install ffmpeg.")
        return None
    except Exception as e:
        print(f"ffprobe error for {path}: {e}")
        return None


def format_seconds(s: float) -> str:
    td = timedelta(seconds=int(round(s)))
    total_seconds = int(td.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def run_ffmpeg_truncate(src: Path, dst: Path, duration_seconds: float) -> bool:
    # Use -t with seconds; -c copy for fast truncation
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-t",
        str(int(round(duration_seconds))),
        "-c",
        "copy",
        str(dst),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"ffmpeg failed for {src}: {proc.stderr.strip()}")
            return False
        return True
    except FileNotFoundError:
        print("ffmpeg not found on PATH. Please install ffmpeg.")
        return False


def scan_folder(folder: Path, tolerance: float) -> List[Tuple[Path, float, float, float]]:
    """Return list of tuples: (path, expected_seconds, actual_seconds, overage_seconds)"""
    flagged = []
    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() != ".mp3":
            continue
        parsed = parse_filename_for_times(p.name)
        if not parsed:
            print(f"Skipping (no timestamps): {p.name}")
            continue
        start, end = parsed
        expected = (end - start).total_seconds()
        if expected <= 0:
            print(f"Skipping (non-positive expected duration): {p.name}")
            continue
        actual = ffprobe_duration(p)
        if actual is None:
            print(f"Could not determine duration for {p.name}; skipping")
            continue
        over = actual - expected
        if over > tolerance:
            flagged.append((p, expected, actual, over))
    return flagged


def preserve_and_replace(original: Path, tmp: Path) -> bool:
    st = original.stat()
    try:
        os.replace(str(tmp), str(original))
    except Exception as e:
        print(f"Failed to replace {original} with {tmp}: {e}")
        return False
    try:
        os.chmod(original, st.st_mode)
    except Exception:
        pass
    try:
        os.chown(original, st.st_uid, st.st_gid)
    except PermissionError:
        print(f"Warning: unable to chown {original}; run as owner/root to preserve ownership")
    except Exception:
        pass
    try:
        os.utime(original, ns=(st.st_atime_ns, st.st_mtime_ns))
    except Exception:
        pass
    return True


def confirm(prompt: str) -> bool:
    try:
        r = input(prompt).strip().lower()
    except EOFError:
        return False
    return r in ("y", "yes")


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="Find and truncate MP3s longer than their filename timeframe")
    parser.add_argument("folder", help="Folder to scan (non-recursive)")
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not modify files")
    parser.add_argument("--yes", action="store_true", help="Assume yes for prompts")
    parser.add_argument("--tolerance-seconds", type=float, default=60.0, help="Min overage to consider (seconds); default 60. Left in file when truncating.")
    args = parser.parse_args(argv)

    folder = Path(args.folder)
    if not folder.exists() or not folder.is_dir():
        print(f"Folder not found or not a directory: {folder}")
        return 2

    flagged = scan_folder(folder, args.tolerance_seconds)

    if not flagged:
        print("No overlong files found.")
        return 0

    print("Overlong files:")
    for p, expected, actual, over in flagged:
        print(f"- {p.name}: expected={format_seconds(expected)} actual={format_seconds(actual)} over={format_seconds(over)}")

    if args.dry_run:
        print("\nDry run; no files modified.")
        return 0

    if not args.yes:
        if not confirm(f"\nTruncate these {len(flagged)} file(s)? [y/N] "):
            print("Aborted by user.")
            return 0

    truncated = 0
    for p, expected, actual, over in flagged:
        # Use a temp name that preserves the original suffix (ends with .mp3)
        # so ffmpeg can infer the output format (avoid unknown .tmp extension).
        tmp = p.with_name(f".{p.stem}.tmp{p.suffix}")
        # Leave the tolerance seconds as extra in the truncated file
        target = expected + args.tolerance_seconds
        print(f"Truncating {p.name} to {format_seconds(target)} (leaving {format_seconds(args.tolerance_seconds)} tolerance)...")
        ok = run_ffmpeg_truncate(p, tmp, target)
        if not ok:
            print(f"Failed to truncate {p.name}; skipping")
            try:
                if tmp.exists():
                    tmp.unlink()
            except Exception:
                pass
            continue
        ok2 = preserve_and_replace(p, tmp)
        if ok2:
            print(f"Truncated: {p.name} ({format_seconds(actual)} -> {format_seconds(expected)})")
            truncated += 1

    print(f"Done. Truncated {truncated} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
