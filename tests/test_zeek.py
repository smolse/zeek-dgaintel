from unittest import mock

import broker
import pytest

from zeek_dgaintel.config import load_config
from zeek_dgaintel.zeek import ZeekBrokerClientContextManager


@mock.patch("zeek_dgaintel.zeek.broker.Endpoint")
def test_zeek_broker_client_context_manager(broker_endpoint_mock):
    endpoint_mock = mock.Mock()
    broker_endpoint_mock.return_value = endpoint_mock
    config = load_config()
    zeek_broker_client_context_manager = ZeekBrokerClientContextManager(config.source)
    zeek_broker_client_context_manager.status_sub = mock.Mock()
    zeek_broker_client_context_manager.status_sub.get.return_value = broker.Status()
    with mock.patch("broker.Status.code", return_value=broker.SC.EndpointDiscovered):
        with zeek_broker_client_context_manager:
            endpoint_mock.peer.assert_called_once_with(
                "localhost", 9999, ZeekBrokerClientContextManager.PEER_TIMEOUT
            )
    endpoint_mock.shutdown.assert_called_once()


@mock.patch("zeek_dgaintel.zeek.broker.Endpoint")
def test_zeek_broker_client_context_manager_failed_to_connect(broker_endpoint_mock):
    endpoint_mock = mock.Mock()
    broker_endpoint_mock.return_value = endpoint_mock
    config = load_config()
    zeek_broker_client_context_manager = ZeekBrokerClientContextManager(config.source)
    zeek_broker_client_context_manager.status_sub = mock.Mock()
    zeek_broker_client_context_manager.status_sub.get.return_value = broker.Status()
    with mock.patch("broker.Status.code", return_value=broker.SC.EndpointUnreachable):
        with pytest.raises(RuntimeError):
            with zeek_broker_client_context_manager:
                pass
