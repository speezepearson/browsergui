import json
import logging
import shlex
import subprocess
from pathlib import Path

from watchman_context import with_triggers # curl -o ~/Downloads/watchman_context.py https://gist.githubusercontent.com/speezepearson/39dd07131dd27e81b92e6794b182dba7/raw/f57f13f2070480edb0b304655a8728ec6296e3da/watchman_context.py
import xargsd.server # pip install xargsd

TRIGGERS = [
    {
        "name": "pytest",
        "expression": [
            "allof",
            ["not", ["pcre", ".*/__pycache__/.*", "wholename"]],
            [
                "anyof",
                ["pcre", "browsergui/.*\\.py", "wholename"],
                ["pcre", "test/.*\\.py", "wholename"]
            ]
        ],
        "stdin": ["name", "mode"],
        "command": [
            "bash",
            "-c",
            "python -m xargsd.client -s .xargsd-pytest.sock ."
        ]
    }
]


with with_triggers(dir='.', triggers=TRIGGERS):
    xargsd.server.run_server_sync(
        command=['chime-success', 'pytest', '--color=yes'],
        socket_file='.xargsd-pytest.sock',
        unique=True,
        log_level=logging.INFO,
    )
