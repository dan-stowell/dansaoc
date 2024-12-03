import argparse
import collections
import re


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


class Day02:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input


    def part01(self):
        reports = self.puzzle_input.splitlines()
        safe_reports = []
        for report in reports:
            levels = [int(x) for x in report.split()]
            last_level = levels[0]
            differences = []
            for level in levels[1:]:
                differences.append(last_level - level)
                last_level = level
            all_decreasing = all(difference < 0 for difference in differences)
            all_increasing = all(difference > 0 for difference in differences)
            all_within_range = all(abs(difference) >= 1 and abs(difference) <= 3 for difference in differences)
            if (all_decreasing or all_increasing) and all_within_range:
                safe_reports.append(report)
        return len(safe_reports)


    def are_level_pairs_safe(self, level_pairs):
        differences = [l - r for (l, r) in level_pairs]
        all_decreasing = all(d < 0 for d in differences)
        all_increasing = all(d > 0 for d in differences)
        all_within_range = all(abs(d) >= 1 and abs(d) <= 3 for d in differences)
        return (all_decreasing or all_increasing) and all_within_range


    def part02(self):
        reports = self.puzzle_input.splitlines()
        safe_reports = []
        for report in reports:
            levels = [int(x) for x in report.split()]
            adjacent_level_pairs = zip(levels[:-1], levels[1:])
            adjacent_level_pairs_safe = self.are_level_pairs_safe(adjacent_level_pairs)
            if adjacent_level_pairs_safe:
                safe_reports.append(report)
                continue

            for index_to_remove in range(len(levels)):
                levels_with_one_removed = list(levels)
                levels_with_one_removed.pop(index_to_remove)
                level_pairs_with_one_removed = zip(levels_with_one_removed[:-1], levels_with_one_removed[1:])
                level_pairs_with_one_removed_safe = self.are_level_pairs_safe(level_pairs_with_one_removed)
                if level_pairs_with_one_removed_safe:
                    safe_reports.append(report)
                    break

        return len(safe_reports)


class Day03:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input


    def part01(self):
        mul_re = re.compile('mul\((?P<left>\d+),(?P<right>\d+)\)')
        sum_of_multiplications = 0
        for match in mul_re.finditer(self.puzzle_input):
            sum_of_multiplications += int(match.group('left')) * int(match.group('right'))
        return sum_of_multiplications


    def part02(self):
        instruction_re = re.compile("(?P<dont_instruction>don't\(\))|(?P<do_instruction>do\(\))|(?P<multiplication>mul\((?P<left>\d+),(?P<right>\d+)\))")
        sum_of_multiplications = 0
        multiplication_enabled = True
        for match in instruction_re.finditer(self.puzzle_input):
            if match.group('dont_instruction') is not None:
                multiplication_enabled = False
                continue
            elif match.group('do_instruction') is not None:
                multiplication_enabled = True
                continue
            elif match.group('multiplication') is not None:
                if multiplication_enabled:
                    sum_of_multiplications += int(match.group('left')) * int(match.group('right'))
                continue
            else:
                continue
        return sum_of_multiplications


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
        2: Day02,
        3: Day03,
    }
    DayClass = day2class[args.day]
    if args.part == 1:
        result = DayClass(puzzle_input).part01()
    elif args.part == 2:
        result = DayClass(puzzle_input).part02()
    else:
        result = None
    print(result)
