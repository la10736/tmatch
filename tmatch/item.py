import re


class Item(object):
    RE = re.compile("\[Time: ([^\]]+)\]"
                    "\[UTC_time: (\d+)(\.\d+)\]"
                    "\[source_ip: ([\d\.]+)\]"
                    "\[pkt: \d+\]"
                    "\[len: \d+\] Tweet\(\d+\)")

    def __init__(self, ip, epoch):
        self._ip = ip
        self._epoch = epoch

    @property
    def ip(self):
        return self._ip

    @property
    def epoch(self):
        return self._epoch

    def __eq__(self, other):
        try:
            return self.ip == other.ip and self.epoch == other.epoch
        except AttributeError:
            return False

    def __hash__(self):
        hash((self.ip, self.epoch))

    def __str__(self):
        return "{}@{}".format(self.ip, self.epoch)

    def __repr__(self):
        return str(self)

    @classmethod
    def from_extend_output_line(cls, line):
        g = cls.RE.match(line).groups()
        return cls(g[3], int(g[1]))


def _valid_lines(data):
    return [l for l in data.splitlines() if l.strip()]


def retrieve_last_n_items(complete_data, ip, n=10):
    items = [Item.from_extend_output_line(l) for l in _valid_lines(complete_data)]
    items = [i for i in items if i.ip == ip]
    return items[-n:]