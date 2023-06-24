import logging
import signal
import sys
import time

class Service:
    """DGAIntel service for Zeek."""
    def __init__(self, source, processor, sink):
        self._logger = logging.getLogger(__name__)
        self._stop = False

        self.source = source
        self.processor = processor
        self.sink = sink

        # Handle graceful shutdown
        signal.signal(signal.SIGINT, self._terminate)
        signal.signal(signal.SIGTERM, self._terminate)

    def _terminate(self, *_):
        """Terminate the service."""
        self._logger.info("received termination signal...")
        self._stop = True

    def run(self) -> None:
        """Run the service."""
        try:
            self._logger.info("starting service...")
            with self.source as source, self.sink as sink:
                self._logger.info("service started")
                while not self._stop:
                    events = source.read()
                    if not events:
                        self._logger.debug("no events, sleeping 1 second...")
                        time.sleep(1)
                        continue
                    self._logger.debug("received %d event(s)", len(events))
                    predictions = self.processor.process(events)
                    if predictions:
                        sink.send(predictions)
        except RuntimeError as exc:
            self._logger.error(exc)
            sys.exit(1)
        finally:
            self._logger.info("service stopped")
