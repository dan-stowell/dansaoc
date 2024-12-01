import argparse
import collections


class Day01:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input

    def part01(self):
        lines = self.puzzle_input.splitlines()
        left = []
        right = []
        for line in lines:
            tokens = line.split()
            left.append(int(tokens[0]))
            right.append(int(tokens[1]))
        left_sorted = sorted(left)
        right_sorted = sorted(right)
        sum_of_differences = 0
        for l, r in zip(left_sorted, right_sorted):
            difference = abs(l - r)
            sum_of_differences += difference
        return sum_of_differences

    def part02(self):
        lines = self.puzzle_input.splitlines()
        left = []
        right = []
        for line in lines:
            tokens = line.split()
            left.append(int(tokens[0]))
            right.append(int(tokens[1]))
        right2count = collections.defaultdict(int)
        for r in right:
            right2count[r] += 1
        sum_of_similarity_scores = 0
        for l in left:
            similarity_score = l * right2count[l]
            sum_of_similarity_scores += similarity_score
        return sum_of_similarity_scores


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int)
    parser.add_argument('part', type=int)
    parser.add_argument('filename')
    args = parser.parse_args()
    with open(args.filename) as f:
        puzzle_input = f.read()

    day2class = {
        1: Day01,
    }
    DayClass = day2class[args.day]
    if args.part == 1:
        result = DayClass(puzzle_input).part01()
    elif args.part == 2:
        result = DayClass(puzzle_input).part02()
    print(result)
