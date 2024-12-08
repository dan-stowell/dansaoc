import argparse
import collections
import copy
import math
import operator
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
        mul_re = re.compile(r'mul\((?P<left>\d+),(?P<right>\d+)\)')
        sum_of_multiplications = 0
        for match in mul_re.finditer(self.puzzle_input):
            sum_of_multiplications += int(match.group('left')) * int(match.group('right'))
        return sum_of_multiplications


    def part02(self):
        instruction_re = re.compile(r"(?P<dont_instruction>don't\(\))|(?P<do_instruction>do\(\))|(?P<multiplication>mul\((?P<left>\d+),(?P<right>\d+)\))")
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

    def swap_incorrectly_ordered_pages(self, page_update):
        indices_pages = tuple(enumerate(page_update))
        page2index = { page: index for index, page in indices_pages }
        update_with_swapped_pages = list(page_update)
        for index, page in indices_pages:
            if page in self.before2afters:
                after_pages = self.before2afters[page]
                for after_page in after_pages:
                    if after_page in page2index:
                        after_index = page2index[after_page]
                        if after_index > index:
                            continue
                        else:
                            update_with_swapped_pages[index] = after_page
                            update_with_swapped_pages[after_index] = page
                            return update_with_swapped_pages
                    else:
                        continue
            else:
                continue
        return update_with_swapped_pages


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

    def part02(self):
        corrected_page_updates = []
        for page_update in self.page_updates:
            if not self.is_page_update_in_order(page_update):
                page_update_in_correct_order = False
                update_with_swapped_pages = page_update
                while not page_update_in_correct_order:
                    update_with_swapped_pages = self.swap_incorrectly_ordered_pages(update_with_swapped_pages)
                    page_update_in_correct_order = self.is_page_update_in_order(update_with_swapped_pages)
                corrected_page_updates.append(update_with_swapped_pages)

        sum_middle_pages = 0
        for corrected_page_update in corrected_page_updates:
            middle_index = math.floor(len(corrected_page_update) / 2)
            middle_page = corrected_page_update[middle_index]
            sum_middle_pages += middle_page

        return sum_middle_pages


class Day06Grid:
    def __init__(self, grid_string):
        self.row_strings = grid_string.splitlines()
        self.num_rows = len(self.row_strings)
        self.num_columns = len(self.row_strings[0])

    def find(self, character):
        for row, row_string in enumerate(self.row_strings):
            column = row_string.find(character)
            if column < 0:
                continue
            else:
                return row, column
        return None, None

    def insert_obstacle(self, row, column):
        row_string = self.row_strings[row]
        modified_row_string = row_string[:column] + 'O' + row_string[column + 1:]
        self.row_strings[row] = modified_row_string

    def walk(self, row, column, direction):
        turn_right = {
            (-1, 0): (0, 1),
            (0, 1): (1, 0),
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
        }
        while True:
            yield ((row, column), direction)
            row_in_front, column_in_front = row + direction[0], column + direction[1]
            if row_in_front < 0 or row_in_front >= self.num_rows or column_in_front < 0 or column_in_front >= self.num_columns:
                break
            is_obstacle_in_front = self.row_strings[row_in_front][column_in_front] in ('#', 'O')
            if is_obstacle_in_front:
                direction = turn_right[direction]
                continue
            else:
                row, column = row_in_front, column_in_front
                continue


class Day06:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.start_grid = Day06Grid(self.puzzle_input)

    def part01(self):
        start_row, start_column = self.start_grid.find('^')
        visited_positions = set()
        for position, direction in self.start_grid.walk(start_row, start_column, (-1, 0)):
            visited_positions.add(position)
        return len(visited_positions)

    def part02(self):
        start_row, start_column = self.start_grid.find('^')
        obstacle_positions_that_cause_cycles = set()
        for obstacle_row in range(self.start_grid.num_rows):
            for obstacle_column in range(self.start_grid.num_columns):
                already_has_obstacle = self.start_grid.row_strings[obstacle_row][obstacle_column] == '#'
                is_start = obstacle_row == start_row and obstacle_column == start_column
                if already_has_obstacle or is_start:
                    continue
                else:
                    grid_copy = copy.deepcopy(self.start_grid)
                    grid_copy.insert_obstacle(obstacle_row, obstacle_column)
                    visited_positions_directions = set()
                    for position, direction in grid_copy.walk(start_row, start_column, (-1, 0)):
                        found_cycle = (position, direction) in visited_positions_directions
                        if found_cycle:
                            obstacle_positions_that_cause_cycles.add((obstacle_row, obstacle_column))
                            break
                        visited_positions_directions.add((position, direction))

        return len(obstacle_positions_that_cause_cycles)


def day07_concat_whole_numbers(left, right):
    return int(str(left) + str(right))

def day07_results_matching_test_value(operators, test_value, result_so_far, numbers):
    # print('test_value', test_value, 'result_so_far', result_so_far, 'numbers', numbers)
    if len(numbers) == 0:
        if result_so_far == test_value:
            return (result_so_far,)
        else:
            return ()
    number = numbers[0]
    rest = numbers[1:]
    for op in operators:
        result_after_next_op = op(result_so_far, number)
        results_matching_test_value = day07_results_matching_test_value(operators, test_value, result_after_next_op, rest)
        # print('result_after_next_op', result_after_next_op, 'results_matching_test_value', results_matching_test_value)
        if len(results_matching_test_value) > 0:
            return results_matching_test_value
    return ()


