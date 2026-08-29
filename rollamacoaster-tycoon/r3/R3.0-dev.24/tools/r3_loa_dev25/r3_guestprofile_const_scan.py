#!/usr/bin/env python3
"""Static guard for the dev.24 guestProfile 'Assignment to constant variable' fault.

This does NOT auto-edit gameplay logic. It reports likely const declarations that are
reassigned inside/near guestProfile so the P0 root fix remains explicit and reviewable.
"""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: r3_guestprofile_const_scan.py rollamacoasterTycoon_R3_rebuilt.html')

p = Path(sys.argv[1])
s = p.read_text(errors='replace')
lines = s.splitlines()

# Artifact is heavily minified in places. Search a generous character window.
pos = s.find('guestProfile')
if pos < 0:
    print('WARN: guestProfile not found.')
    raise SystemExit(2)

lo = max(0, pos - 3000)
hi = min(len(s), pos + 18000)
window = s[lo:hi]

consts = set(re.findall(r'\bconst\s+([A-Za-z_$][\w$]*)\s*=', window))
suspects = []
for name in sorted(consts):
    # declaration plus any later assignment not immediately part of const declaration
    assignments = list(re.finditer(rf'(?<!const\s)\b{re.escape(name)}\s*=(?!=)', window))
    if assignments:
        suspects.append((name, len(assignments)))

print('R3 guestProfile const-reassignment scan')
print(f'file: {p}')
print(f'window chars: {lo}..{hi}')
if suspects:
    print('SUSPECTS:')
    for name, count in suspects:
        print(f'  {name}: {count} apparent reassignment(s)')
    print('ACTION: inspect these in source/generator before dev.25 release. Do not blind-replace const with let.')
    raise SystemExit(1)
else:
    print('No obvious const reassignment found in the local guestProfile window.')
    print('Runtime playtest is still required because the original fault was dynamic.')
