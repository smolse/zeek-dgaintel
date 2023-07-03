from dataclasses import dataclass
from unittest import mock

import broker
import pytest

from zeek_dgaintel import config, sinks, zeek


def test_load_unsupported_sink_from_config():
    @dataclass
    class UnsupportedSinkConfig:
        pass

    with pytest.raises(ValueError):
        sinks.from_config(UnsupportedSinkConfig())


def test_load_zeek_sink_from_config():
    assert isinstance(
        sinks.from_config(config.ZeekSinkConfig(broker_topic=str(mock.ANY))),
        sinks.ZeekSink
    )


@mock.patch("zeek_dgaintel.zeek.broker.Endpoint")
def test_zeek_sink_send_prediction_events(broker_endpoint_mock):
    endpoint_mock = mock.Mock()
    broker_endpoint_mock.return_value = endpoint_mock
    zeek_sink = sinks.ZeekSink(config.load_config().sink)
    event1 = broker.zeek.Event("dgaintel_prediction")
    event2 = broker.zeek.Event("dgaintel_prediction")
    zeek_sink.send([event1, event2])
    endpoint_mock.publish_batch.assert_called_once_with(
        ("dgaintel/prediction", event1),
        ("dgaintel/prediction", event2)
    )
