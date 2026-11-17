# Blocks and config rules

How a demo YAML turns into a running pipeline. The message formats sent to the
browser are in [frame_format.md](frame_format.md).

## The pipeline

Every window goes through the `pre` blocks in order, then the `model` block,
then the `post` blocks in order. The model is a block too (its `block` name is
`model`). Each block is a subclass of `Block` in `backend/blocks/base.py`, is
built once from its YAML settings, and exposes `run(x) -> result`.

`pipeline.py` times each block. The timings are sent as `timing_us`, keyed by
block name, plus `total`.

## How blocks pass data

One rule:

1. By default a block receives the **previous block's result**.
2. A block can add `output: <name>`. Its result is also saved in a shared dict
   under that name. The chain still continues with that result as "previous".
3. A block can read a saved result by its **bare name** (no `pre.` or `post.`
   prefix), in one of two ways:
   - `input: <name>` — `run()` receives that one value instead of the previous
     result.
   - `compare: [a, b]` — `run()` receives a list `[value_a, value_b]`.

`Block.resolve_input(previous, values)` implements this, so `pipeline.py` just
calls it before each `run()`.

A name must be saved by an earlier block than the one that reads it.

### What goes to the dashboard

All saved results live in the shared dict while a window is processed, but only
the ones saved by **`post` blocks** are sent, as `frame.outputs.<name>`.
Intermediate results (`features`, `recon` in the fan demo) stay in the backend.

### Fan blade example

| Block | Receives | Saves as |
|---|---|---|
| `spectral_features` | the window (1024 x 3) | `features` (3, 64) |
| `reshape` | previous: `features` | not saved |
| `model` | previous: reshaped features (1, 3, 64, 1) | `recon` (1, 3, 64, 1) |
| `reconstruction_error` | `compare: [features, recon]` | `score` |
| `threshold` | `input: score` | `status` |

`reconstruction_error` reshapes the second input to the first one's shape
before the MSE. Both have the same element order, so the result equals the
original's `np.mean((features - recon) ** 2)`.

## Config references in the dashboard

A widget setting can point at a config value instead of repeating it:

```yaml
- widget: history_bars
  threshold: post.threshold.limit
```

The form is `<section>.<block name>.<key>`, where section is `pre`, `model` or
`post`. For `model` the block name is left out (`model.threads`). `window.<key>`
and `input.<key>` also work. `config_loader` replaces the reference with the
real value **before** the dashboard list is put in the "demo" message, so
widgets only ever see plain values.

Not resolved: the `source` and `value` settings, and any other setting that
points into a frame (`outputs.…`, `signals.…`, `timing_us`, `system.…`). Those
are read by the widget at runtime. A reference to a section that exists but a
key that does not is an error.

Block names (`block:`) must be unique within a demo, because they are used in
references and as `timing_us` keys.

## What `config_loader` checks

On load, raise a clear error (naming the file and key) for:

- missing or unknown sections; a config with only `title`, `description` and
  `dashboard` is valid (the engine idles on it, like `_template.yaml`);
- `window.size == frame_size * n_frames` (for `spectral_features`);
- `output_shape == [len(input.columns), n_frames * fft_bins / bin_size]`;
- `stride` is **not** tied to `frame_size`; they are equal only in the fan demo;
- every `compare` / `input` name is saved by an earlier block;
- block names are unique;
- every scenario `folder` exists and has at least one matching CSV;
- every `<section>.<block>.<key>` reference in the dashboard resolves.

## Paths

Every file path in a YAML (`datasets/…`, `models/…`) is resolved relative to the
**repo root**, never the working directory:

```python
REPO_ROOT = Path(__file__).resolve().parents[1]   # from a file in backend/
```

This matters when the app is started by systemd. Paths in the `dashboard`
(`assets/…`) are not file paths; they are URLs under `frontend/`.

## Widgets

Each widget's settings (`heading`, `text` and `arrow` for `message`, `series`
for `line_chart`, and so on) are documented in the docstring comment at the top
of its file in `frontend/widgets/`. A widget never knows which demo it is in.
