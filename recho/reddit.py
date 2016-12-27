class UnsupportedSubmissionError(Exception):
    pass


class RedditBase(object):
    """ Base model for Reddit Post and Comment objects from Praw
    """
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __str__(self):
        return str(self)

    def __repr__(self):
        return "{0} -> {1}".format(self._obj.id, str(self))


class RedditComment(RedditBase):
    """ Object model for Reddit comments
    """
    @property
    def text(self):
        """ Returns the full body of the comment
        """
        return "\n>>>" + self._obj.body

    @property
    def title(self):
        """ Returns the title of the comment, truncated to 75 characters
        """
        return self._obj.link_title[:75]


class RedditSubmission(RedditBase):
    """ Object model for Reddit submissions
    """
    @property
    def text(self):
        """ Returns the text of the
        """
        if hasattr(self._obj, 'selftext') and self._obj.selftext:
            return ">>>" + self._obj.selftext
        elif hasattr(self._obj, 'preview') and 'images' in self._obj.preview:
            return self._obj.preview['images'][0]['source']['url']
        else:
            exc_msg = "Found unsupported submission type: {}".format(self._obj.id)
            raise UnsupportedSubmissionError(exc_msg)

    @property
    def title(self):
        """ Returns the title of the comment, truncated to 75 characters
        """
        return self._obj.title[:75]
