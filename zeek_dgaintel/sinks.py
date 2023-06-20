import itertools
import logging
from typing import Protocol

import broker

from .config import ZeekSinkConfig
from .zeek import ZeekBrokerClientContextManager

class Sink(Protocol):
    """Sink is a protocol for sink implementations."""
    def send(self, predictions: list[broker.zeek.Event]) -> None:
        """Send predictions to the sink."""
        ...

class ZeekSink(ZeekBrokerClientContextManager, Sink):
    """ZeekSink is responsible for sending predictions to Zeek."""
    def __init__(self, config: ZeekSinkConfig):
        super().__init__(config)
        self._config = config
        self._logger = logging.getLogger(__name__)

    def send(self, predictions: list[broker.zeek.Event]):
        """Send predictions to the Zeek broker sink."""
        self.endpoint.publish_batch(*zip(itertools.repeat(self._config.broker_topic), predictions))


def from_config(config: ZeekSinkConfig) -> Sink:
    """Create a sink from the given configuration."""
    if isinstance(config, ZeekSinkConfig):
        return ZeekSink(config)
    raise ValueError(f"invalid sink config: {config}")
