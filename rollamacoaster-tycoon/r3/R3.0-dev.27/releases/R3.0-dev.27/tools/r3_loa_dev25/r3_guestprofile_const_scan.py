#!/usr/bin/env python3
"""Static guard for guestProfile const reassignment.

Scopes the scan to the actual guestProfile function body instead of a broad minified
character window, preventing unrelated later functions from generating false positives.
"""
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: r3_guestprofile_const_scan.py rollamacoasterTycoon_R3_rebuilt.html')
p=Path(sys.argv[1]); s=p.read_text(errors='replace')
start=s.find('function guestProfile(')
if start < 0:
    print('WARN: guestProfile not found.'); raise SystemExit(2)
brace=s.find('{',start)
if brace < 0: raise SystemExit('guestProfile opening brace not found')
# Balanced-brace scan with basic JS string/template awareness. Braces inside strings are ignored.
depth=0; quote=None; esc=False; end=None
i=brace
while i < len(s):
    ch=s[i]
    if quote:
        if esc: esc=False
        elif ch=='\\': esc=True
        elif ch==quote: quote=None
    else:
        if ch in "'\"`": quote=ch
        elif ch=='{': depth += 1
        elif ch=='}':
            depth -= 1
            if depth == 0:
                end=i+1; break
    i += 1
if end is None: raise SystemExit('guestProfile closing brace not found')
window=s[start:end]
# Collect every declarator in const statements, not only the first name.
const_names=set()
for stmt in re.findall(r'\bconst\s+([^;]+);',window):
    for name in re.findall(r'(?:^|,)\s*([A-Za-z_$][\w$]*)\s*=',stmt): const_names.add(name)
suspects=[]
for name in sorted(const_names):
    # strip declaration occurrences before looking for plain assignments
    scrub=re.sub(rf'([,\s]){re.escape(name)}\s*=([^,;]+)',r'\1',window,count=1)
    hits=list(re.finditer(rf'(?<![\w$]){re.escape(name)}\s*=(?!=)',scrub))
    if hits: suspects.append((name,len(hits)))
print('R3 guestProfile const-reassignment scan')
print(f'file: {p}')
print(f'function chars: {start}..{end}')
if suspects:
    print('SUSPECTS:')
    for name,count in suspects: print(f'  {name}: {count} apparent reassignment(s)')
    raise SystemExit(1)
print('PASS: no const binding in guestProfile is reassigned.')
