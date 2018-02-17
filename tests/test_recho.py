from datetime import datetime as dt, timedelta
from mock import patch, create_autospec, MagicMock
import time

from praw.models.reddit.comment import Comment
from praw.models.reddit.submission import Submission
import pytest

from recho import recho

CREDS = {'client_id': 'mock id', 'client_secret': 'mock secret'}
SLACK = {'token': 'mock token', 'channel': 'mock channel'}
TS = dt.utcnow() - timedelta(days=1)
AUTHOR = 'mock author'
TITLE = 'Mock Title ' + '0123456789' * 7
LINK = "http://mock.link"
TEXT = "mock body text"


def make_ts(ts):
    return int((time.mktime(ts.timetuple())+ts.microsecond/1e6))


@pytest.fixture()
def com():
    comm = create_autospec(Comment)
    comm.created_utc = make_ts(TS + timedelta(days=1))
    comm.author = AUTHOR
    comm.title = TITLE
    comm.permalink = LINK
    comm.text = TEXT
    yield comm


@pytest.fixture()
def old_com():
    comm = create_autospec(Comment)
    comm.created_utc = make_ts(TS - timedelta(days=1))
    comm.author = AUTHOR
    comm.title = TITLE
    comm.permalink = LINK
    comm.text = TEXT
    yield comm


@pytest.fixture()
def sub():
    subm = create_autospec(Submission)
    subm.created_utc = make_ts(TS + timedelta(days=1))
    subm.author = AUTHOR
    subm.title = TITLE
    subm.permalink = LINK
    subm.text = TEXT
    yield subm


@pytest.fixture()
def old_sub():
    subm = create_autospec(Submission)
    subm.created_utc = make_ts(TS - timedelta(days=1))
    subm.author = AUTHOR
    subm.title = TITLE
    subm.permalink = LINK
    subm.text = TEXT
    yield subm


@pytest.fixture()
def new(com, old_com, sub, old_sub):
    new = sorted([com, old_com, sub, old_sub], key=lambda x: x.created_utc)
    return reversed(new)


def test_build_user_agent():
    """ Validate user agent is built """
    assert "recho:" in recho.build_user_agent()


@patch('recho.recho.praw')
def test_get_posts_since(praw_mock, new):
    """ Validate can filter down to recent posts """
    praw_mock.Reddit.return_value = praw_mock
    praw_mock.redditor.return_value = praw_mock
    praw_mock.new.return_value = new
    posts = recho.get_posts_since(CREDS, 'mock name', TS)

    assert len(posts) == 2


@patch('recho.recho.praw')
def test_get_posts_since_exc(praw_mock, new):
    """ Validate an exception is raised if unkown type is found """
    praw_mock.Reddit.return_value = praw_mock
    praw_mock.redditor.return_value = praw_mock
    unknown = MagicMock()
    unknown.created_utc = make_ts(TS + timedelta(days=1))
    praw_mock.new.return_value = [unknown, ]

    with pytest.raises(recho.RechoError) as exc:
        recho.get_posts_since(CREDS, 'mock name', TS)

    assert "Unknown comment/submission" in str(exc.value)


@patch('recho.recho.Slacker')
def test_post_to_slack(slack_mock, new):
    """ """
    slack_mock.return_value = slack_mock

    recho.post_to_slack(SLACK, new)

    assert slack_mock.chat.post_message.call_count == 4
