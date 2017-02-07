import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from tmatch.pearson import pearson


def sequence(path):
    valid_lines = filter(None, [l.strip() for l in open(path).read().splitlines()])
    return {int(v) for v in valid_lines}


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("usage {} <start> <end> <sequence_a> <sequence_b>".format(sys.argv[0]))
        sys.exit(-1)
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    seq_a = sequence(sys.argv[3])
    seq_b = sequence(sys.argv[4])
    print("Pearson = {}".format(pearson(seq_a, seq_b, start, end)))