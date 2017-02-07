import logging

from tmatch import tweet
from tmatch.item import retrieve_last_n_items
from tmatch.tweet import retrieve_tweets_in_interval


def dump_time_map(output, start, end, elements):
    for t in xrange(start, end + 1):
        output.write("{} {}".format(t, int(t in elements)))


def main(extend_results, ip, samples, *timelines):
    logging.info("Read last {} extend data items from {}, filter by ip {} ".format(samples, extend_results, ip))
    items = retrieve_last_n_items(open(extend_results).read(), ip, samples)
    if not items:
        logging.info("No Items")
        return
    start_epoch, end_epoch = items[0].epoch, items[-1].epoch
    logging.info("From {} to {}".format(start_epoch, end_epoch))
    items_epoch = {item.epoch for item in items}
    assert items_epoch, "Should dump items"
    for timeline in timelines:
        user = tweet.get_user(open(timeline))
        if not user:
            logging.warning("No user in {} timeline".format(timeline))
            continue
        tweets = set(retrieve_tweets_in_interval(open(timeline).read(), start_epoch, end_epoch))
        if not tweets:
            logging.debug("No tweets for {}".format(user))
        assert tweets, "Should dump tweets"