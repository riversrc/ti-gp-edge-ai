"""
Web server built on Python's http.server (one thread per browser connection).
Routes: GET / and frontend files; GET /demos (demo list, JSON); GET /stream
(Server-Sent Events: a "demo" message with the widget layout, then one
"frame" message per window); POST /control (pick a demo, scenario buttons;
passed to the engine). Not implemented yet.
"""
