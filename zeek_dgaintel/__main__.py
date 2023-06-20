import logging
import sys

import fire

from .config import load_config
from .processor import Processor
from .service import Service
from .sinks import from_config as load_sink_from_config
from .source import Source

def run(log_level="INFO"):  # pragma: no cover
    """Prepare and start the service."""
    try:
        logging.basicConfig(
            level=logging.getLevelName(log_level), format="%(asctime)s %(levelname)s %(message)s"
        )
    except ValueError:
        print(f"invalid log level: {log_level}", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    svc = Service(
        Source(config.source), Processor(config.processor), load_sink_from_config(config.sink)
    )
    svc.run()

# Too lazy to create a proper CLI for this service, so just use "fire" here for now.
fire.Fire(run)
