#!/usr/bin/env python3
"""Build, validate, fingerprint, and stage an R3 development release."""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build_rct_r3.py'
ART=ROOT/'rollamacoasterTycoon_R3_rebuilt.html'


def run(cmd):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    return {'cmd':' '.join(map(str,cmd)),'ok':p.returncode==0,'stdout':p.stdout[-4000:],'stderr':p.stderr[-4000:]}


def main():
    tests=[]
    tests.append(run([sys.executable,str(BUILD)]))
    if not tests[-1]['ok']:
        print(tests[-1]['stderr']); return 1
    text=ART.read_text(encoding='utf-8')
    m=re.search(r"id:'([^']+)',schema:1,builtBy:'build_rct_r3.py'",text)
    release=m.group(1) if m else 'unknown-release'
    scripts=re.findall(r'<script(?:[^>]*)>(.*?)</script>',text,re.S)
    js=ROOT/'.r3-release-check.js'; js.write_text('\n'.join(scripts),encoding='utf-8')
    node=shutil.which('node')
    if node: tests.append(run([node,'--check',str(js)]))
    required=['R3 DEVELOPMENT TEST LOOP','/api/dev/core-dump','rollamacoaster-r3','/api/tags','/api/chat','REVISION 3']
    missing=[x for x in required if x not in text]
    tests.append({'cmd':'required markers','ok':not missing,'stdout':'','stderr':('missing: '+', '.join(missing)) if missing else ''})
    if js.exists(): js.unlink()
    sha=hashlib.sha256(ART.read_bytes()).hexdigest()
    stage=ROOT/'releases'/release
    stage.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ART,stage/ART.name)
    for f in [BUILD,ROOT/'rct_r3_dev_server.py',ROOT/'rct_r3_release.py',ROOT/'rollamacoasterTycoon_R3_REBUILD_NOTES.md',ROOT/'R3_PLAYTEST_DEVELOPMENT_LOOP.md',ROOT/'run_rct_r3_dev.sh']:
        if f.exists(): shutil.copy2(f,stage/f.name)
    manifest={'release':release,'createdAt':datetime.now(timezone.utc).isoformat(),'artifact':ART.name,'sha256':sha,'bytes':ART.stat().st_size,'tests':tests,'passed':all(t['ok'] for t in tests),'workflowNext':'TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE'}
    (stage/'release-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    (ROOT/'rollamacoasterTycoon_R3_RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'release':release,'passed':manifest['passed'],'sha256':sha,'stage':str(stage)},indent=2))
    return 0 if manifest['passed'] else 2

if __name__=='__main__': raise SystemExit(main())
