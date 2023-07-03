from unittest import mock

import broker

from zeek_dgaintel.config import load_config
from zeek_dgaintel.source import Source


@mock.patch("zeek_dgaintel.zeek.broker.Endpoint")
def test_source_read_events(broker_endpoint_mock):
    endpoint_mock = mock.Mock()
    broker_endpoint_mock.return_value = endpoint_mock
    source = Source(load_config().source)
    source.sub = mock.Mock()
    source.sub.poll.return_value = [
        ("dgaintel/dns_request", broker.zeek.Event("dns_request", *[str(mock.ANY)]*5)),
    ]
    events = source.read()
    assert len(events) == 1
    assert events[0].name() == "dns_request"