class Day07:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.test_values_number_lists = []
        for line in self.puzzle_input.splitlines():
            test_value_string, number_strings = line.split(':')
            test_value = int(test_value_string)
            numbers = [int(x) for x in number_strings.split()]
            self.test_values_number_lists.append((test_value, numbers))

    def part01(self):
        total_calibration_result = 0
        operators = (operator.add, operator.mul)
        for test_value, numbers in self.test_values_number_lists:
            first_number = numbers[0]
            rest = numbers[1:]
            results_matching_test_value = day07_results_matching_test_value(operators, test_value, first_number, rest)
            if len(results_matching_test_value) > 0:
                total_calibration_result += test_value
        return total_calibration_result

    def part02(self):
        total_calibration_result = 0
        operators = (operator.add, operator.mul, day07_concat_whole_numbers)
        for test_value, numbers in self.test_values_number_lists:
            first_number = numbers[0]
            rest = numbers[1:]
            results_matching_test_value = day07_results_matching_test_value(operators, test_value, first_number, rest)
            if len(results_matching_test_value) > 0:
                total_calibration_result += test_value
        return total_calibration_result


class Day08:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.row_strings = self.puzzle_input.splitlines()
        self.num_rows = len(self.row_strings)
        self.num_columns = len(self.row_strings[0])

    def is_on_map(self, location):
        row, column = location
        return row >= 0 and row < self.num_rows and column >= 0 and column <= self.num_columns

    def part01(self):
        frequency2locations = collections.defaultdict(list)
        for row, row_string in enumerate(self.row_strings):
            for column, frequency in enumerate(row_string):
                if frequency == '.':
                    continue
                frequency2locations[frequency].append((row, column))
        potential_antinodes = set()
        for frequency, locations in frequency2locations.items():
            for i, location in enumerate(locations):
                row, column = location
                other_locations = locations[:i] + locations[i + 1:]
                for other_location in other_locations:
                    other_row, other_column = other_location
                    abs_row_difference, abs_column_difference = abs(row - other_row), abs(column - other_column)

                    if (row < other_row and column > other_column):
                        # location NE, other_location SW
                        northeastern_antinode = (row - abs_row_difference, column + abs_column_difference)
                        potential_antinodes.add(northeastern_antinode)
                        southwestern_antinode = (other_row + abs_row_difference, other_column - abs_column_difference)
                        potential_antinodes.add(southwestern_antinode)
                        continue

                    elif (row > other_row and column < other_column):
                        # location SW, other_location NE
                        southwestern_antinode = (row + abs_row_difference, column - abs_column_difference)
                        potential_antinodes.add(southwestern_antinode)
                        northeastern_antinode = (other_row - abs_row_difference, other_column + abs_column_difference)
                        potential_antinodes.add(northeastern_antinode)
                        continue

                    elif (row < other_row and column < other_column):
                        # location NW, other_location SE
                        northwestern_antinode = (row - abs_row_difference, column - abs_column_difference)
                        potential_antinodes.add(northwestern_antinode)
                        southeastern_antinode = (other_row + abs_row_difference, other_column + abs_column_difference)
                        potential_antinodes.add(southeastern_antinode)
                        continue

                    elif (row > other_row and column > other_column):
                        # location SE, other_location NW
                        southeastern_antinode = (row + abs_row_difference, column + abs_column_difference)
                        potential_antinodes.add(southeastern_antinode)
                        northwestern_antinode = (other_row - abs_row_difference, other_column - abs_column_difference)
                        potential_antinodes.add(northwestern_antinode)
                        continue

                    elif (row < other_row and column == other_column):
                        # location N, other_location S
                        northern_antinode = (row - abs_row_difference, column)
                        potential_antinodes.add(northern_antinode)
                        southern_antinode = (other_row + abs_row_difference, other_column)
                        potential_antinodes.add(southern_antinode)
                        continue

                    elif (row > other_row and column == other_column):
                        # location S, other_location N
                        southern_antinode = (row + abs_row_difference, column)
                        potential_antinodes.add(southern_antinode)
                        northern_antinode = (other_row - abs_row_difference, other_column)
                        potential_antinodes.add(northern_antinode)
                        continue

                    elif (row == other_row and column < other_column):
                        # location W, other_location E
                        western_antinode = (row, column - abs_column_difference)
                        potential_antinodes.add(western_antinode)
                        eastern_antinode = (other_row, other_column + abs_column_difference)
                        potential_antinodes.add(eastern_antinode)
                        continue

                    elif (row == other_row and column > other_column):
                        # location E, other_location W
                        eastern_antinode = (row, column + abs_column_difference)
                        potential_antinodes.add(eastern_antinode)
                        western_antinode = (other_row, other_column - abs_column_difference)
                        potential_antinodes.add(western_antinode)
                        continue

                    else:
                        assert(False)
        antinodes_on_map = set(potential_antinode for potential_antinode in potential_antinodes if self.is_on_map(potential_antinode))
        return len(antinodes_on_map)


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
        6: Day06,
        7: Day07,
        8: Day08,
    }
    DayClass = day2class[args.day]
    if args.part == 1:
        result = DayClass(puzzle_input).part01() # type: ignore[attr-defined]
    elif args.part == 2:
        result = DayClass(puzzle_input).part02() # type: ignore[attr-defined]
    else:
        result = None
    print(result)
