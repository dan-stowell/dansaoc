import argparse
import collections
import copy
import enum
import math
import operator
import pprint
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
        self.frequency2locations = collections.defaultdict(list)
        for row, row_string in enumerate(self.row_strings):
            for column, frequency in enumerate(row_string):
                if frequency in ('.', '#'):
                    continue
                self.frequency2locations[frequency].append((row, column))

    def is_on_map(self, location):
        row, column = location
        return row >= 0 and row < self.num_rows and column >= 0 and column < self.num_columns

    def antinodes_on_map(self):
        for frequency, locations in self.frequency2locations.items():
            for i, location in enumerate(locations):
                row, column = location
                other_locations = locations[:i] + locations[i + 1:]
                for other_location in other_locations:
                    other_row, other_column = other_location
                    abs_row_difference, abs_column_difference = abs(row - other_row), abs(column - other_column)

                    if (row < other_row and column > other_column):
                        # location NE, other_location SW
                        northeastern_antinode = (row - abs_row_difference, column + abs_column_difference)
                        if self.is_on_map(northeastern_antinode):
                            yield (frequency, location, other_location, northeastern_antinode)
                        southwestern_antinode = (other_row + abs_row_difference, other_column - abs_column_difference)
                        if self.is_on_map(southwestern_antinode):
                            yield (frequency, location, other_location, southwestern_antinode)
                        continue

                    elif (row > other_row and column < other_column):
                        # location SW, other_location NE
                        southwestern_antinode = (row + abs_row_difference, column - abs_column_difference)
                        if self.is_on_map(southwestern_antinode):
                            yield (frequency, location, other_location, southwestern_antinode)
                        northeastern_antinode = (other_row - abs_row_difference, other_column + abs_column_difference)
                        if self.is_on_map(northeastern_antinode):
                            yield (frequency, location, other_location, northeastern_antinode)
                        continue

                    elif (row < other_row and column < other_column):
                        # location NW, other_location SE
                        northwestern_antinode = (row - abs_row_difference, column - abs_column_difference)
                        if self.is_on_map(northwestern_antinode):
                            yield (frequency, location, other_location, northwestern_antinode)
                        southeastern_antinode = (other_row + abs_row_difference, other_column + abs_column_difference)
                        if self.is_on_map(southeastern_antinode):
                            yield (frequency, location, other_location, southeastern_antinode)
                        continue

                    elif (row > other_row and column > other_column):
                        # location SE, other_location NW
                        southeastern_antinode = (row + abs_row_difference, column + abs_column_difference)
                        if self.is_on_map(southeastern_antinode):
                            yield (frequency, location, other_location, southeastern_antinode)
                        northwestern_antinode = (other_row - abs_row_difference, other_column - abs_column_difference)
                        if self.is_on_map(northwestern_antinode):
                            yield (frequency, location, other_location, northwestern_antinode)
                        continue

                    elif (row < other_row and column == other_column):
                        # location N, other_location S
                        northern_antinode = (row - abs_row_difference, column)
                        if self.is_on_map(northern_antinode):
                            yield (frequency, location, other_location, northern_antinode)
                        southern_antinode = (other_row + abs_row_difference, other_column)
                        if self.is_on_map(southern_antinode):
                            yield (frequency, location, other_location, southern_antinode)
                        continue

                    elif (row > other_row and column == other_column):
                        # location S, other_location N
                        southern_antinode = (row + abs_row_difference, column)
                        if self.is_on_map(southern_antinode):
                            yield (frequency, location, other_location, southern_antinode)
                        northern_antinode = (other_row - abs_row_difference, other_column)
                        if self.is_on_map(northern_antinode):
                            yield (frequency, location, other_location, northern_antinode)
                        continue

                    elif (row == other_row and column < other_column):
                        # location W, other_location E
                        western_antinode = (row, column - abs_column_difference)
                        if self.is_on_map(western_antinode):
                            yield (frequency, location, other_location, western_antinode)
                        eastern_antinode = (other_row, other_column + abs_column_difference)
                        if self.is_on_map(eastern_antinode):
                            yield (frequency, location, other_location, eastern_antinode)
                        continue

                    elif (row == other_row and column > other_column):
                        # location E, other_location W
                        eastern_antinode = (row, column + abs_column_difference)
                        if self.is_on_map(eastern_antinode):
                            yield (frequency, location, other_location, eastern_antinode)
                        western_antinode = (other_row, other_column - abs_column_difference)
                        if self.is_on_map(western_antinode):
                            yield (frequency, location, other_location, western_antinode)
                        continue

                    else:
                        assert(False)

    def antinodes_on_map_based_on_direction(self):
        for frequency, locations in self.frequency2locations.items():
            for i, location in enumerate(locations):
                row, column = location
                other_locations = locations[:i] + locations[i + 1:]
                for other_location in other_locations:
                    other_row, other_column = other_location
                    abs_row_difference, abs_column_difference = abs(row - other_row), abs(column - other_column)

                    if (row < other_row and column > other_column):
                        # direction NE, other_direction SW
                        direction = (-abs_row_difference, abs_column_difference)
                        other_direction = (abs_row_difference, -abs_column_difference)

                    elif (row > other_row and column < other_column):
                        # direction SW, other_direction NE
                        direction = (abs_row_difference, -abs_column_difference)
                        other_direction = (-abs_row_difference, abs_column_difference)

                    elif (row < other_row and column < other_column):
                        # direction NW, other_direction SE
                        direction = (-abs_row_difference, -abs_column_difference)
                        other_direction = (abs_row_difference, abs_column_difference)

                    elif (row > other_row and column > other_column):
                        # direction SE, other_direction NW
                        direction = (abs_row_difference, abs_column_difference)
                        other_direction = (-abs_row_difference, -abs_column_difference)

                    elif (row < other_row and column == other_column):
                        # direction N, other_direction S
                        direction = (-abs_row_difference, 0)
                        other_direction = (abs_row_difference, 0)

                    elif (row > other_row and column == other_column):
                        # direction S, other_direction N
                        direction = (abs_row_difference, 0)
                        other_direction = (-abs_row_difference, 0)

                    elif (row == other_row and column < other_column):
                        # direction W, other_direction E
                        direction = (0, -abs_column_difference)
                        other_direction = (0, abs_column_difference)

                    elif (row == other_row and column > other_column):
                        # direction E, other_direction W
                        direction = (0, abs_column_difference)
                        other_direction = (0, -abs_column_difference)

                    else:
                        assert(False) # unreachable

                    potential_antinode_row = row + direction[0]
                    potential_antinode_column = column + direction[1]
                    if self.is_on_map((potential_antinode_row, potential_antinode_column)):
                        yield (frequency, location, other_location, (potential_antinode_row, potential_antinode_column))

                    other_potential_antinode_row = other_row + other_direction[0]
                    other_potential_antinode_column = other_column + other_direction[1]
                    if self.is_on_map((other_potential_antinode_row, other_potential_antinode_column)):
                        yield (frequency, location, other_location, (other_potential_antinode_row, other_potential_antinode_column))

    def antinodes_on_map_any_position(self):
        for frequency, locations in self.frequency2locations.items():
            for i, location in enumerate(locations):
                row, column = location
                other_locations = locations[:i] + locations[i + 1:]
                for other_location in other_locations:
                    yield (frequency, location, other_location, location)
                    yield (frequency, location, other_location, other_location)
                    other_row, other_column = other_location
                    abs_row_difference, abs_column_difference = abs(row - other_row), abs(column - other_column)

                    if (row < other_row and column > other_column):
                        # direction NE, other_direction SW
                        direction = (-abs_row_difference, abs_column_difference)
                        other_direction = (abs_row_difference, -abs_column_difference)

                    elif (row > other_row and column < other_column):
                        # direction SW, other_direction NE
                        direction = (abs_row_difference, -abs_column_difference)
                        other_direction = (-abs_row_difference, abs_column_difference)

                    elif (row < other_row and column < other_column):
                        # direction NW, other_direction SE
                        direction = (-abs_row_difference, -abs_column_difference)
                        other_direction = (abs_row_difference, abs_column_difference)

                    elif (row > other_row and column > other_column):
                        # direction SE, other_direction NW
                        direction = (abs_row_difference, abs_column_difference)
                        other_direction = (-abs_row_difference, -abs_column_difference)

                    elif (row < other_row and column == other_column):
                        # direction N, other_direction S
                        direction = (-abs_row_difference, 0)
                        other_direction = (abs_row_difference, 0)

                    elif (row > other_row and column == other_column):
                        # direction S, other_direction N
                        direction = (abs_row_difference, 0)
                        other_direction = (-abs_row_difference, 0)

                    elif (row == other_row and column < other_column):
                        # direction W, other_direction E
                        direction = (0, -abs_column_difference)
                        other_direction = (0, abs_column_difference)

                    elif (row == other_row and column > other_column):
                        # direction E, other_direction W
                        direction = (0, abs_column_difference)
                        other_direction = (0, -abs_column_difference)

                    else:
                        assert(False) # unreachable

                    potential_antinode_row = row + direction[0]
                    potential_antinode_column = column + direction[1]
                    assert((potential_antinode_row, potential_antinode_column) not in (location, other_location))
                    while self.is_on_map((potential_antinode_row, potential_antinode_column)):
                        yield (frequency, location, other_location, (potential_antinode_row, potential_antinode_column))
                        potential_antinode_row += direction[0]
                        potential_antinode_column += direction[1]
                        assert((potential_antinode_row, potential_antinode_column) not in (location, other_location))

                    other_potential_antinode_row = other_row + other_direction[0]
                    other_potential_antinode_column = other_column + other_direction[1]
                    assert((other_potential_antinode_row, other_potential_antinode_column) not in (location, other_location))
                    while self.is_on_map((other_potential_antinode_row, other_potential_antinode_column)):
                        yield (frequency, location, other_location, (other_potential_antinode_row, other_potential_antinode_column))
                        other_potential_antinode_row += other_direction[0]
                        other_potential_antinode_column += other_direction[1]
                        assert((other_potential_antinode_row, other_potential_antinode_column) not in (location, other_location))

    def check_antinodes_against_solution(self, antinodes_on_map):
        solution_antinodes = set()
        for row, row_string in enumerate(self.row_strings):
            for column, frequency in enumerate(row_string):
                if frequency == '#':
                    solution_antinodes.add((row, column))
        all_solution_antinodes_present = solution_antinodes.issubset(antinodes_on_map)
        if not all_solution_antinodes_present:
            return False
        for antinode in antinodes_on_map.difference(solution_antinodes):
            antinode_row, antinode_column = antinode
            frequency = self.row_strings[antinode_row][antinode_column]
            if frequency in ('.', '#'):
                return False
        return True


    def part01(self):
        antinodes_on_map = frozenset(antinode_on_map for _, _, _, antinode_on_map in self.antinodes_on_map_based_on_direction())
        return len(antinodes_on_map)

    def part02(self):
        antinodes_on_map = frozenset(antinode_on_map for _, _,_, antinode_on_map in self.antinodes_on_map_any_position())
        return len(antinodes_on_map)


