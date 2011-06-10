"""
Use an atom or rss feed as a remote bag.
"""

import feedparser

from tiddlyweb.store import NoTiddlerError
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.remotebag import retrieve_remote


def is_feed(environ, uri):
    """
    Return true if content at uri is atom or rss.
    """
    response, _ = retrieve_remote(uri, method='HEAD')
    content_type = response['content-type']
    return 'atom+xml' in content_type or 'rss+xml' in content_type


def get_feed(environ, uri):
    """
    Retrieve a feed and parse for tiddlers.
    """
    _, content = retrieve_remote(uri)
    feed = feedparser.parse(content)
    for entry in feed.entries:
        yield Tiddler(entry.title, uri)


def get_entry(environ, uri, title):
    """
    Get an entry out of a feed as a tiddler.
    """
    _, content = retrieve_remote(uri)
    feed = feedparser.parse(content)
    tiddler = None
    for entry in feed.entries:
        if entry.title == title:
            tiddler = Tiddler(entry.title, uri)
            tiddler.text = entry.content[0].value
            tiddler.type = entry.content[0].type
            return tiddler
    raise NoTiddlerError('unable to find tiddler %s in feed %s'
            % (title, uri))


def init(config):
    """
    Set up the remote handler.
    """
    config['remotebag.remote_handlers'].append(
            (is_feed, (get_feed, get_entry)))
