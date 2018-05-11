from lxml import html
from datetime import datetime

from orgfeeds import org

import time
import feedparser
import requests


FORCE = True
TIME_FMT = '%a, %d %b %Y %H:%M:%S'


class Feed(object):
    def __init__(self, element, title):
        self.element = element
        self.title = title
        self.changed = False
        self.stored_entries = set()

    def load_org_entries(self, forget_new):
        for entry in org.get_entries(self.element):
            properties = org.get_properties(entry)
            if forget_new and 'NEW' in entry.tags:
                entry.tags.remove('NEW')
                self.changed = True
            self.stored_entries.add(properties.get('ENTRY_ID'))


class RssFeed(Feed):

    def __init__(self, element, title, properties):
        super(RssFeed, self).__init__(element, title)
        self.url = properties.get('URL')

        if not self.url:
            raise RuntimeError("missing URL property")

    def refresh(self, mark_as_new):
        r = feedparser.parse(self.url)
        if r.get('status') != 200:
            print('cannot load feed from %(url)s' % {'url': self.url})
            return

        entries = r.get('entries')
        for entry in entries:
            entry_id = entry.get('id')
            if entry_id in self.stored_entries:
                continue
            title = entry.get('title')
            link = entry.get('link')
            date = entry.get('published_parsed')
            datestr = time.strftime(TIME_FMT, date)
            entry_header = org.make_entry_header(entry_id=entry_id,
                                                 title=title,
                                                 link=link,
                                                 datestr=datestr,
                                                 new_tag=mark_as_new)
            self.element.append_clean(entry_header)
            self.changed = True


class TwitterFeed(Feed):
    def __init__(self, element, title, properties):
        super(TwitterFeed, self).__init__(element, title)
        self.url = properties.get('URL')

        if not self.url:
            raise RuntimeError("missing URL property")

    def refresh(self, mark_as_new):
        r = requests.get(self.url)
        if r.status_code != 200:
            print('cannot load feed from %(url)s' % {'url': self.url})
            return

        doc = html.document_fromstring(r.text)

        # NOTE: I think the last one is empty as a way to expand
        # the page on scroll
        for tweet in doc.find_class('tweet')[:-1]:

            tweet_class = tweet.attrib['class']
            if 'promoted-tweet' in tweet_class:
                continue

            timestamp = int(tweet.find_class('_timestamp')[0].get('data-time'))
            entry_id = self.url + '/' + str(timestamp)

            if entry_id in self.stored_entries:
                continue

            title = tweet.find_class('tweet-text')[0].text_content()
            date = datetime.fromtimestamp(timestamp)
            datestr = date.strftime(TIME_FMT)
            link = ('https://twitter.com' +
                    tweet.find_class('tweet-timestamp')[0].get('href'))

            entry_header = org.make_entry_header(entry_id=entry_id,
                                                 title=title,
                                                 link=link,
                                                 datestr=datestr,
                                                 new_tag=mark_as_new)
            self.element.append_clean(entry_header)
            self.changed = True


feed_handlers = {
    'rss': RssFeed,
    'twitter': TwitterFeed
}


def feed_factory(feed_type, element, title, properties):
    if not feed_type:
        raise RuntimeError('missing TYPE property for %(title)s' %
                           {'title': title})

    Handler = feed_handlers.get(feed_type)

    if not Handler:
        raise RuntimeError('invalid feed type: %(feed_type)s' %
                           {'feed_type': feed_type})

    return Handler(element, title, properties)


class OrgFeeds:

    def __init__(self, path):
        self.path = path
        self.feeds = []
        self.changed = FORCE

    def refresh(self, mark_as_new=False, forget_new=False):
        self._load_org_file(forget_new)
        for feed in self.feeds:
            feed.refresh(mark_as_new)
            self.changed = self.changed or feed.changed

        if self.changed:
            org.save_file(self.org_doc, self.path)
            self.changed = False
            self.feeds = []

    def _load_org_file(self, forget_new):
        self.org_doc = org.load_file(self.path)
        for feed_header in org.get_feeds(self.org_doc):
            title = feed_header.heading
            properties = org.get_properties(feed_header)
            feed_type = properties.get('TYPE')
            feed = feed_factory(feed_type, feed_header, title, properties)
            feed.load_org_entries(forget_new)
            self.feeds.append(feed)
