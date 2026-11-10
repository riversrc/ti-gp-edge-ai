"""
The center of the app. Loads _template.yaml at startup. When a demo is picked,
builds the data source and pipeline from its YAML, then every window: gets a
window, runs the pipeline, adds CPU/memory stats, publishes a frame to the
server, and keeps real-time pace. Commands from the dashboard wait in a queue
and are applied between windows. One loop serves every browser tab.
Not implemented yet.
"""
