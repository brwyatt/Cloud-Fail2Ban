import json
from socket import gethostname
from subprocess import run, PIPE
from time import time
from uuid import UUID, uuid5

import boto3

from cloud_f2b.logging import setup_logging


log = setup_logging()
base_uuid = UUID('fde6e282-3b5f-4044-9167-d96002397a27')


def main():
    log.debug('Starting up Cloud Fail2Ban client')

    host_uuid = uuid5(base_uuid, gethostname())
    queue_name = 'F2B-Client-{0}'.format(host_uuid)

    log.debug('Host\'s queue UUID: {0}'.format(host_uuid))

    log.debug('Creating SQS and SNS resources')
    sqs = boto3.resource('sqs')
    sns = boto3.resource('sns')

    log.debug('Creating SNS Topic')
    topic = sns.create_topic(Name='F2B')

    log.debug('Creating SQS Queue')
    queue = sqs.create_queue(QueueName=queue_name)
    queue.set_attributes(Attributes={
        'MessageRetentionPeriod': '3600',
        'Policy': json.dumps({
            'Version': '2012-10-17',
            'Id': '{0}/SQSDefaultPolicy'.format(queue.attributes['QueueArn']),
            'Statement': [{
                'Sid': 'Sid{0}'.format(int(time())),
                'Effect': 'Allow',
                'Principal': {'AWS': '*'},
                'Action': 'SQS:SendMessage',
                'Resource': queue.attributes['QueueArn'],
                'Condition': {
                    'ArnEquals': {
                        'aws:SourceArn': topic.arn,
                    }
                }
            }]
        })
    })

    jails = get_jail_list()
    log.debug('Local jails: {0}'.format(jails))

    log.debug('Subscribing Queue to Topic')
    subscription = topic.subscribe(Protocol='sqs',
                                   Endpoint=queue.attributes['QueueArn'])
    subscription.set_attributes(AttributeName='FilterPolicy',
                                AttributeValue=json.dumps({
                                    'jail': jails
                                }))

    # Reload subscription and queue information
    subscription.reload()
    queue.reload()

    log.debug('Entering Queue watching loop')
    wait_time = 20  # 20 is the max!
    while True:
        msgs = queue.receive_messages(WaitTimeSeconds=wait_time)
        for msg in msgs:
            bans = json.loads(json.loads(msg.body)['Message'])
            for jail in bans:
                log.info('Received {0} bans for {1}: {2}'.format(
                    len(bans[jail]), jail, bans[jail]))
                ban_ips(jail, bans[jail])
            msg.delete()


def ban_ips(jail, ips):
    for ip in ips:
        log.info('Banning {0} in {1}'.format(ip, jail))
        res = run(['sudo', 'fail2ban-client', 'set', jail, 'banip', ip],
                  stdout=PIPE, universal_newlines=True)
        log.debug(res.stdout)


def get_jail_list():
    res = run(['sudo', 'fail2ban-client', 'status'], stdout=PIPE,
              universal_newlines=True)

    # Grab the second-last line (last line is blank), grab the values (right of
    # the first ':', re-join remaining on a ':', just in case, strip whitespace,
    # then split on ', ' to grab all the jails
    jails = ':'.join(
        res.stdout.split("\n")[-2].split(':')[1:]
    ).strip().split(', ')

    return jails


if __name__ == '__main__':
    main()
