# ti-gp-edge-ai

A general-purpose platform for running time-series edge AI demos on TI processors with
Arm cores (AM64x). Built from
TI's fan blade demo (sitara-edgai-time-series) and inspired by TI's edgeai-gst-apps:
one YAML config per demo. The board replays recorded sensor data, runs
pre-processing -> ONNX model -> post-processing, and streams results to a browser
dashboard. Python backend (numpy, onnxruntime, pyyaml); plain HTML/CSS/JS frontend
with Chart.js. The dashboard works with no internet connection (no CDN links or web
fonts; libraries are copied into the repo).

## Roadmap

- Version 0: build this modular structure and get the fan blade demo
  running in it with the same results as the original.
- Version 1: more demos, blocks, and widgets.
- Version 2: cleanup and extra features.

## Folders

- `datasets/` — recorded sensor data for each demo (e.g. `fan_blade/`).
- `models/` — trained `.onnx` models.
- `demos/` — one YAML config per demo, plus the `_template.yaml` welcome screen.
- `backend/` — Python app that runs on the board: engine, pipeline, web server,
  and processing blocks.
- `frontend/` — browser dashboard: HTML/CSS/JS, widgets, and vendored libraries
  (no CDN dependencies, so it works offline).
- `scripts/` — systemd service file and other tooling scripts.
- `docs/` — diagrams and guides.
- `.github/` — issue/PR templates and the CI workflow.

## Setup

On the board, run the one-time setup:

```
./setup.sh
```

## Run

```
./run.sh
```

Then open `http://<board-ip>:8080` in a browser.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch, commit, and PR rules.
