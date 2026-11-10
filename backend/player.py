"""
The CSV data source: replays recorded CSV data one window at a time at the
recorded speed. next() returns the next window; set_scenario() switches
recordings for the scenario buttons. Written so other data sources (UART,
Ethernet live data) can be added later behind the same next() interface.
Not implemented yet.
"""
