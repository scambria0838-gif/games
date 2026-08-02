#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path('.')
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
MAX_SIZE = 2_000_000

keyword_re = re.compile(r"master credentials|anthropic|claude|UE5PILOT_LLM_API_KEY|LLM_API|OPENAI_API_KEY|api[_ -]?key", re.I)
key_res = {
    'anthropic_key': re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    'openai_key': re.compile(r"sk-proj-[A-Za-z0-9_\-]{20,}|sk-[A-Za-z0-9_\-]{30,}"),
    'env_assignment': re.compile(r"(?i)\b(?:UE5PILOT_LLM_API_KEY|ANTHROPIC_API_KEY|OPENAI_API_KEY)\s*=\s*([^\s#'\"]+)"),
}

def skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)

def mask(value: str) -> str:
    if not value or value in {'', 'your_key_here', 'changeme', '...'}:
        return value
    if len(value) <= 10:
        return '…MASKED'
    return value[:8] + '…MASKED…' + value[-4:]

hits = []
actual_keys = []
keyword_hits = []
for path in ROOT.rglob('*'):
    if skip(path) or not path.is_file():
        continue
    try:
        if path.stat().st_size > MAX_SIZE:
            continue
        data = path.read_text(errors='replace')
    except Exception:
        continue
    found = False
    for name, rx in key_res.items():
        for m in rx.finditer(data):
            value = m.group(1) if name == 'env_assignment' else m.group(0)
            # Ignore obvious placeholders and masked artifacts
            if any(x in value.lower() for x in ['masked', 'your_', '<this-value>', '...masked', 'example', 'xxxx']):
                continue
            if value.strip() in {'', '…', 'REPLACE_ME', 'changeme'}:
                continue
            actual_keys.append((str(path), name, mask(value)))
            found = True
    if keyword_re.search(data):
        count = len(keyword_re.findall(data))
        keyword_hits.append((str(path), count, found))

print(f"ACTUAL_SECRET_PATTERN_HITS\t{len(actual_keys)}")
for p, name, masked in actual_keys[:100]:
    print(f"SECRET\t{name}\t{p}\t{masked}")
if len(actual_keys) > 100:
    print(f"SECRET_MORE\t{len(actual_keys)-100}")

print(f"KEYWORD_FILE_HITS\t{len(keyword_hits)}")
for p, count, has_secret in sorted(keyword_hits)[:200]:
    print(f"KEYWORD\t{count}\tsecret_pattern={has_secret}\t{p}")
