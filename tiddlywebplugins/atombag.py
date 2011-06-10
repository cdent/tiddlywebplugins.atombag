
import feedparser

from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.remotebag import retrieve_remote

def is_feed(environ, uri):
    """
    Return true if content at uri is atom or rss.
    """
    response, content = retrieve_remote(uri, method='HEAD')
    content_type = response['content-type']
    print content_type
    return 'atom+xml' in content_type or 'rss+xml' in content_type

def get_feed(environ, uri):
    print 'uri', uri
    response, content = retrieve_remote(uri)
    feed = feedparser.parse(content)
    for entry in feed.entries:
        yield Tiddler(entry.title, uri)

def get_entry(environ, uri, title):
    """
    Get an entry out of a feed as a tiddler.
    """
    response, content = retrieve_remote(uri)
    feed = feedparser.parse(content)
    tiddler = None
    for entry in feed.entries:
        print 'looking at', entry.title
        if entry.title == title:
            tiddler = Tiddler(entry.title, uri)
            print dir(entry)
            tiddler.text = entry.content[0].value
            tiddler.type = entry.content[0].type
            return tiddler
    raise NoTiddlerError('unable to find tiddler %s in feed %s'
            % (title, uri))


def init(config):
    print 'calling init in atombag'
    config['remotebag.remote_handlers'].append(
            (is_feed, (get_feed, get_entry)))
    print 'did some config'
