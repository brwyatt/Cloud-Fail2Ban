import json

from cloud_f2b.lambda_helpers import (run_filters, run_jails,
                                      unpack_cloudwatch_event)
from cloud_f2b.logging import setup_logging


log = setup_logging()


def run(event, context):
    """
    Lambda function for receiving events from CloudWatch and checking against
    defined filters and checking matches against the jails then sending ban
    alerts.

    This is the single-phase variant.
    """
    log.debug('Received CloudWatch event: {0}'.format(json.dumps(event)))
    matches = run_filters(unpack_cloudwatch_event(event))
    run_jails(matches)
