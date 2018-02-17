from sys import platform
from datetime import datetime as dt

import praw
from slacker import Slacker
from praw.models.reddit.comment import Comment
from praw.models.reddit.submission import Submission

from . import __version__ as recho_version
from .reddit import RedditComment, RedditSubmission

TIME_PERIOD = 'week'


class RechoError(Exception):
    pass


def build_user_agent():
    recho_version_trunk = recho_version.split("+")[0]
    user_agent = '{0}:recho:{1} (by /u/IHKAS1984)'
    user_agent = user_agent.format(platform, recho_version_trunk)

    return user_agent


def get_posts_since(credentials, redditor_name, timestamp):
    """ Returns all reddit posts since timestamp for redditor
    """
    reddit = praw.Reddit(user_agent=build_user_agent(), **credentials)
    activity = list()

    for new in reddit.redditor(redditor_name).new():
        if dt.utcfromtimestamp(new.created_utc) <= timestamp:
            break

        if isinstance(new, Comment):
            activity.append(RedditComment(new))
        elif isinstance(new, Submission):
            activity.append(RedditSubmission(new))
        else:  # Unknown type
            msg = "Unknown comment/submission type: {0}".format(type(new))
            raise RechoError(msg)

    return sorted(activity, key=lambda x: x.created)


def post_to_slack(slack_config, posts):
    """ Post the given post or comment to the configured slack channel

        returns timestamp of the last posted message
    """
    slack = Slacker(slack_config['token'])

    last_timestamp = None
    for post in posts:
        message = format_for_slack(post)
        slack.chat.post_message(slack_config['channel'], message, as_user=True)
        last_timestamp = dt.utcfromtimestamp(post.created_utc)

    return last_timestamp


def format_for_slack(comment):
    """ Format a reddit comment for slack
    """
    slack_post = ("*User*:          {user_name}\n"
                  "*Thread*:      {thread}\n"
                  "*Permalink*: `{permalink}`\n"
                  "{text}")

    user_name = comment.author  # pylint: disable=W0612
    thread = comment.title[:75]  # pylint: disable=W0612
    permalink = 'https://www.reddit.com' + comment.permalink
    text = comment.text  # pylint: disable=W0612

    return slack_post.format(**locals())
