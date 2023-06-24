import itertools
import logging

import broker
import dgaintel

class Processor:
    """Processor is responsible for processing dns_request events from Zeek and enriching them with
    the predictions produced by the Keras model from the dgaintel package."""
    ZEEK_DGAINTEL_PREDICTION_EVENT_NAME = "dgaintel_prediction"

    def __init__(self, config) -> None:
        self._config = config
        self._intel = dgaintel.Intel()
        self._logger = logging.getLogger(__name__)

    def process(self, events: list[broker.zeek.Event]) -> list[broker.zeek.Event]:
        """Process the given events and return a list of predictions."""
        dgaintel_events = []
        for event in events:
            if event.name() != "dns_request":
                self._logger.warning(
                    "only dns_request events are supported, skipping event: %s", event.name()
                )
                continue
            dgaintel_events.append(event)

        if dgaintel_events:
            predictions = self._intel.get_prediction(
                [event.args()[2] for event in dgaintel_events], show=False
            )
            prediction_events = list(itertools.starmap(
                lambda event, pred: broker.zeek.Event(
                    self.ZEEK_DGAINTEL_PREDICTION_EVENT_NAME,
                    event.args()[0],  # connection
                    event.args()[2],  # query
                    pred.rstrip()
                ),
                zip(dgaintel_events, predictions)
            ))
            return prediction_events
        return []
