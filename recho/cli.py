import os
import json
import argparse
from datetime import datetime as dt

from raven import Client
from configparser import ConfigParser

from recho import __version__ as recho_version
from recho.recho import get_reddit_posts_since, post_to_slack

CONFIG_NAME = '.recho.ini'

TS_NAME = '.recho_timestamps'
TS_FILEPATH = os.path.join(os.path.dirname(__file__), TS_NAME)


class RechoError(Exception):
    pass


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'redditor', type=str,
        help="The name of the target Redditor"
    )

    return parser.parse_args()


def _load_config():
    """ Load the configuration file """
    config = ConfigParser()
    config_path = os.path.join(os.path.expanduser('~'), CONFIG_NAME)

    if not os.path.exists(config_path):
        raise RechoError("Config file must be present in ~/.recho.ini")

    config.read(config_path)

    return config


def _get_last_seen(redditor):
    """ Return the last time a check was done """
    if not os.path.exists(TS_FILEPATH):
        with open(TS_FILEPATH, 'w') as w:  # pylint: disable=C0103
            w.write(json.dumps({}))

    with open(TS_FILEPATH, 'r') as rfile:
        timestamps = json.load(rfile)

    if redditor not in timestamps:
        last_seen = dt.utcnow()
        timestamps[redditor] = last_seen.timestamp()
        with open(TS_FILEPATH, 'w') as w:  # pylint: disable=C0103
            w.write(json.dumps(timestamps, indent=4, sort_keys=True))
    else:
        last_seen = dt.fromtimestamp(float(timestamps[redditor]))

    return last_seen


def main():
    # Load CLI args
    args = _get_args()

    # Load config
    config = _load_config()

    try:
        # Get last timestamp
        last_seen = _get_last_seen(args.redditor)

        # Get new comments and threads from reddit
        new_posts = get_reddit_posts_since(args.redditor, last_seen)

        if new_posts:
            # Post new comments and threads to slack
            latest_timestamp = post_to_slack(config['slack'], new_posts)

            # Write new timestamp
            with open(TS_FILEPATH, 'r') as r:  # pylint: disable=C0103
                timestamps = json.load(r)

            timestamps[args.redditor] = latest_timestamp.timestamp()
            with open(TS_FILEPATH, 'w') as w:  # pylint: disable=C0103
                w.write(json.dumps(timestamps, indent=4, sort_keys=True))
    except:
        # Log to sentry, if configured
        if 'sentry' in config:
            key, secret = config['sentry']['key'], config['sentry']['secret']
            url = 'https://{0}:{1}@sentry.io/173123'.format(key, secret)
            Client(url, release=recho_version).captureException()

        raise
