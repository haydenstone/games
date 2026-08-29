#!/usr/bin/env python3
from pathlib import Path
import sys

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('rollamacoasterTycoon_R3_rebuilt.html')
text = p.read_text(encoding='utf-8')
required = [
    'R3.0-dev.26',
    'R3_DEV26_LOA_KNOWLEDGE_NOTE',
    'window.R3GuestAlexandria',
    'r3Dev26AdoptAlexandria',
    'r3Dev26ResearchGuest',
    'alexandriaKnowledge',
    'alexandriaBias',
    'alexandriaResearchCount',
    'source:\'library-of-alexandria\'',
    "const r3Dev26GuestChatBase=ollama.guestChat.bind(ollama)",
    'const r3Dev26GuestTargetScoreBase=guestTargetScore',
    'const r3Dev26LoadParkBase=loadPark',
    'const r3Dev26DirectQueries=new Set()',
    '<b>📚 Alexandria knowledge</b>',
    'Offline · ${err.message}',
]
missing = [x for x in required if x not in text]
forbidden_ui = [
    'LIVE ALEXANDRIA KNOWLEDGE',
    'LAST KNOWLEDGE-INFLUENCED DECISION',
    'OFFLINE / ERROR',
]
found = [x for x in forbidden_ui if x in text]
if missing or found:
    if missing:
        print('Missing dev.26 contract markers:')
        for x in missing: print(' -', x)
    if found:
        print('Found forbidden all-caps dev.26 UI strings:')
        for x in found: print(' -', x)
    raise SystemExit(1)
print('PASS dev.26 native LoA guest knowledge contract')
print('PASS dev.26 new Alexandria UI uses normal case')
