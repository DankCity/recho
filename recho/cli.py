import os
import argparse
from datetime import datetime as dt
from configparser import ConfigParser

# import appdirs

from recho.recho import get_reddit_posts_since, post_to_slack

CONFIG_NAME = '.recho.ini'

TS_NAME = '.recho_timestamp'
TS_FILEPATH = os.path.join(os.path.dirname(__file__), TS_NAME)


class RechoError(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'redditor', type=str,
        help="The name of the target Redditor"
    )

    return parser.parse_args()


def load_config():
    config = ConfigParser()
    config_path = os.path.join(os.path.expanduser('~'), CONFIG_NAME)

    if not os.path.exists(config_path):
        raise RechoError("Config file must be present in ~/.recho.ini")

    config.read(config_path)

    return config


def get_last_seen():
    """ Return the last time a check was done
    """
    if not os.path.exists(TS_FILEPATH):
        last_seen = dt.utcnow()
    else:
        with open(TS_FILEPATH, 'r') as r:
            last_seen = dt.fromtimestamp(float(r.read()))

    return last_seen


def main():
    # Load CLI args
    args = get_args()

    # Load config
    config = load_config()

    # Get last timestamp
    last_seen = get_last_seen()

    # Get comments from reddit
    activity = get_reddit_posts_since(args.redditor, last_seen)

    if activity:
        # Post posts to slack
        post_to_slack(config['slack'], activity)

    # Write new timestamp
    with open(TS_FILEPATH, 'w') as w:
        w.write(str(dt.utcnow().timestamp()))
