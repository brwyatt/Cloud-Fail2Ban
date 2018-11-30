import json

from cloud_f2b.lambda_helpers import run_jails
from cloud_f2b.logging import setup_logging
from cloud_f2b.utils import dynamodb_event_to_matches


log = setup_logging()


def run(event, context):
    """
    Lambda function for receiving events from DynamoDB and checking against
    defined jails and sending ban alerts.

    This is the second phase of the 2-phase variant.
    """
    log.debug('Received DynamoDB event: {0}'.format(json.dumps(event)))
    matches = dynamodb_event_to_matches(event)
    run_jails(matches)
