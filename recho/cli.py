import os
import json
import argparse
from datetime import datetime as dt

from raven import Client
from configparser import ConfigParser

from . import __version__ as recho_version
from .recho import get_posts_since, post_to_slack

CONFIG_NAME = '.recho.ini'
TS_NAME = '.recho_timestamps'


class RechoError(Exception):
    pass


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'redditor', type=str,
        help="The name of the target Redditor"
    )

    parser.add_argument(
        '-V', '--version', action='version',
        version='{version}'.format(version=recho_version)
    )

    default_config_path = os.path.join(os.path.expanduser('~'), CONFIG_NAME)
    parser.add_argument(
        '--config', type=str, default="{0}".format(default_config_path),
        help="Location of the recho config file")

    default_ts_path = os.path.join(os.path.dirname(__file__), TS_NAME)
    parser.add_argument(
        '--timestamp-file', type=str, default="{0}".format(default_ts_path),
        help="Location of the recho config file")

    return parser.parse_args()


def _load_config(config_path):
    """ Load the configuration file """
    config = ConfigParser()

    if not os.path.exists(config_path):
        raise RechoError("Could not find config file at: {0}".format(config_path))

    config.read(config_path)

    return config


def _get_last_seen(redditor, ts_path):
    """ Return the last time a check was done """
    if not os.path.exists(ts_path):
        with open(ts_path, 'w') as w:  # pylint: disable=C0103
            w.write(json.dumps({}))

    with open(ts_path, 'r') as rfile:
        timestamps = json.load(rfile)

    if redditor not in timestamps:
        last_seen = dt.utcnow()
        timestamps[redditor] = last_seen.timestamp()
        with open(ts_path, 'w') as w:  # pylint: disable=C0103
            w.write(json.dumps(timestamps, indent=4, sort_keys=True))
    else:
        last_seen = dt.fromtimestamp(float(timestamps[redditor]))

    return last_seen


def main():
    # Load CLI args
    args = _get_args()

    # Load config
    config = _load_config(args.config)

    try:
        # Get last timestamp
        last_seen = _get_last_seen(args.redditor, args.timestamp_file)

        # Get new comments and threads from reddit
        new_posts = get_posts_since(config['praw'], args.redditor, last_seen)

        if not new_posts:
            return

        # Post new comments and threads to slack
        latest_timestamp = post_to_slack(config['slack'], new_posts)

        # Write new timestamp
        with open(args.timestamp_file, 'r') as r:  # pylint: disable=C0103
            timestamps = json.load(r)

        timestamps[args.redditor] = latest_timestamp.timestamp()
        with open(args.timestamp_file, 'w') as w:  # pylint: disable=C0103
            w.write(json.dumps(timestamps, indent=4, sort_keys=True))
    except Exception:
        # Log to sentry, if configured
        if 'sentry' in config:
            key, secret = config['sentry']['key'], config['sentry']['secret']
            url = 'https://{0}:{1}@sentry.io/173123'.format(key, secret)
            Client(url, release=recho_version).captureException()

        raise
