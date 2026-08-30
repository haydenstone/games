# R5.0-dev.3 playtest

- [ ] Open the miniature world through port 8765.
- [ ] Confirm the entity moves around the timeline ring while simulation is running.
- [ ] Stop simulation; confirm timeline/tick freeze exactly.
- [ ] Start simulation; confirm it resumes rather than resets.
- [ ] Confirm Codex is initially available and the entity actively perceives Psalm 119:24.
- [ ] Confirm the UI shows the verse reference, verse text, and perceived wisdom.
- [ ] Make Codex unavailable; confirm perception disappears and happiness trends downward.
- [ ] Restore Codex; confirm perception returns and happiness recovers naturally. This is the dev.1 regression test.
- [ ] Confirm wisdom increases only while the entity can perceive the Codex during running simulation.
- [ ] Reset after Codex loss; confirm Codex/perception and baseline state are restored coherently.
- [ ] Save, stop container, restart with the same data volume, and confirm state persists.
- [ ] Toggle Codex and simulation rapidly; look for contradictory state or crashes.
- [ ] Inspect /api/world and verify the UI is only observing authoritative state.
- [ ] Inspect /api/codex and verify the verse is a small addressable JSON unit.
- [ ] Report anything that feels hard-coded, coupled, or manager-like.
- [ ] Give the next desired behavior as intent rather than implementation instructions.