class Day09:

    def __init__(self, puzzle_input):
        self.disk_map = puzzle_input.strip()
        blocks = []
        file_and_free_space_entries = []
        is_file = True
        file_id = 0
        for num_blocks_string in self.disk_map:
            num_blocks = int(num_blocks_string)
            if is_file:
                file_id_string = str(file_id)
                if num_blocks > 0:
                    blocks.extend([file_id_string] * num_blocks)
                    file_and_free_space_entries.append((is_file, file_id_string, num_blocks))
                is_file = False
                file_id += 1
                continue
            else:
                if num_blocks > 0:
                    blocks.extend(['.'] * num_blocks)
                    file_and_free_space_entries.append((is_file, '.', num_blocks))
                is_file = True
                continue
        self.blocks = blocks
        self.file_and_free_space_entries = file_and_free_space_entries

    def part01(self):
        blocks = list(self.blocks)
        num_blocks = len(blocks)
        left_index = 0
        right_index = num_blocks - 1
        while left_index < right_index:
            left_block = blocks[left_index]
            if left_block.isdigit():
                left_index += 1
                continue

            right_block = blocks[right_index]
            if not right_block.isdigit():
                right_index -= 1
                continue

            blocks[left_index] = right_block
            blocks[right_index] = left_block
            left_index += 1
            right_index -= 1
            continue

        checksum = 0
        for i, block in enumerate(blocks):
            if not block.isdigit():
                break
            checksum += (i * int(block))
        return checksum

    def part02(self):
        file_and_free_space_entries = list(self.file_and_free_space_entries)
        num_entries = len(file_and_free_space_entries)
        right_index = num_entries - 1
        while right_index >= 0:
            right_entry = file_and_free_space_entries[right_index]
            right_entry_is_file, right_entry_file_id, right_entry_num_blocks = right_entry
            assert(right_entry_num_blocks > 0)
            if not right_entry_is_file:
                right_index -= 1
                continue

            # find left space entry big enough for right entry
            left_index = None
            for i in range(right_index):
                left_entry = file_and_free_space_entries[i]
                left_entry_is_file, left_entry_file_id, left_entry_num_blocks = left_entry
                assert(left_entry_num_blocks > 0)
                if left_entry_is_file:
                    continue
                elif left_entry_num_blocks < right_entry_num_blocks:
                    continue
                else:
                    left_index = i
                    break

            if left_index is None:
                right_index -= 1
                continue
            left_entry = file_and_free_space_entries[left_index]
            left_entry_is_file, left_entry_file_id, left_entry_num_blocks = left_entry
            assert(left_entry_num_blocks > 0)

            if left_entry_num_blocks > right_entry_num_blocks:
                assert(right_entry_num_blocks > 0)
                remaining_num_blocks = left_entry_num_blocks - right_entry_num_blocks
                assert(remaining_num_blocks > 0)

                remaining_space_entry = (False, '.', remaining_num_blocks)
                space_entry_to_swap = (False, '.', right_entry_num_blocks)
                file_and_free_space_entries[left_index] = right_entry
                file_and_free_space_entries[right_index] = space_entry_to_swap
                file_and_free_space_entries.insert(left_index + 1, remaining_space_entry)
                continue
            elif left_entry_num_blocks == right_entry_num_blocks:
                file_and_free_space_entries[left_index] = right_entry
                file_and_free_space_entries[right_index] = left_entry
                right_index -= 1
                continue
            else:
                right_index -= 1
                continue

        # pprint.pprint(file_and_free_space_entries)
        # blocks = ''.join(file_id * num_blocks for _, file_id, num_blocks in file_and_free_space_entries)
        checksum = 0
        block_position = 0
        for is_file, file_id, num_blocks in file_and_free_space_entries:
            if not is_file:
                block_position += num_blocks
                continue
            for i in range(block_position, block_position + num_blocks):
                checksum += (i * int(file_id))
            block_position += num_blocks
        return checksum

