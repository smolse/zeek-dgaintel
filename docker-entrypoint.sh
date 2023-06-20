#!/bin/bash
set -e

. .venv/bin/activate

# Add Zeek Broker bindings package to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.11/site-packages

exec python3 -u -m zeek_dgaintel "$@"
