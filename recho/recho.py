from sys import platform
from datetime import datetime as dt

import praw
from slacker import Slacker

from recho import __version__ as recho_version


def build_user_agent():
    recho_version_trunk = recho_version.split("+")[0]
    user_agent = '{0}:recho:{1} (by /u/IHKAS1984)'
    user_agent = user_agent.format(platform, recho_version_trunk)

    return user_agent


def get_reddit_posts_since(redditor_name, timestamp):
    """ Yields all reddit posts since timestamp for redditor
    """
    reddit = praw.Reddit(user_agent=build_user_agent())
    new_comments = list()
    for comment in reddit.get_redditor(redditor_name).get_comments('week'):
        if timestamp > dt.utcfromtimestamp(comment.created_utc):
            break

        new_comments.append(comment)

    return sorted(new_comments, key=lambda x: x.created)


def post_to_slack(slack_config, comments):
    """ Post the given comments to the configured slack channel
    """
    slack = Slacker(slack_config['token'])

    for comment in comments:
        message = format_for_slack(comment)
        slack.chat.post_message(slack_config['channel'], message, as_user=True)


def format_for_slack(comment):
    """ Format a reddit comment for slack
    """
    slack_post = ("*User*: {user_name}\n"
                  "*Thread*: {thread}\n"
                  "*Permalink*: `{permalink}`\n"
                  "```"
                  "{body}"
                  "```")
    user_name = comment.author
    thread = comment.link_title[:75]
    permalink = comment.permalink
    body = comment.body

    return slack_post.format(**locals())
