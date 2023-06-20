import logging

import broker

from .config import SourceConfig
from .zeek import ZeekBrokerClientContextManager

class Source(ZeekBrokerClientContextManager):
    """Source is responsible for reading events from Zeek."""
    def __init__(self, config: SourceConfig) -> None:
        super().__init__(config)
        self._config = config
        self._logger = logging.getLogger(__name__)

    def read(self) -> list[broker.zeek.Event]:
        """Read events from the broker."""
        return [broker.zeek.Event(data) for _, data in self.sub.poll()]
