import dataclasses
from unittest import mock

import pytest

from zeek_dgaintel.config import load_config


def test_load_config_loads_default_configuration():
    config = load_config()
    assert dataclasses.asdict(config) == {
        "source": {
            "broker_host": "localhost",
            "broker_port": 9999,
            "broker_topic": "dgaintel/dns_request",
        },
        "processor": {},
        "sink": {
            "broker_host": "localhost",
            "broker_port": 9999,
            "broker_topic": "dgaintel/prediction",
        }
    }


@mock.patch.dict("os.environ", {
    "ZEEK_DGAINTEL_SOURCE_BROKER_HOST": "1.2.3.4",
    "ZEEK_DGAINTEL_SOURCE_BROKER_PORT": "1234",
    "ZEEK_DGAINTEL_SOURCE_BROKER_TOPIC": "source",
    "ZEEK_DGAINTEL_SINK_BROKER_HOST": "9.8.7.6",
    "ZEEK_DGAINTEL_SINK_BROKER_PORT": "9876",
    "ZEEK_DGAINTEL_SINK_BROKER_TOPIC": "sink",
}, clear=True)
def test_load_config_loads_configuration_from_env():
    config = load_config()
    assert dataclasses.asdict(config) == {
        "source": {
            "broker_host": "1.2.3.4",
            "broker_port": 1234,
            "broker_topic": "source",
        },
        "processor": {},
        "sink": {
            "broker_host": "9.8.7.6",
            "broker_port": 9876,
            "broker_topic": "sink",
        }
    }


@mock.patch.dict("os.environ", {"ZEEK_DGAINTEL_SINK_TYPE": "pulsar"}, clear=True)
def test_load_config_throws_an_error_if_sink_is_not_supported():
    with pytest.raises(ValueError):
        load_config()
