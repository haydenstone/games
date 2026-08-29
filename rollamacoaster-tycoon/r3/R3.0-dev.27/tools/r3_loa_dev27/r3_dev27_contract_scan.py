#!/usr/bin/env python3
from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'rollamacoasterTycoon_R3_rebuilt.html'); s=p.read_text(encoding='utf-8')
required=['R3.0-dev.27','R3_DEV27_ALEXANDRIA_AUTONOMY_NOTE','R3AlexandriaRuntime','r3Dev27CheckAlexandria','r3Dev27AutomaticResearch','Automatic guest research','Search live Alexandria','Alexandria live','R3GuestAlexandria']
missing=[x for x in required if x not in s]; forbidden=['LIVE ALEXANDRIA KNOWLEDGE','ALEXANDRIA LIVE']
found=[x for x in forbidden if x in s]
if missing or found:
 print('FAIL dev.27 Alexandria contract'); print('missing',missing); print('forbidden',found); raise SystemExit(1)
print('PASS dev.27 Alexandria autonomous gameplay contract')
