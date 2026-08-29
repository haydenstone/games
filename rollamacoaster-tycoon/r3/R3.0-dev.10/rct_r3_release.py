#!/usr/bin/env python3
"""Build, validate, fingerprint, and stage an R3 development release."""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'build_rct_r3.py'
ART = ROOT / 'rollamacoasterTycoon_R3_rebuilt.html'


def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {'cmd':' '.join(map(str,cmd)), 'ok':p.returncode==0, 'stdout':p.stdout[-4000:], 'stderr':p.stderr[-4000:]}


def resolve_codex(explicit=None):
    if explicit:
        p = Path(explicit).expanduser()
        if not p.is_absolute():
            p = ROOT / p
        p = p.resolve()
        return p if p.is_file() else None
    for p in [ROOT/'codex.json', ROOT/'codex(1).json', *sorted(ROOT.glob('codex*.json'))]:
        if p.is_file():
            return p.resolve()
    return None


def main():
    ap = argparse.ArgumentParser(description='Create an immutable RollamacoasterTycoon R3 development release')
    ap.add_argument('--codex', help='Codex JSON path. Defaults to a codex*.json beside the release script.')
    args = ap.parse_args()

    codex = resolve_codex(args.codex)
    if not codex:
        print('Missing Codex JSON. Put codex.json (or codex(1).json) in this project folder, or pass --codex /path/to/file.json', file=sys.stderr)
        return 1

    tests=[]
    tests.append(run([sys.executable, str(BUILD), '--codex', str(codex)]))
    if not tests[-1]['ok']:
        print(tests[-1]['stderr']); return 1

    # Rebuild once to prove the generator is deterministic for the same source inputs.
    deterministic_art = ROOT / '.r3-determinism.html'
    det_run = run([sys.executable, str(BUILD), '--codex', str(codex), '--output', str(deterministic_art)])
    det_ok = det_run['ok'] and deterministic_art.exists() and deterministic_art.read_bytes() == ART.read_bytes()
    tests.append({'cmd':'deterministic rebuild','ok':det_ok,'stdout':det_run.get('stdout',''),'stderr':det_run.get('stderr','') if not det_ok else ''})
    if deterministic_art.exists(): deterministic_art.unlink()

    text=ART.read_text(encoding='utf-8')
    m=re.search(r"id:'([^']+)',schema:1,builtBy:'build_rct_r3.py'",text)
    release=m.group(1) if m else 'unknown-release'
    scripts=re.findall(r'<script(?:[^>]*)>(.*?)</script>',text,re.S)
    js=ROOT/'.r3-release-check.js'; js.write_text('\n'.join(scripts),encoding='utf-8')
    node=shutil.which('node')
    if node: tests.append(run([node,'--check',str(js)]))
    required=['R3 DEVELOPMENT TEST LOOP','/api/dev/core-dump','rollamacoaster-r3','/api/tags','/api/chat','REVISION 3','R3.0-dev.10','updateKeyboardCamera(dt)','cam.position.distanceTo(ctl.target)','frameStep("camera"','frame-loop fault containment','R3_GRID_FENCE_RELEASE_NOTE','GRID_STEP=2','makeConstructionGrid()','makeParkBoundaryFence()','pathCellInside(x,z)','exact 2m grid cell','R3_SIGN_PATH_RELEASE_NOTE','R3_ENTRANCE_PROPERTY_RELEASE_NOTE','makeWildernessApproachPath()','PROPERTY_PARCELS','parkSignFont','boundaryPartFromHits(hits)','data-buy-parcel',"rightClick:'fence=property, entrance=park-manager'",'const w=k==="queue"?1.18:GRID_STEP,depth=GRID_STEP','R3_CINEMATIC_UI_RELEASE_NOTE','R3_GATEWORKS_RELEASE_NOTE','R3_TRANSACTION_FEEDBACK_RELEASE_NOTE','R3_COMMAND_DECK_RELEASE_NOTE','R3_DIAGNOSTIC_CAPTURE_RELEASE_NOTE','activeParkBounds()','activeParkGate()','ensureGateConnectorPaths()','systemTray','positionSystemsTray()','toggleSystemsTray','pauseMenu','openPauseMenu','renderPauseMenu','menuContinue','menuSave','menuLoad','menuCheats','menuExit','data-menu-delete','preserveDrawingBuffer:true','forced-render-dataurl','networkPanel','pulsePanel','simRateSlider','guestCapEditor','entranceLive','GATE_STYLES','MASONRY_STYLES','insufficientFunds','showTransactionFloat','SYSTEM_BRANDS','FRONTIERNET','GATEWORKS','SURVEYOR']
    missing=[x for x in required if x not in text]
    tests.append({'cmd':'required markers','ok':not missing,'stdout':'','stderr':('missing: '+', '.join(missing)) if missing else ''})
    forbidden=['cam.distanceTo(ctl.target)','new THREE.GridHelper(160,80',"labelSprite('FOREST FRONTIERS'",'const w=k==="queue"?1.18:1.82','#systemTray{position:fixed;z-index:99',"if(e.key==='Escape'||e.key==='Backspace')"]
    found_forbidden=[x for x in forbidden if x in text]
    tests.append({'cmd':'camera/grid regression guard','ok':not found_forbidden,'stdout':'','stderr':('forbidden: '+', '.join(found_forbidden)) if found_forbidden else ''})
    if js.exists(): js.unlink()

    sha=hashlib.sha256(ART.read_bytes()).hexdigest()
    codex_sha=hashlib.sha256(codex.read_bytes()).hexdigest()
    stage=ROOT/'releases'/release
    stage.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ART,stage/ART.name)
    staged_codex = stage / codex.name
    shutil.copy2(codex, staged_codex)
    # Stage a genuinely self-contained canonical toolchain. Portable transition names
    # are rewritten so a release folder can rebuild and relaunch itself unchanged.
    shutil.copy2(BUILD, stage/'build_rct_r3.py')
    release_text = Path(__file__).resolve().read_text(encoding='utf-8')
    release_text = release_text.replace("BUILD = ROOT / 'build_rct_r3.py'", "BUILD = ROOT / 'build_rct_r3.py'")
    release_text = release_text.replace("launcher = ROOT/'run_rct_r3_dev.sh'", "launcher = ROOT/'run_rct_r3_dev.sh'")
    staged_release = stage/'rct_r3_release.py'
    staged_release.write_text(release_text, encoding='utf-8'); staged_release.chmod(0o755)
    launcher = ROOT/'run_rct_r3_dev.sh'
    if launcher.exists():
        launcher_text = launcher.read_text(encoding='utf-8').replace('python3 rct_r3_release_PORTABLE_dev4.py', 'python3 rct_r3_release.py')
        staged_launcher = stage/'run_rct_r3_dev.sh'
        staged_launcher.write_text(launcher_text, encoding='utf-8'); staged_launcher.chmod(0o755)
    for f in [ROOT/'rct_r3_dev_server.py',ROOT/'rollamacoasterTycoon_R3_REBUILD_NOTES.md',ROOT/'R3_PLAYTEST_DEVELOPMENT_LOOP.md']:
        if f.exists(): shutil.copy2(f,stage/f.name)

    manifest={
        'release':release,
        'createdAt':datetime.now(timezone.utc).isoformat(),
        'artifact':ART.name,
        'sha256':sha,
        'bytes':ART.stat().st_size,
        'codex':{'file':codex.name,'sha256':codex_sha,'bytes':codex.stat().st_size},
        'tests':tests,
        'passed':all(t['ok'] for t in tests),
        'workflowNext':'TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE'
    }
    (stage/'release-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    (ROOT/'rollamacoasterTycoon_R3_RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'release':release,'passed':manifest['passed'],'sha256':sha,'codex':str(codex),'stage':str(stage)},indent=2))
    return 0 if manifest['passed'] else 2

if __name__=='__main__': raise SystemExit(main())
