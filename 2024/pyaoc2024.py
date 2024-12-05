import argparse
import collections
import functools
import math
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


class Day04:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.grid = self.puzzle_input.splitlines()

    def has_letters_in_direction(self, letters_to_find, position, direction):
        if len(letters_to_find) <= 0:
            return True
        row, column = position
        if row < 0 or row >= len(self.grid) or column < 0 or column >= len(self.grid[0]):
            return False
        letter = self.grid[row][column]
        if letter == letters_to_find[0]:
            next_position = (row + direction[0], column + direction[1])
            return self.has_letters_in_direction(letters_to_find[1:], next_position, direction)
        else:
            return False

    def part01(self):
        directions = {
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        }
        xmas_count = 0
        for (row, row_string) in enumerate(self.grid):
            for (column, letter) in enumerate(row_string):
                if letter == 'X':
                    for direction in directions:
                        next_position = ((row + direction[0]), (column + direction[1]))
                        if self.has_letters_in_direction('MAS', next_position, direction):
                            xmas_count += 1
                else:
                    continue
        return xmas_count


    def part02(self):
        xmas_count = 0
        for (row, row_string) in enumerate(self.grid):
            for (column, letter) in enumerate(row_string):
                if letter == 'A':
                    # MAS, MAS
                    # MAS, SAM
                    # SAM, MAS
                    # SAM, SAM
                    northwest_to_southeast_has_letters = (
                        self.has_letters_in_direction('MAS', (row - 1, column - 1), (1, 1)) or
                        self.has_letters_in_direction('SAM', (row - 1, column - 1), (1, 1))
                    )
                    northeast_to_southwest_has_letters = (
                        self.has_letters_in_direction('MAS', (row - 1, column + 1), (1, -1)) or
                        self.has_letters_in_direction('SAM', (row - 1, column + 1), (1, -1))
                    )
                    if northwest_to_southeast_has_letters and northeast_to_southwest_has_letters:
                        xmas_count += 1
                    else:
                        continue
                else:
                    continue
        return xmas_count


class Day05:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.before2afters = collections.defaultdict(set)
        self.page_updates = []
        for line in self.puzzle_input.splitlines():
            if '|' in line:
                before, after = tuple(int(x) for x in line.split('|'))
                self.before2afters[before].add(after)
            elif ',' in line:
                pages_to_produce = tuple(int(x) for x in line.split(','))
                self.page_updates.append(pages_to_produce)
            else:
                continue


    def is_page_update_in_order(self, page_update):
        indices_pages = tuple(enumerate(page_update))
        page2index = { page: index for index, page in indices_pages }
        for index, page in indices_pages:
            if page in self.before2afters:
                after_pages = self.before2afters[page]
                for after_page in after_pages:
                    if after_page in page2index:
                        after_index = page2index[after_page]
                        if after_index > index:
                            continue
                        else:
                            return False
                    else:
                        continue
            else:
                continue
        return True


    def part01(self):
        updates_in_correct_order = []
        for page_update in self.page_updates:
            is_page_update_in_correct_order = self.is_page_update_in_order(page_update)
            if is_page_update_in_correct_order:
                updates_in_correct_order.append(page_update)

        sum_middle_pages = 0
        for update_in_correct_order in updates_in_correct_order:
            middle_index = math.floor(len(update_in_correct_order) / 2)
            middle_page = update_in_correct_order[middle_index]
            sum_middle_pages += middle_page

        return sum_middle_pages

    def less_than(self, a_page, another_page):
        result =  another_page in self.before2afters.get(a_page, ()) or a_page < another_page
        print('a_page', a_page, 'another_page', another_page, 'result', result)
        return result

    def part02(self):
        updates_in_incorrect_order = []
        for page_update in self.page_updates:
            is_page_update_in_correct_order = self.is_page_update_in_order(page_update)
            if not is_page_update_in_correct_order:
                updates_in_incorrect_order.append(page_update)
        corrected_page_updates = []
        for incorrect_update in updates_in_incorrect_order:
            corrected_page_update = sorted(incorrect_update, key=functools.cmp_to_key(self.less_than))
            corrected_page_updates.append(corrected_page_update)
            print('incorrect', incorrect_update, 'corrected', corrected_page_update)

        sum_middle_pages = 0
        for corrected_page_update in corrected_page_updates:
            middle_index = math.floor(len(corrected_page_update) / 2)
            middle_page = corrected_page_update[middle_index]
            sum_middle_pages += middle_page

        return sum_middle_pages


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
        4: Day04,
        5: Day05,
    }
    DayClass = day2class[args.day]
    if args.part == 1:
        result = DayClass(puzzle_input).part01()
    elif args.part == 2:
        result = DayClass(puzzle_input).part02()
    else:
        result = None
    print(result)
