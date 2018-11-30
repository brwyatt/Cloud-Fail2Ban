import json

from cloud_f2b.lambda_helpers import run_filters, unpack_cloudwatch_event
from cloud_f2b.logging import setup_logging


log = setup_logging()


def run(event, context):
    """
    Lambda function for receiving events from CloudWatch and checking against
    defined filters.

    This is the first phase of the 2-phase variant.
    """
    log.debug('Received CloudWatch event: {0}'.format(json.dumps(event)))
    run_filters(unpack_cloudwatch_event(event))