class Day10:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.row_strings = self.puzzle_input.splitlines()
        self.num_rows = len(self.row_strings)
        self.num_columns = len(self.row_strings[0])

    def find_trailheads(self):
        for row, row_string in enumerate(self.row_strings):
            for column, tile in enumerate(row_string):
                if tile == '0':
                    yield row, column
                else:
                    continue

    def find_walkable_9s(self, row, column, height):
        all_walkable_9s = set()
        if height == 9:
            all_walkable_9s.add((row, column))
            return all_walkable_9s

        directions = (
            (-1, 0), # north
            (0, 1),  # east
            (1, 0),  # south
            (0, -1), # west
        )
        for d in directions:
            adjacent_row, adjacent_column = row + d[0], column + d[1]
            if adjacent_row < 0 or adjacent_row >= self.num_rows:
                continue
            if adjacent_column < 0 or adjacent_column >= self.num_columns:
                continue
            adjacent_tile = self.row_strings[adjacent_row][adjacent_column]
            if not adjacent_tile.isdigit():
                continue
            adjacent_height = int(adjacent_tile)
            if adjacent_height - height == 1:
                walkable_9s = self.find_walkable_9s(adjacent_row, adjacent_column, adjacent_height)
                all_walkable_9s.update(walkable_9s)
            else:
                continue
        return all_walkable_9s

    def part01(self):
        trailhead2walkable_9s = {}
        for trailhead in self.find_trailheads():
            trailhead_row, trailhead_column = trailhead
            walkable_9s = self.find_walkable_9s(trailhead_row, trailhead_column, 0)
            trailhead2walkable_9s[trailhead] = walkable_9s

        pprint.pprint(trailhead2walkable_9s)
        score = 0
        for walkable_9s in trailhead2walkable_9s.values():
            score += len(walkable_9s)
        return score

    def find_trails(self, row, column, height, earlier_locations):
        all_trails = set()
        if height == 9:
            trail = tuple(earlier_locations + ((row, column),))
            all_trails.add(trail)
            return all_trails

        directions = (
            (-1, 0), # north
            (0, 1),  # east
            (1, 0),  # south
            (0, -1), # west
        )
        for d in directions:
            adjacent_row, adjacent_column = row + d[0], column + d[1]
            if adjacent_row < 0 or adjacent_row >= self.num_rows:
                continue
            if adjacent_column < 0 or adjacent_column >= self.num_columns:
                continue
            adjacent_tile = self.row_strings[adjacent_row][adjacent_column]
            if not adjacent_tile.isdigit():
                continue
            adjacent_height = int(adjacent_tile)
            if adjacent_height - height == 1:
                trails = self.find_trails(adjacent_row, adjacent_column, adjacent_height, tuple(earlier_locations + (row, column)))
                all_trails.update(trails)
            else:
                continue
        return all_trails

    def part02(self):
        trailhead2trails = {}
        for trailhead in self.find_trailheads():
            trailhead_row, trailhead_column = trailhead
            trails = self.find_trails(trailhead_row, trailhead_column, 0, ())
            trailhead2trails[trailhead] = trails

        # pprint.pprint(trailhead2walkable_9s)
        score = 0
        for trails in trailhead2trails.values():
            score += len(trails)
        return score

