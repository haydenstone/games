# R5.0-dev.4 playtest checklist

- [ ] Container refuses to boot with a clear message when Codex is not mounted.
- [ ] Container boots when `$HOME/Documents/codex.json` is mounted read-only.
- [ ] `http://127.0.0.1:8765/health` returns `ok`.
- [ ] Timeline entity advances while simulation is running.
- [ ] Stop simulation freezes tick and timeline position.
- [ ] Start simulation resumes from the frozen position.
- [ ] Entity perceives Psalm 119:24 from the external Codex.
- [ ] Disable Codex: perception disappears and happiness trends down.
- [ ] Restore Codex: verse perception returns and happiness trends up.
- [ ] Wisdom rises only while Codex perception is available and simulation runs.
- [ ] Reset returns the miniature world to a coherent initial state.
- [ ] Rapidly toggle simulation and Codex access; no contradictory state or crash.
- [ ] Save, stop container, restart with same data volume; state survives.
- [ ] Remove the Codex mount and verify failure is explicit rather than mysterious.
- [ ] No second gameplay port is required.
