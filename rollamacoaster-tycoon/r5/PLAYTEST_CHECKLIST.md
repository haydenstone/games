# R5.0-dev.7 playtest

- [ ] UI looks like a futuristic telemetry console, not rounded web forms.
- [ ] Ava moves around the timeline only while simulation is running.
- [ ] Stop simulation. Tick, position, happiness, wisdom, perception, and memory do not advance.
- [ ] With simulation stopped, toggle Codex off/on. The relationship may change, but Ava must not newly perceive a verse.
- [ ] Stop simulation, run `./start.sh restart`, refresh browser. Simulation must still be stopped at the saved tick/position.
- [ ] Start simulation. Ava resumes from the saved point rather than resetting.
- [ ] Restart while running. Running state remains running.
- [ ] Browser refresh does not alter simulation state.
- [ ] New iteration deliberately resets the iteration while preserving bounded Ava memory.
- [ ] `./start.sh status` reports the container cleanly.
