# rollamacoasterTycoon R5.0-dev.1
First architectural proof. One container, one exposed gameplay port (8765), one authoritative miniature world.

## Run
```bash
docker build -t rct-r5-dev1 .
docker run --rm --name rct-r5 -p 8765:8765 -v "$(pwd)/data:/app/data" rct-r5-dev1
```
Open http://127.0.0.1:8765

## Test
```bash
docker run --rm rct-r5-dev1 npm test
```

This is intentionally a tiny proof, not the full R4 feature transplant. See R5_GUIDING_LIGHT.docx.
