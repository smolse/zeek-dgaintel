from __future__ import annotations

import broker

class ZeekBrokerClientContextManager:
    """ZeekBrokerClientContextManager is a context manager for the Zeek broker client."""
    PEER_TIMEOUT = 5.0

    def __init__(self, config) -> None:
        self._config = config
        self.endpoint = broker.Endpoint()
        self.sub = self.endpoint.make_subscriber(self._config.broker_topic)
        self.status_sub = self.endpoint.make_status_subscriber(True)

    def __enter__(self) -> ZeekBrokerClientContextManager:
        self.endpoint.peer(self._config.broker_host, self._config.broker_port, self.PEER_TIMEOUT)
        status = self.status_sub.get()
        if not (
                isinstance(status, broker.Status)
                and status.code() == broker.SC.EndpointDiscovered
                ):
            raise RuntimeError(
                f"failed to connect to the Zeek broker at "
                f"{self._config.broker_host}:{self._config.broker_port}"
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.sub.reset()
        self.status_sub.reset()
        self.endpoint.shutdown()
