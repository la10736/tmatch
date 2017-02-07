import datetime
import re


class Tweet(object):
    RE = re.compile("(\d+)\s+([^@]+)@([^ ]+)\s+(.*)")

    def __init__(self, tid, user, when, message):
        self._tid = tid
        self._user = user
        self._when = when
        self._message = message

    @property
    def tid(self):
        return self._tid

    @property
    def user(self):
        return self._user

    @property
    def when(self):
        return self._when

    @property
    def message(self):
        return self._message

    def from_epoch(self):
        d = datetime.datetime.strptime(self.when, "%Y-%m-%d %H:%M:%S")
        return int(d.strftime('%s'))

    @classmethod
    def from_timeline(cls, line):
        m = cls.RE.match(line).groups()
        return Tweet(int(m[0]), m[2], m[1].strip(), m[3])

    def __eq__(self, other):
        try:
            return self.tid == other.tid and self.user == other.user and self.when == other.when and self.message == other.message
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.tid, self.user, self.when, self. message))

    def __str__(self):
        return "[{}@{}][{}]->{}".format(self.tid, self.user, self.when, self.message)

    def __repr__(self):
        return str(self)


def _valid_lines(data):
    return [l for l in data.splitlines() if l.strip()]


def retrieve_tweets_in_interval(complete_data, start_epoch, end_epoch):
    tweets = [Tweet.from_timeline(l) for l in _valid_lines(complete_data)]
    tweets = [t for t in tweets if start_epoch <= t.from_epoch() <= end_epoch]
    return tweets


def get_user(f):
    for l in f.readlines():
        if l.strip():
            t = Tweet.from_timeline(l)
            return t.user
    return ""