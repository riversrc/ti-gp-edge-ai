# Frame format

The contract between the backend and the dashboard. The backend sends two kinds
of Server-Sent Events messages on `GET /stream`: one **"demo"** message when a
demo is loaded, then one **"frame"** message per window. Block and config rules
are in [blocks.md](blocks.md).

## "demo" message

Sent first on every new `/stream` connection, and again whenever a demo is
loaded. The browser clears the grid and builds the widgets from it.

```json
{"type": "demo",
 "name": "fan_blade_anomaly",
 "title": "Fan Blade Anomaly Detection",
 "scenarios": [{"id": "normal", "label": "Normal"},
               {"id": "damage", "label": "Blade Damage"}],
 "active_scenario": "normal",
 "dashboard": [ ...the YAML dashboard list... ]}
```

- `name` is the YAML filename without `.yaml`.
- `scenarios` and `active_scenario` come from `input.scenarios`. Only `id` and
  `label` are sent. `scenarios` is `[]` and `active_scenario` is `null` for a
  demo with no `input` (like `_template.yaml`).
- `dashboard` is the YAML list with every config reference
  (`post.threshold.limit`) already replaced by its value.
- While no input is configured the engine idles, so no "frame" messages follow.

## "frame" message

```json
{"type": "frame",
 "seq": 1234,
 "scenario": "normal",
 "signals":   {"channels": ["Vibx", "Viby", "Vibz"],
               "window": [[...1024], [...1024], [...1024]]},
 "outputs":   {"score": 12.7, "status": "GOOD"},
 "timing_us": {"spectral_features": 2100, "reshape": 5, "model": 3900,
               "reconstruction_error": 40, "threshold": 2, "total": 6050},
 "system":    {"cpu_pct": 31.0, "mem_pct": 22.5, "fps": 15.6}}
```

| Key | Contents |
|---|---|
| `seq` | window counter, increasing |
| `scenario` | id of the scenario playing now |
| `signals.channels` | the `input.columns` names |
| `signals.window` | the raw window, one list per channel, before pre-processing |
| `outputs` | results saved with `output:` by `post` blocks, named in the YAML |
| `timing_us` | microseconds per block, keyed by block name, plus `total` |
| `system` | `cpu_pct`, `mem_pct`, and `fps` (rolling average over 30 windows) |

## Source paths

A widget's `source` is a dotted path into the frame: `outputs.score` means
`frame.outputs.score`, and `source: timing_us` is the whole `timing_us` object.
Other frame-pointing settings (`value`, and `fps` on `metrics`) work the same
way. These are read by the widget on every frame.

One exception: `source: scenarios` (for `scenario_buttons`) reads the
`scenarios` list from the **"demo" message**, once, because it does not change
between frames. The widget highlights the button whose `id` equals
`frame.scenario`.

## `GET /demos` (draft)

JSON list used to fill the dropdown; files starting with `_` are left out.

```json
[{"name": "fan_blade_anomaly", "title": "Fan Blade Anomaly Detection"}]
```

## `POST /control`

JSON commands, applied by the engine between windows:

```json
{"cmd": "load_demo", "demo": "fan_blade_anomaly"}
{"cmd": "set_scenario", "scenario": "damage"}
```

`scenario` is a scenario `id` from the YAML.
