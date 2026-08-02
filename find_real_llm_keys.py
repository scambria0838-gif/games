#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('.')
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
MAX_SIZE = 5_000_000

# Anthropic commonly looks like sk-ant-api03-... ; OpenAI like sk-proj-... or sk-...
patterns = {
    'anthropic': re.compile(r"sk-ant-[A-Za-z0-9_.\-]{25,}"),
    'openai': re.compile(r"sk-proj-[A-Za-z0-9_\-]{30,}|sk-[A-Za-z0-9_\-]{45,}"),
}
ignore_fragments = ['MASKED', '…', '<', '>', 'your_', 'example', 'REPLACE', 'xxxx', '\\u2026']

def skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)

def mask(s: str) -> str:
    return s[:14] + '…MASKED…' + s[-6:]

hits = []
for path in ROOT.rglob('*'):
    if skip(path) or not path.is_file():
        continue
    try:
        if path.stat().st_size > MAX_SIZE:
            continue
        text = path.read_text(errors='replace')
    except Exception:
        continue
    for line_no, line in enumerate(text.splitlines(), 1):
        for provider, rx in patterns.items():
            for m in rx.finditer(line):
                val = m.group(0).strip().strip('"\',`:,;')
                if any(x.lower() in val.lower() for x in ignore_fragments):
                    continue
                # Exclude obvious regex/code patterns containing brackets or braces
                if any(ch in val for ch in '[]{}()+*?'):
                    continue
                hits.append((provider, str(path), line_no, mask(val), len(val)))

print(f"REAL_LOOKING_KEY_HITS\t{len(hits)}")
for provider, path, line_no, masked, length in hits[:100]:
    print(f"KEY\t{provider}\t{path}:{line_no}\tlen={length}\t{masked}")
if len(hits) > 100:
    print(f"MORE\t{len(hits)-100}")
