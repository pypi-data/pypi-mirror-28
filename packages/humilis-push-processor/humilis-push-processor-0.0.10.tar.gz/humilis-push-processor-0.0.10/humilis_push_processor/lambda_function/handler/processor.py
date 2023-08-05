"""Event processing logic."""

from __future__ import print_function

import logging
import json

import lambdautils.utils as utils
from lambdautils.exception import CriticalError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class KinesisError(Exception):
    pass


class FirehoseError(Exception):
    pass


def process_event(event, context, environment, layer, stage, input, output):
    """Processes incoming events."""

    events = event["Records"]

    if not input:
        input = {}

    if not output:
        output = {}

    # Arguments needed to set/get processor state.
    context = dict(environment=environment, layer=layer, stage=stage,
                   lambda_context=context)

    logger.info("Going to process {} events".format(len(events)))
    logger.info("First event: {}".format(pretty(events[0])))

    if input:
        input_delivery_stream = input.get("firehose_delivery_stream")
        if input_delivery_stream:
            send_to_delivery_stream(events, input_delivery_stream)

        events = process_input(input, events, context)
        if not events:
            return

    oevents = produce_outputs(output, events, context)

    # To make the processing task as atomic as possible we deliver the events
    # to the output streams only after all outputs have been produced.
    deliver_outputs(output, oevents)


def deliver_outputs(output, oevents):
    """Delivers the output events to their corresponding streams."""
    for i, o in enumerate(output):
        logger.info("Forwarding output #{}".format(i))
        stream = o.get("kinesis_stream")

        if not oevents[i]:
            logger.info("All events have been filtered out for this output")
            continue

        if stream:
            send_to_kinesis_stream(oevents[i], stream, o.get("partition_key"))
        else:
            logger.info("No output Kinesis stream: not forwarding to Kinesis")

        delivery_stream = o.get("firehose_delivery_stream")
        if delivery_stream:
            send_to_delivery_stream(oevents[i], delivery_stream)
        else:
            logger.info("No FH delivery stream: not forwarding to FH")


def produce_outputs(output, events, context):
    """Produces the output event streams."""
    oevents = []
    _all = lambda ev, context: True
    for i, o in enumerate(output):
        logger.info("Producing output #{}".format(i))
        ofilter = o.get("filter", _all)
        if not ofilter:
            ofilter = _all
        oevents.append([dict(ev) for ev in events if ofilter(ev, context)])
        logger.info("Selected {} events".format(len(oevents[i])))

        if not oevents[i]:
            continue

        omapper = o.get("mapper")
        if omapper:
            mapped_evs = []
            for ev in oevents[i]:
                res = omapper(ev, context)
                if isinstance(res, dict):
                    # 1-to-1 mapping: for backwards compatibility
                    mapped_evs.append(res)
                elif isinstance(res, list):
                    # 1-to-many mapping
                    mapped_evs += res
                else:
                    raise CriticalError("Mapper must return a list of dicts")
            oevents[i] = mapped_evs
            logger.info("Mapped {} events".format(len(oevents[i])))
            if mapped_evs:
                logger.info("First output event: {}".format(
                    pretty(oevents[0])))
        else:
            logger.info("No output mapper: doing nothing")

    return oevents


def process_input(input, events, context):
    """Filters and maps the input events."""
    if input.get("filter"):
        logger.info("Filtering input events")
        events = [ev for ev in events if input["filter"](ev, context)]
        if not events:
            logger.info("All input events were filtered out: nothing to do")
            return []
        else:
            logger.info("Selected {} input events".format(len(events)))
    else:
        logger.info("No input filter: using all input events")

    if input.get("mapper"):
        logger.info("Mapping input evets")
        mapped_evs = []
        for ev in events:
            res = input["mapper"](ev, context)
            if isinstance(res, dict):
                # 1-to-1 mapping: for backwards compatibility
                mapped_evs.append(res)
            elif isinstance(res, list):
                # 1-to-many mapping
                mapped_evs += res
            else:
                raise CriticalError("Mapper must return a list of dicts")

        logger.info("First mapped input events: {}".format(pretty(events[0])))
    else:
        mapped_evs = events
        logger.info("No input mapping: processing raw input events")

    return mapped_evs


def send_to_delivery_stream(events, delivery_stream):
    if events:
        logger.info("Sending events to delivery stream '{}' ...".format(
            len(events), delivery_stream))
        resp = utils.send_to_delivery_stream(events, delivery_stream)
        if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise FirehoseError(json.dumps(resp))
        logger.info(resp)


def send_to_kinesis_stream(events, stream, partition_key):
    if events:
        logger.info("Sending {} events to stream '{}' ...".format(
            len(events), stream))

        logger.info("Using partition key: {}".format(partition_key))
        resp = utils.send_to_kinesis_stream(events, stream,
                                            partition_key=partition_key)
        if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise KinesisError(json.dumps(resp))
        logger.info(resp)


def pretty(event):
    return json.dumps(event, indent=4)
