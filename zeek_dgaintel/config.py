from dataclasses import dataclass
from enum import Enum
import os
from typing import no_type_check

class SinkType(Enum):
    """Enumeration of supported sink types."""
    ZEEK = "zeek"

@dataclass(kw_only=True)
class ZeekBrokerClientConfig:
    """Configuration for the Zeek broker client."""
    broker_host: str = "localhost"
    broker_port: int = 9999
    broker_topic: str

@dataclass(kw_only=True)
class SourceConfig(ZeekBrokerClientConfig):
    """Configuration for the source."""

@dataclass
class ProcessorConfig:
    """Configuration for the processor."""

@dataclass(kw_only=True)
class ZeekSinkConfig(ZeekBrokerClientConfig):
    """Configuration for the Zeek sink."""

@dataclass
class Config:
    """Configuration for the zeek-dgaintel service."""
    source: SourceConfig
    processor: ProcessorConfig
    sink: ZeekSinkConfig


@no_type_check
def _load_source_config() -> SourceConfig:
    """Parse configuration for the source."""
    source_config = {}
    host = os.environ.get("ZEEK_DGAINTEL_SOURCE_BROKER_HOST")
    if host:
        source_config["broker_host"] = host
    port = os.environ.get("ZEEK_DGAINTEL_SOURCE_BROKER_PORT")
    if port:
        source_config["broker_port"] = int(port)
    source_config["broker_topic"] = os.environ.get(
        "ZEEK_DGAINTEL_SOURCE_BROKER_TOPIC", "dgaintel/dns_request"
    )
    return SourceConfig(**source_config)  # pylint: disable=missing-kwoa


def _load_processor_config() -> ProcessorConfig:
    """Parse configuration for the processor."""
    return ProcessorConfig()


@no_type_check
def _load_zeek_sink_config() -> ZeekSinkConfig:
    """Parse configuration for the Zeek sink."""
    sink_config = {}
    host = os.environ.get("ZEEK_DGAINTEL_SINK_BROKER_HOST")
    if host:
        sink_config["broker_host"] = host
    port = os.environ.get("ZEEK_DGAINTEL_SINK_BROKER_PORT")
    if port:
        sink_config["broker_port"] = int(port)
    sink_config["broker_topic"] = os.environ.get(
        "ZEEK_DGAINTEL_SINK_BROKER_TOPIC", "dgaintel/prediction"
    )
    return ZeekSinkConfig(**sink_config)  # pylint: disable=missing-kwoa


def _load_sink_config() -> ZeekSinkConfig:
    """Parse configuration for the sink."""
    try:
        _ = SinkType(os.environ.get("ZEEK_DGAINTEL_SINK_TYPE", "zeek"))
    except ValueError as exc:
        raise ValueError("invalid sink type") from exc
    # Only Zeek sink is supported for now.
    return _load_zeek_sink_config()


def load_config() -> Config:
    """Parse configuration from environment variables."""
    return Config(
        source=_load_source_config(),
        processor=_load_processor_config(),
        sink=_load_sink_config()
    )
