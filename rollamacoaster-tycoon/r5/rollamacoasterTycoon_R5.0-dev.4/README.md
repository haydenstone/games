# Rollamacoaster Tycoon R5.0-dev.4

R5 Phase 1 miniature-world proof. The Bible Codex is now an external dependency and is intentionally NOT packaged in this release.

Expected host file:

    $HOME/Documents/codex.json

The container sees it read-only at `/codex/codex.json`. Override the host path in the docker command if your file is named differently.

Build:

    docker build -t rct-r5-dev4 .

Test the actual image with the external Codex mounted:

    docker run --rm \
      -v "$HOME/Documents/codex.json:/codex/codex.json:ro" \
      rct-r5-dev4 npm test

Run gameplay:

    mkdir -p data
    docker run --rm --name rct-r5 \
      -p 8765:8765 \
      -v "$(pwd)/data:/app/data" \
      -v "$HOME/Documents/codex.json:/codex/codex.json:ro" \
      rct-r5-dev4

Open http://127.0.0.1:8765

Only gameplay port 8765 is exposed.