# thanks to Claude for these two helper functions

def day11_has_even_digit_count(stone):
    # Add 1 since log10(100) = 2 but 100 has 3 digits
    digit_count = math.floor(math.log10(stone)) + 1
    return digit_count % 2 == 0


def day11_split_stone(stone):
    n = math.floor(math.log10(stone)) + 1  # digit count
    divisor = 10 ** (n//2)
    left = stone // divisor
    right = stone % divisor
    return left, right


def day11_num_stones_after_n_blinks(stone, blinks_remaining):
    print(stone, blinks_remaining)
    if blinks_remaining <= 0:
        return 1

    if stone == 0:
        next_stones = (1,)
    elif day11_has_even_digit_count(stone):
        left, right = day11_split_stone(stone)
        next_stones = (left, right)
    else:
        next_stones = (stone * 2024,)

    num_stones = 0
    for next_stone in next_stones:
        num_stones += day11_num_stones_after_n_blinks(next_stone, blinks_remaining - 1)
    return num_stones


class Day11:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.stones = tuple(int(x) for x in self.puzzle_input.split())
        self.stone_and_blinks_remaining2num_stones = {}


    def part01(self):
        num_blinks = 25
        num_stones = 0
        for stone in self.stones:
            num_stones += day11_num_stones_after_n_blinks(stone, num_blinks)
        return num_stones


    def num_stones_after_n_blinks_with_cache(self, stone, blinks_remaining):
        if blinks_remaining <= 0:
            return 1

        if (stone, blinks_remaining) in self.stone_and_blinks_remaining2num_stones:
            return self.stone_and_blinks_remaining2num_stones[(stone, blinks_remaining)]

        if stone == 0:
            next_stones = (1,)
        elif day11_has_even_digit_count(stone):
            left, right = day11_split_stone(stone)
            next_stones = (left, right)
        else:
            next_stones = (stone * 2024,)

        num_stones = 0
        for next_stone in next_stones:
            num_stones += self.num_stones_after_n_blinks_with_cache(next_stone, blinks_remaining - 1)
        self.stone_and_blinks_remaining2num_stones[(stone, blinks_remaining)] = num_stones
        return num_stones

    def part02(self):
        num_blinks = 75
        num_stones = 0
        for stone in self.stones:
            num_stones += self.num_stones_after_n_blinks_with_cache(stone, num_blinks)
        return num_stones


class Direction(enum.Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

class Day12:
    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input
        self.row_strings = self.puzzle_input.splitlines()
        self.num_rows = len(self.row_strings)
        self.num_columns = len(self.row_strings[0])

    def is_on_map(self, row, column):
        return row >= 0 and row < self.num_rows and column >= 0 and column < self.num_columns

    def walk_region(self, location):
        row, column = location
        plot_label = self.row_strings[row][column]
        locations_in_region = set((location,))
        visited = set((location,))
        to_visit_list = []
        to_visit_set = set()

        for direction in Direction:
            row_to_visit, column_to_visit = row + direction.value[0], column + direction.value[1]
            if self.is_on_map(row_to_visit, column_to_visit):
                if (row_to_visit, column_to_visit) in to_visit_set or (row_to_visit, column_to_visit) in visited:
                    continue
                else:
                    to_visit_list.append((row_to_visit, column_to_visit))
                    to_visit_set.add((row_to_visit, column_to_visit))
                    continue
            else:
                continue

        while len(to_visit_list) > 0:
            visiting_location = to_visit_list.pop(0)
            to_visit_set.remove(visiting_location)
            visited.add(visiting_location)
            assert(len(to_visit_set) == len(to_visit_list))

            visiting_row, visiting_column = visiting_location
            visiting_plot_label = self.row_strings[visiting_row][visiting_column]
            if plot_label == visiting_plot_label:
                locations_in_region.add((visiting_row, visiting_column))
                for direction in Direction:
                    row_to_consider, column_to_consider = (visiting_row + direction.value[0], visiting_column + direction.value[1])
                    if self.is_on_map(row_to_consider, column_to_consider):
                        if (row_to_consider, column_to_consider) in visited or (row_to_consider, column_to_consider) in to_visit_set:
                            continue
                        else:
                            to_visit_list.append((row_to_consider, column_to_consider))
                            to_visit_set.add((row_to_consider, column_to_consider))
                            continue
                    else:
                        continue

        return plot_label, locations_in_region

    def perimeter(self, plot_label, locations_in_region):
        sides_facing_outside = 0
        for location in locations_in_region:
            row, column = location
            for direction in Direction:
                adjacent_row, adjacent_column = row + direction.value[0], column + direction.value[1]
                if adjacent_row < 0 or adjacent_row >= self.num_rows or adjacent_column < 0 or adjacent_column >= self.num_columns:
                    sides_facing_outside += 1
                    continue
                else:
                    adjacent_plot_label = self.row_strings[adjacent_row][adjacent_column]
                    if adjacent_plot_label == plot_label:
                        continue
                    else:
                        sides_facing_outside += 1
                        continue
        return sides_facing_outside

    def part01(self):
        region2label = {}
        locations_in_a_region = set()
        for row, row_string in enumerate(self.row_strings):
            for column, plot_label in enumerate(row_string):
                location = row, column
                if location in locations_in_a_region:
                    continue
                plot_label, locations_in_region = self.walk_region(location)
                sorted_locations_in_region = tuple(sorted(locations_in_region))
                region2label[sorted_locations_in_region] = plot_label
                locations_in_a_region.update(locations_in_region)

        total_price = 0
        for sorted_locations_in_region, plot_label in region2label.items():
            area = len(sorted_locations_in_region)
            perimeter = self.perimeter(plot_label, sorted_locations_in_region)
            total_price += (area * perimeter)
        return total_price

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
        9: Day09, # 84572976092 too low
        10: Day10,
        11: Day11,
        12: Day12,
    }
    DayClass = day2class[args.day]
    if args.part == 1:
        result = DayClass(puzzle_input).part01() # type: ignore[attr-defined]
    elif args.part == 2:
        result = DayClass(puzzle_input).part02() # type: ignore[attr-defined]
    else:
        result = None
    print(result)
