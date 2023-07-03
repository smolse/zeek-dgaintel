from unittest import mock

import broker
import pytest

from zeek_dgaintel import config, processor


@pytest.fixture(scope="module")
def genuine_domain_dns_request_event():
    """Return the dns_request event fixture for a genuine domain."""
    return broker.zeek.Event(
        "dns_request",
        str(mock.ANY),
        str(mock.ANY),
        "google.com",
        str(mock.ANY),
        str(mock.ANY)
    )


@pytest.fixture(scope="module")
def malicious_domain_dns_request_event():
    """Return the dns_request event fixture for a malicious domain."""
    return broker.zeek.Event(
        "dns_request",
        str(mock.ANY),
        str(mock.ANY),
        "voydfjjtjmjffvgkfozjevvvc.com",
        str(mock.ANY),
        str(mock.ANY)
    )


def test_zeek_processor_ignores_non_dns_request_events():
    proc = processor.Processor(config.ProcessorConfig())
    predictions = proc.process([
        broker.zeek.Event("dns_end"),
        broker.zeek.Event("dns_rejected")
    ])
    assert len(predictions) == 0


def test_zeek_processor_predict_dns_request_events(
        genuine_domain_dns_request_event,
        malicious_domain_dns_request_event
    ):
    proc = processor.Processor(config.ProcessorConfig())
    predictions = proc.process([
        genuine_domain_dns_request_event,
        malicious_domain_dns_request_event
    ])
    assert len(predictions) == 2
    assert predictions[0].args()[2] == "google.com is genuine with probability 0.0014475431526079774"
    assert predictions[1].args()[2] == "voydfjjtjmjffvgkfozjevvvc.com is DGA with probability 0.9997776746749878"
