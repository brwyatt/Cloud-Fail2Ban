import base64
import gzip
import json
import logging


log = logging.getLogger(__name__)


class format_dict(dict):
    def __missing__(self, key):
        return '{'+key+'}'


def compile_regex(regex, subs):
    if type(subs) is not format_dict and type(subs) is dict:
        subs = format_dict(subs)
    compiled_regex = regex % subs
    if compiled_regex == regex:  # No substitutions made
        return regex
    else:  # We made a substitution
        return compile_regex(compiled_regex, subs)


def decompress_cloudwatch_data(data):
    log.debug('Decompressing data: {0}'.format(data))
    decompressed = json.loads(str(gzip.decompress(base64.b64decode(
        data)), 'utf-8'))
    log.debug('Decompressed data to: {0}'.format(decompressed))

    return decompressed


def decompress_cloudwatch_event(event):
    event['awslogs']['data'] = decompress_cloudwatch_data(
        event['awslogs']['data'])

    return event
