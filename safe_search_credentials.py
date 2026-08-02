#!/usr/bin/env python3
import re
from pathlib import Path

patterns = re.compile(r"master credentials|anthropic|claude|api[_ -]?key|UE5PILOT_LLM|LLM_PROVIDER|LLM_API", re.I)
secret_patterns = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"(?i)((?:[A-Z0-9_]*API[_-]?KEY|TOKEN|SECRET)[\"' ]*[:=][\"' ]*)[^\"'\s,]+"),
]

def mask(line: str) -> str:
    for pat in secret_patterns[:2]:
        line = pat.sub(lambda m: m.group(0)[:12] + "…MASKED", line)
    line = secret_patterns[2].sub(lambda m: m.group(1) + "…MASKED", line)
    return line

target = Path("summarized_conversations/original_conversation_1780057442_526.txt")
if not target.exists():
    print(f"MISSING\t{target}")
    raise SystemExit(1)

print(f"FOUND_TRANSCRIPT\t{target}")
matches = []
with target.open("r", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if patterns.search(line):
            matches.append((i, mask(line.rstrip())))

print(f"MATCH_COUNT\t{len(matches)}")
for i, line in matches[-120:]:
    print(f"{target}:{i}: {line}")
