# coding=utf-8
import cStringIO
import os

import pytest

from tmatch.tweet import Tweet, retrieve_tweets_in_interval, get_user


def test_int_of():
    assert 618707468676399104 == int("618707468676399104")


@pytest.mark.parametrize("line, tid, user, when, message", [
    ("""618707468676399104  2015-07-08 09:05:30     @__zainmalik1D  @donnysIwt siete carinissime 💕""",
     618707468676399104,
     "__zainmalik1D",
     "2015-07-08 09:05:30",
     "@donnysIwt siete carinissime 💕"),
    ("""807898838660972544  2016-12-11 11:44:27  @__zainmalik1D  RT @Louis_Tomlinson: All the support has been incredible! Let's do this together tonight .""",
     807898838660972544,
     "__zainmalik1D",
     "2016-12-11 11:44:27",
     "RT @Louis_Tomlinson: All the support has been incredible! Let's do this together tonight ."),
])
def test_parse_tweeter_line(line, tid, user, when, message):
    t = Tweet.from_timeline(line)

    assert t.tid == tid
    assert t.when == when
    assert t.user == user
    assert t.message == message


def test_from_epoch_should_return_when_as_seconds_from_1970():
    t = Tweet(12345, "pippo", "2016-12-11 11:44:27", "_message_")
    assert t.from_epoch() == 1481453067


@pytest.fixture()
def complete_data():
    return open(os.path.join("resources", "timeline.txt")).read()


def test_retrieve_tweets_in_interval_should_return_empty_if_no_valid_interval(complete_data):
    assert [] == retrieve_tweets_in_interval(complete_data, 10, 100)


def test_retrieve_tweets_in_interval_should_return_tweets(complete_data):
    assert [Tweet(807898818641592320,
                  "__zainmalik1D",
                  "2016-12-11 11:44:23",
                  "RT @Louis_Tomlinson: Feeling so much love around me and my family . Mum would have been so fucking proud ( sorry for swearing mum 😝 ) love you !"),
            Tweet(807898838660972544,
                  "__zainmalik1D",
                  "2016-12-11 11:44:27",
                  "RT @Louis_Tomlinson: All the support has been incredible! Let's do this together tonight .")
            ] == retrieve_tweets_in_interval(complete_data, 1481453057, 1481453070)


def test_retrieve_tweets_in_interval_should_include_boudary(complete_data):
    assert [Tweet(807898818641592320,
                  "__zainmalik1D",
                  "2016-12-11 11:44:23",
                  "RT @Louis_Tomlinson: Feeling so much love around me and my family . Mum would have been so fucking proud ( sorry for swearing mum 😝 ) love you !"),
            Tweet(807898838660972544,
                  "__zainmalik1D",
                  "2016-12-11 11:44:27",
                  "RT @Louis_Tomlinson: All the support has been incredible! Let's do this together tonight .")
            ] == retrieve_tweets_in_interval(complete_data, 1481453063, 1481453067)


def test_get_user_should_return_user_name_from_timeline():
    f = cStringIO.StringIO("""

694958333577596928  2016-02-03 10:33:02  @__zainmalik1D  Esigo  https://t.co/zKuATBVK2K
807898773707980800  2016-12-11 11:44:12  @__zainmalik1D  RT @Louis_Tomlinson: That was harder than I ever imagined. I want to thank everyone around me and all of the amazing fans out there that made that so special!
807898818641592320  2016-12-11 11:44:23  @__zainmalik1D  RT @Louis_Tomlinson: Feeling so much love around me and my family . Mum would have been so fucking proud ( sorry for swearing mum 😝 ) love you !
    """)
    assert "__zainmalik1D" == get_user(f)
