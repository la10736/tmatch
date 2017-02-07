import math
import pytest
from tmatch.pearson import mean, covariance, pearson


def mean_raw(seq, start, end):
    tot = 0
    for i in range(start, end + 1):
        tot += 1 if i in seq else 0
    return tot/float(end + 1 - start)


def var_raw(seq, start, end, m=None):
    if m is None:
        m = mean(seq, start, end)
    l = end - start + 1
    tot = 0
    for i in range(start, end + 1):
        v = 1 if i in seq else 0
        tot += (v - m) ** 2
    return math.sqrt(tot / l)


def covariance_raw(seq_a, seq_b, start, end, m_a=None, m_b=None):
    l = end - start + 1
    if m_a is None:
        m_a = mean_raw(seq_a, start, end)
    if m_b is None:
        m_b = mean_raw(seq_b, start, end)
    tot = 0
    par = 0
    for i in range(start, end + 1):
        a = 1 if i in seq_a else 0
        b = 1 if i in seq_b else 0
        if a and b:
            par += (a - m_a) * (b - m_b)
            print(par)

        tot += (a - m_a) * (b - m_b)
    return tot / float(l)


def pearson_raw(seq_a, seq_b, start, end):
    m_a = mean_raw(seq_a, start, end)
    m_b = mean_raw(seq_b, start, end)
    var_a = var_raw(seq_a, start, end, m_a)
    var_b = var_raw(seq_b, start, end, m_b)
    return covariance_raw(seq_a, seq_b, start, end, m_a, m_b) / (var_a * var_b)


@pytest.mark.parametrize("seq_a, seq_b, start, end, expected",
                         [({0}, {0}, 0, 1000, 1)]
                         )
def test_pearson_raw_base(seq_a, seq_b, start, end, expected):
    assert expected == pearson_raw(seq_a, seq_b, start=start, end=end)


@pytest.mark.parametrize("seq, start, end, expected",
                         [({}, 0, 1000, 0.0),
                          ({1}, 0, 1000, 1.0 / 1001),
                          ({33}, 0, 1000, 1.0 / 1001),
                          ({33, 12, 55, 55}, 0, 1000, 3.0 / 1001),
                          ],
                         )
def test_mean(seq, start, end, expected):
    assert expected == pytest.approx(mean(seq, start=start, end=end))


@pytest.mark.parametrize("seq_a, seq_b, start, end", [
    ({1, 543, 222, 11, 998}, {5, 543, 221, 12}, 0, 1000),
    ({5, 6, 7, 8}, {6, 7, 8, 9, 10}, 0, 10),
])
def test_covariance(seq_a, seq_b, start, end):
    assert covariance_raw(seq_a, seq_b, start, end) == pytest.approx(
        covariance(seq_a, seq_b, start, end)
    )


@pytest.mark.parametrize("seq_a, seq_b, start, end", [
    ({1, 12, 45, 222, 11, 998}, {5, 543, 12, 933}, 0, 1000),
    ({5, 6, 7, 8}, {6, 7, 8, 9, 1, 10}, 0, 10),
])
def test_pearson(seq_a, seq_b, start, end):
    assert pearson_raw(seq_a, seq_b, start, end) == pytest.approx(
        pearson(seq_a, seq_b, start, end)
    )