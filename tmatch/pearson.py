import math
from collections import deque


def mean(seq, start, end):
    return len(seq)/float(end + 1 - start)


def var(seq, start, end, m=None):
    if m is None:
        m = mean(seq, start, end)
    l = end - start + 1
    ones = len(seq)
    zeros = l - ones
    tot = (1 - m)**2 * ones + m ** 2 * zeros
    return math.sqrt(tot / float(l))


def count_intersection(seq_a, seq_b):
    a = deque(sorted(seq_a))
    b = deque(sorted(seq_b))
    n = 0
    while a and b:
        if a[0] == b[0]:
            a.popleft(), b.popleft()
            n += 1
        elif a[0] < b[0]:
            a.popleft()
        else:
            b.popleft()
    return n


def count_intersection_set(seq_a, seq_b):
    return len(seq_a.intersection(seq_b))


def covariance(seq_a, seq_b, start, end, m_a=None, m_b=None):
    l = end - start + 1
    if m_a is None:
        m_a = mean(seq_a, start, end)
    if m_b is None:
        m_b = mean(seq_b, start, end)
    n_intersection = count_intersection_set(seq_a, seq_b)
    just_a = (len(seq_a) - n_intersection)
    just_b = (len(seq_b) - n_intersection)
    zeros = l - n_intersection - just_a - just_b
    tot = n_intersection * (1 - m_a) * (1 - m_b)
    tot += just_a * (1 - m_a) * (0 - m_b)
    tot += just_b * (0 - m_a) * (1 - m_b)
    tot += zeros * (0 - m_a) * (0 - m_b)
    return tot / float(l)


def pearson(seq_a, seq_b, start, end):
    m_a = mean(seq_a, start, end)
    m_b = mean(seq_b, start, end)
    var_a = var(seq_a, start, end, m_a)
    var_b = var(seq_b, start, end, m_b)
    return covariance(seq_a, seq_b, start, end, m_a, m_b) / (var_a * var_b)