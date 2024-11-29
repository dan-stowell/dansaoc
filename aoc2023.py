import argparse
import functools
import itertools
import json
import math
import operator
import pprint
import re
import sys


def line2value_digits(line):
  first = None
  last = None
  for c in line:
    if c.isdigit():
      if first is None:
        first = c
        last = c
      else:
        last = c
    else:
      continue
  if first is not None and last is not None:
    return int(first + last)


def day01(puzzle_input, _):
  calibrationvaluesum = 0
  calibrationvalues = []
  for line in puzzle_input.splitlines():
    calibrationvalues.append(line2value_words_and_digits(line))
  for calibrationvalue in calibrationvalues:
    calibrationvaluesum += calibrationvalue
  print(calibrationvaluesum)


def line2value_words_and_digits(line):
  digitre = re.compile('one|two|three|four|five|six|seven|eight|nine|\d')
  digit2value = {
      'one': '1',
      'two': '2',
      'three': '3',
      'four': '4',
      'five': '5',
      'six': '6',
      'seven': '7',
      'eight': '8',
      'nine': '9',
      '1': '1',
      '2': '2',
      '3': '3',
      '4': '4',
      '5': '5',
      '6': '6',
      '7': '7',
      '8': '8',
      '9': '9',
  }

  reversedigitre = re.compile('eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|\d')
  reversedigit2value = {
      'eno': '1',
      'owt': '2',
      'eerht': '3',
      'ruof': '4',
      'evif': '5',
      'xis': '6',
      'neves': '7',
      'thgie': '8',
      'enin': '9',
      '1': '1',
      '2': '2',
      '3': '3',
      '4': '4',
      '5': '5',
      '6': '6',
      '7': '7',
      '8': '8',
      '9': '9',
  }

  first = None
  for m in digitre.finditer(line):
    s = m.group()
    v = digit2value[s]
    first = v
    break

  last = None
  for m in reversedigitre.finditer(''.join(reversed(line))):
    s = m.group()
    v = reversedigit2value[s]
    last = v
    break

  if first is not None and last is not None:
    return int(first + last)



def load_cubesets(puzzle_input):
  gameidre = re.compile("^Game\s+(?P<gameid>\d+):\s+(?P<cubesets>.+)$")
  cubere = re.compile('\s*(?P<cubecount>\d+)\s+(?P<cubecolor>red|blue|green)')
  gameid2cubesets = {}
  for line in puzzle_input.splitlines():
    m = gameidre.match(line)
    if m is None:
      continue
    else:
      gameid = int(m.groupdict()['gameid'])
      cubesets = m.groupdict()['cubesets']
      cubesetdicts = []
      for cubeset in cubesets.split(';'):
        cubesetdict = {}
        for cube in cubeset.split(','):
          m = cubere.match(cube)
          if m is None:
            continue
          else:
            cubecount = m.groupdict()['cubecount']
            cubecolor = m.groupdict()['cubecolor']
            cubesetdict[cubecolor] = int(cubecount)
        cubesetdicts.append(cubesetdict)
      gameid2cubesets[gameid] = cubesetdicts

  return gameid2cubesets


def find_possible_gameids(gameid2cubesets, bag_contents):
  all_gameids = set(gameid2cubesets.keys())
  impossible_gameids = set()
  for gameid, cubesets in gameid2cubesets.items():
    for cubeset in cubesets:
      for color, count in cubeset.items():
        if color not in bag_contents or count > bag_contents[color]:
          impossible_gameids.add(gameid)
  possible_gameids = all_gameids.difference(impossible_gameids)
  return possible_gameids


def find_fewest_cubes(cubesets):
  fewest_cubes = {}
  for cubeset in cubesets:
    for color, count in cubeset.items():
      fewest_cubes[color] = max(count, fewest_cubes.get(color, 0))
  return fewest_cubes


def day02(puzzle_input, bag_contents):
  gameid2cubesets = load_cubesets(puzzle_input)
  powersum = 0
  for gameid, cubesets in gameid2cubesets.items():
    fewest_cubes = find_fewest_cubes(cubesets)
    pprint.pprint(fewest_cubes)
    cubeset_power = functools.reduce(operator.mul, fewest_cubes.values())
    powersum += cubeset_power
  print(powersum)
  # possible_gameids = find_possible_gameids(gameid2cubesets, bag_contents)

def day03(puzzle_input, _):
  index2number_and_indices = {}
  index2symbol = {}
  height = 0
  width = 0
  for (y, line) in enumerate(puzzle_input.splitlines()):
    height += 1
    current_number = None
    current_number_indices = []
    for (x, c) in enumerate(line):
      width = max(width, x + 1)
      if c == '.':
        if current_number is not None:
          current_number_int = int(current_number)
          current_number_indices_tuple = tuple(current_number_indices)
          for (number_x, number_y) in current_number_indices:
            index2number_and_indices[(number_x, number_y)] = (
                current_number_int, current_number_indices_tuple)
          current_number = None
          current_number_indices = []
      elif c.isdigit():
        if current_number is None:
          current_number = c
          current_number_indices.append((x, y))
        else:
          current_number = current_number + c
          current_number_indices.append((x, y))
      else:
        index2symbol[(x, y)] = c
        if current_number is not None:
          current_number_int = int(current_number)
          current_number_indices_tuple = tuple(current_number_indices)
          for (number_x, number_y) in current_number_indices:
            index2number_and_indices[(number_x, number_y)] = (
                current_number_int, current_number_indices_tuple)
          current_number = None
          current_number_indices = []

    if current_number is not None:
      current_number_int = int(current_number)
      current_number_indices_tuple = tuple(current_number_indices)
      for (number_x, number_y) in current_number_indices:
        index2number_and_indices[(number_x,
                                  number_y)] = (current_number_int,
                                                current_number_indices_tuple)
      current_number = None
      current_number_indices = []

  symbol_adjacent_indices = set()
  deltas = (
      (-1, -1),
      (0, -1),
      (1, -1),
      (-1, 0),
      (1, 0),
      (-1, 1),
      (0, 1),
      (1, 1),
  )
  for (x, y) in index2symbol:
    for (dx, dy) in deltas:
      if x + dx >= 0 and x + dx < width and y + dy >= 0 and y + dy < height:
        symbol_adjacent_indices.add((x + dx, y + dy))

  part_numbers_and_indices = set()
  for (adjacent_x, adjacent_y) in symbol_adjacent_indices:
    if (adjacent_x, adjacent_y) in index2number_and_indices:
      part_numbers_and_indices.add(index2number_and_indices[(adjacent_x,
                                                             adjacent_y)])

  part_number_sum = 0
  for part_number, _ in part_numbers_and_indices:
    part_number_sum += part_number
  print(part_number_sum)


def find_numbers_symbols_width_height(input):
  index2number_and_indices = {}
  index2symbol = {}
  height = 0
  width = 0
  for (y, line) in enumerate(input.splitlines()):
    height += 1
    current_number = None
    current_number_indices = []
    for (x, c) in enumerate(line):
      width = max(width, x + 1)
      if c == '.':
        if current_number is not None:
          current_number_int = int(current_number)
          current_number_indices_tuple = tuple(current_number_indices)
          for (number_x, number_y) in current_number_indices:
            index2number_and_indices[(number_x, number_y)] = (
                current_number_int, current_number_indices_tuple)
          current_number = None
          current_number_indices = []
      elif c.isdigit():
        if current_number is None:
          current_number = c
          current_number_indices.append((x, y))
        else:
          current_number = current_number + c
          current_number_indices.append((x, y))
      else:
        index2symbol[(x, y)] = c
        if current_number is not None:
          current_number_int = int(current_number)
          current_number_indices_tuple = tuple(current_number_indices)
          for (number_x, number_y) in current_number_indices:
            index2number_and_indices[(number_x, number_y)] = (
                current_number_int, current_number_indices_tuple)
          current_number = None
          current_number_indices = []

    if current_number is not None:
      current_number_int = int(current_number)
      current_number_indices_tuple = tuple(current_number_indices)
      for (number_x, number_y) in current_number_indices:
        index2number_and_indices[(number_x,
                                  number_y)] = (current_number_int,
                                                current_number_indices_tuple)
      current_number = None
      current_number_indices = []
  return (index2number_and_indices, index2symbol, width, height)


def find_part_numbers_and_indices(index2number_and_indices, index2symbol,
                                  width, height):
  symbol_adjacent_indices = set()
  deltas = (
      (-1, -1),
      (0, -1),
      (1, -1),
      (-1, 0),
      (1, 0),
      (-1, 1),
      (0, 1),
      (1, 1),
  )
  for (x, y) in index2symbol:
    for (dx, dy) in deltas:
      if x + dx >= 0 and x + dx < width and y + dy >= 0 and y + dy < height:
        symbol_adjacent_indices.add((x + dx, y + dy))

  part_numbers_and_indices = set()
  for (adjacent_x, adjacent_y) in symbol_adjacent_indices:
    if (adjacent_x, adjacent_y) in index2number_and_indices:
      part_numbers_and_indices.add(index2number_and_indices[(adjacent_x,
                                                             adjacent_y)])
  return part_numbers_and_indices


def find_gears(index2number_and_indices, index2symbol):
  deltas = (
      (-1, -1),
      (0, -1),
      (1, -1),
      (-1, 0),
      (1, 0),
      (-1, 1),
      (0, 1),
      (1, 1),
  )
  gears = set()
  for ((x, y), symbol) in index2symbol.items():
    if symbol == '*':
      adjacent_part_numbers = set()
      for (dx, dy) in deltas:
        if (x + dx, y + dy) in index2number_and_indices:
          adjacent_part_numbers.add(index2number_and_indices[(x + dx, y + dy)])
      if len(adjacent_part_numbers) == 2:
        part_numbers = tuple(part_number
                             for part_number, _ in adjacent_part_numbers)
        gears.add(((x, y), part_numbers))
  return gears


def day03part02(puzzle_input, _):
  index2number_and_indices, index2symbol, width, height = find_numbers_symbols_width_height(
      puzzle_input)
  part_numbers_and_indices = find_part_numbers_and_indices(
      index2number_and_indices, index2symbol, width, height)
  # pprint.pprint(part_numbers_and_indices)
  gears = find_gears(index2number_and_indices, index2symbol)
  pprint.pprint(gears)
  gear_ratio_sum = 0
  for _, part_numbers in gears:
    gear_ratio = part_numbers[0] * part_numbers[1]
    gear_ratio_sum += gear_ratio
  print(gear_ratio_sum)


def day04part01(puzzle_input, _):
  cardre = re.compile('^\s*Card\s+(?P<card_number>\d+):\s+(?P<winning_numbers>[\s\d]+)\s+\|\s+(?P<numbers_you_have>[\s\d]+)$')
  points_sum = 0
  for line in puzzle_input.splitlines():
    m = cardre.match(line)
    card_number = int(m.group('card_number'))
    winning_numbers = set(int(x) for x in m.group('winning_numbers').split())
    numbers_you_have = set(int(x) for x in m.group('numbers_you_have').split())
    winning_numbers_you_have = winning_numbers.intersection(numbers_you_have)
    if len(winning_numbers_you_have) > 0:
      points = pow(2, len(winning_numbers_you_have) - 1)
      points_sum += points
  print(points_sum)


def day04part02(puzzle_input, _):
  cardre = re.compile('^\s*Card\s+(?P<card_number>\d+):\s+(?P<winning_numbers>[\s\d]+)\s+\|\s+(?P<numbers_you_have>[\s\d]+)$')
  cardnumbers_matches = []
  for line in puzzle_input.splitlines():
    m = cardre.match(line)
    cardnumber = int(m.group('card_number'))
    winning_numbers = set(int(x) for x in m.group('winning_numbers').split())
    numbers_you_have = set(int(x) for x in m.group('numbers_you_have').split())
    winning_numbers_you_have = winning_numbers.intersection(numbers_you_have)
    matches = len(winning_numbers_you_have)
    cardnumbers_matches.append((cardnumber, matches))

  cardnumber2instances = {cardnumber: 1 for cardnumber, _ in cardnumbers_matches}
  for cardnumber, matches in cardnumbers_matches:
    instances = cardnumber2instances[cardnumber]
    for _ in range(instances):
      for i in range(cardnumber + 1, cardnumber + 1 + matches):
        if i in cardnumber2instances:
          cardnumber2instances[i] += 1
  print(sum(cardnumber2instances.values()))


def day05lookup(source, mapping):
  for source_range_start, destination_range_start, range_length in mapping:
    if source >= source_range_start and source < source_range_start + range_length:
      return destination_range_start + (source - source_range_start)
  return source


def day05part01(puzzle_input, _):
  mapheadre = re.compile(
      '^(?P<source_category>[^\-]+)-to-(?P<destination_category>[^\s\-]+)\s+map:$'
  )
  maplinere = re.compile(
      '^(?P<destination_range_start>\d+)\s+(?P<source_range_start>\d+)\s+(?P<range_length>\d+)$'
  )
  seedsre = re.compile('^seeds:(?P<seeds>[\s+\d]+)$')

  seeds = None
  current_source_destination = None
  source2destination = {}
  for line in puzzle_input.splitlines():
    mapheadmatch = mapheadre.match(line)
    maplinematch = maplinere.match(line)
    seedsmatch = seedsre.match(line)
    if seedsmatch is not None:
      if seeds is not None:
        print('already have seeds', seeds, 'encountered another seeds line',
              seedsmatch.group('seed'))
        return
      seeds = tuple(map(int, seedsmatch.group('seeds').split()))
    elif mapheadmatch is not None:
      if current_source_destination is not None:
        print('already have map', current_source_destination,
              'encountered another map header', line.strip())
        return
      source_category = mapheadmatch.group('source_category')
      destination_category = mapheadmatch.group('destination_category')
      current_source_destination = (source_category, destination_category)
      source2destination[source_category] = (destination_category, [])
    elif maplinematch is not None:
      destination_range_start = int(
          maplinematch.group('destination_range_start'))
      source_range_start = int(maplinematch.group('source_range_start'))
      range_length = int(maplinematch.group('range_length'))
      current_source, _ = current_source_destination
      _, current_map = source2destination[current_source]
      current_map.append(
          (source_range_start, destination_range_start, range_length))
    else:
      current_source_destination = None
  pprint.pprint(seeds)
  # for source_category, (destination_category, mapping) in source2destination.items():
  # source2destination[source_category] = (destination_category, tuple(sorted(mapping)))

  pprint.pprint(source2destination)

  seed2location = {}
  for seed in seeds:
    destination_category, mapping = source2destination['seed']
    destination = day05lookup(seed, mapping)
    while destination_category in source2destination:
      destination_category, mapping = source2destination[destination_category]
      destination = day05lookup(destination, mapping)
    seed2location[seed] = destination

  pprint.pprint(seed2location)
  print(min(seed2location.values()))


def day05_parse_inputpath_to_seedranges_and_map(puzzle_input):
  mapheadre = re.compile(
      '^(?P<source_category>[^\-]+)-to-(?P<destination_category>[^\s\-]+)\s+map:$'
  )
  maplinere = re.compile(
      '^(?P<destination_range_start>\d+)\s+(?P<source_range_start>\d+)\s+(?P<range_length>\d+)$'
  )
  seedsre = re.compile('^seeds:(?P<seeds>[\s+\d]+)$')

  seedranges = None
  current_source_destination = None
  source2destination = {}
  for line in puzzle_input.splitlines():
    mapheadmatch = mapheadre.match(line)
    maplinematch = maplinere.match(line)
    seedsmatch = seedsre.match(line)
    if seedsmatch is not None:
      if seedranges is not None:
        raise (Exception(
            'already have seeds {} encountered another seeds line {}'.format(
                seedranges, seedsmatch.group('seed'))))
      seedlist = tuple(int(x) for x in seedsmatch.group('seeds').split())
      seedranges = tuple(zip(seedlist[::2], seedlist[1::2]))
    elif mapheadmatch is not None:
      if current_source_destination is not None:
        raise (Exception(
            'already have map {} encountered another map header {}'.format(
                current_source_destination, line.strip())))
      source_category = mapheadmatch.group('source_category')
      destination_category = mapheadmatch.group('destination_category')
      current_source_destination = (source_category, destination_category)
      source2destination[source_category] = (destination_category, [])
    elif maplinematch is not None:
      destination_range_start = int(
          maplinematch.group('destination_range_start'))
      source_range_start = int(maplinematch.group('source_range_start'))
      range_length = int(maplinematch.group('range_length'))
      current_source, _ = current_source_destination
      _, current_map = source2destination[current_source]
      current_map.append(
          (source_range_start, destination_range_start, range_length))
    else:
      current_source_destination = None

  return seedranges, source2destination


def day05_lookup(source, starts_lens):
  for source_range_start, destination_range_start, range_length in starts_lens:
    if source >= source_range_start and source < source_range_start + range_length:
      return destination_range_start + (source - source_range_start)
  return source


def day05_invert_map(source2destination):
  destination2source = {}
  for source, (destination, mapping) in source2destination.items():
    destination2source[destination] = (
        source,
        tuple((destination_range_start, source_range_start, range_length)
              for source_range_start, destination_range_start, range_length in
              mapping))
  return destination2source


def day05_starts_lens_to_ranges(starts_lens):
  mapped_ranges = []
  for source_range_start, destination_range_start, range_length in starts_lens:
    mapped_ranges.append(
        ((source_range_start, source_range_start + range_length),
         (destination_range_start, destination_range_start + range_length)))

  last_end = 0
  full_ranges = []
  for mapped_range in sorted(mapped_ranges):
    (start, end), (dstart, dend) = mapped_range
    if start > last_end:
      full_ranges.append(((last_end, start), (last_end, start)))
    full_ranges.append(mapped_range)
    last_end = end
  full_ranges.append(((last_end, sys.maxsize), (last_end, sys.maxsize)))

  return full_ranges


def day05_enumerate_ranges(a_range, target_mapping):
  start, end = a_range
  split_start = start
  for i, ((s, e), (ts, te)) in enumerate(target_mapping):
    if start >= e:
      continue

    if start < s and end <= s:
      continue

    if end <= e:
      yield ((start, end), (ts + (start - s), te - (e - end)))
      return
    else:
      yield ((start, e), (ts + (start - s), te))
      split_start = e
      break

  for (s, e), (ts, te) in target_mapping[i + 1:]:
    if end <= e:
      yield ((split_start, end), (ts + (split_start - s), te - (e - end)))
      return
    else:
      yield ((split_start, e), (ts + (split_start - s), te))
      split_start = e

  return


def day05_find_valid_seed(seedranges, destination2source_full_mapping, destination,
                    a_range):
  if destination == 'seed':
    start, end = a_range
    for s, e in seedranges:
      if start >= s and start < e:
        shrunk_destination_range = (max(s, start), min(e, end))
        print(destination, shrunk_destination_range, 'is in seed range',
              (s, e))
        return True, shrunk_destination_range
      if end > s and end <= e:
        shrunk_destination_range = (max(s, start), min(e, end))
        print(destination, shrunk_destination_range, 'is in seed range',
              (s, e))
        return True, shrunk_destination_range
    return False, None

  source, full_mapping = destination2source_full_mapping[destination]
  destination_source_ranges = tuple(day05_enumerate_ranges(a_range, full_mapping))
  for destination_range, source_range in destination_source_ranges:
    found, shrunk_source_range = day05_find_valid_seed(
        seedranges, destination2source_full_mapping, source, source_range)
    if found:
      source_start_difference = shrunk_source_range[0] - source_range[0]
      source_end_difference = source_range[1] - shrunk_source_range[1]
      shrunk_destination_range = (destination_range[0] + source_start_difference,
                                  destination_range[1] - source_end_difference)
      print(destination, shrunk_destination_range, 'is in seed range')
      return True, shrunk_destination_range

  return False, None


def day05part02(puzzle_input, _):
  seed_starts_lens, source2destination = day05_parse_inputpath_to_seedranges_and_map(puzzle_input)
  destination2source_full_mapping = {}
  for source, (destination, mapping) in source2destination.items():
    full_mapping = day05_starts_lens_to_ranges(mapping)
    flipped_mapping = tuple(sorted((r[1], r[0]) for r in full_mapping))
    destination2source_full_mapping[destination] = (source, flipped_mapping)

  seedranges = tuple(
      sorted((start, start + len) for (start, len) in seed_starts_lens))
  source, full_mapping = destination2source_full_mapping['location']
  for destination_range, source_range in full_mapping:
    found, shrunk_source_range = day05_find_valid_seed(
        seedranges, destination2source_full_mapping, source, source_range)
    if found:
      source_start_difference = shrunk_source_range[0] - source_range[0]
      source_end_difference = source_range[1] - shrunk_source_range[1]
      shrunk_destination_range = (destination_range[0] + source_start_difference,
                                  destination_range[1] - source_end_difference)
      print('location', shrunk_destination_range, 'is in seed range')
      break


def day06part01(puzzle_input, _):
  lines = puzzle_input.splitlines()
  race_times = tuple(int(x.strip()) for x in lines[0].split()[1:])
  record_distances = tuple(int(x.strip()) for x in lines[1].split()[1:])
  ways_to_win = []
  for race_time, record_distance in zip(race_times, record_distances):
    winning_times_and_distances = []
    for t in range(race_time + 1):
      distance = t * (race_time - t)
      if distance > record_distance:
        winning_times_and_distances.append((t, distance))
    ways_to_win.append(len(winning_times_and_distances))
  print(functools.reduce(operator.mul, ways_to_win))


def day06part02(puzzle_input, _):
  lines = puzzle_input.splitlines()
  race_time = int(''.join(x for x in lines[0].split()[1:]))
  record_distance = int(''.join(x for x in lines[1].split()[1:]))

  first_winning_time = None
  for t in range(race_time + 1):
    distance = t * (race_time - t)
    if distance > record_distance:
      first_winning_time = t
      break

  last_winning_time = None
  for t in range(race_time, -1, -1):
    distance = t * (race_time - t)
    if distance > record_distance:
      last_winning_time = t
      break

  print(first_winning_time, last_winning_time,
        last_winning_time - first_winning_time + 1)


day07part01_label2rank = {
  '2': 12,
  '3': 11,
  '4': 10,
  '5': 9,
  '6': 8,
  '7': 7,
  '8': 6,
  '9': 5,
  'T': 4,
  'J': 3,
  'Q': 2,
  'K': 1,
  'A': 0,
}

day07part01_type2rank = {
  'Five of a kind': 0,
  'Four of a kind': 1,
  'Full house': 2,
  'Three of a kind': 3,
  'Two pair': 4,
  'One pair': 5,
  'High card': 6,
}

def day07part01_hand2type(hand):
  label2count = {}
  for label in hand:
    if label in label2count:
      label2count[label] += 1
    else:
      label2count[label] = 1

  if len(label2count) == 1 and 5 in label2count.values():
    return 'Five of a kind'
  elif len(label2count) == 2 and 4 in label2count.values():
    return 'Four of a kind'
  elif len(label2count) == 2 and 3 in label2count.values() and 2 in label2count.values():
    return 'Full house'
  elif len(label2count) == 3 and 3 in label2count.values():
    return 'Three of a kind'
  elif len(label2count) == 3 and 2 in label2count.values() and 1 in label2count.values():
    return 'Two pair'
  elif len(label2count) == 4 and 2 in label2count.values():
    return 'One pair'
  elif len(label2count) == 5 and 1 in label2count.values():
    return 'High card'

  return None


def day07part01_handlt(a, b):
  a_type = day07part01_hand2type(a)
  b_type = day07part01_hand2type(b)
  a_typerank = day07part01_type2rank[a_type]
  b_typerank = day07part01_type2rank[b_type]
  if a_typerank < b_typerank:
    return True
  elif a_typerank > b_typerank:
    return False
  else:
    for i in range(len(a)):
      if day07part01_label2rank[a[i]] < day07part01_label2rank[b[i]]:
        return True
      elif day07part01_label2rank[a[i]] > day07part01_label2rank[b[i]]:
        return False
      else:
        continue
  return False


def day07part01_handkey(hand):
  handtype = day07part01_hand2type(hand)
  typerank = day07part01_type2rank[handtype]
  cardranks = tuple(day07part01_label2rank[label] for label in hand)
  return (typerank, cardranks)

def day07part01(puzzle_input, _):
  hands_bids = []
  for line in puzzle_input.splitlines():
    hand, bidstr = line.split()
    bid = int(bidstr)
    hands_bids.append((hand, bid))
  sorted_hands_bids = sorted(hands_bids, key=lambda x: day07part01_handkey(x[0]))
  total_winnings = 0
  for rank, (hand, bid) in zip(range(len(sorted_hands_bids), -1, -1), sorted_hands_bids):
    print(rank, hand, bid)
    total_winnings += rank * bid
  print(total_winnings)


day07part02_label2rank = {
  'J': 12,
  '2': 11,
  '3': 10,
  '4': 9,
  '5': 8,
  '6': 7,
  '7': 6,
  '8': 5,
  '9': 4,
  'T': 3,
  'Q': 2,
  'K': 1,
  'A': 0,
}

day07part02_type2rank = {
  'Five of a kind': 0,
  'Four of a kind': 1,
  'Full house': 2,
  'Three of a kind': 3,
  'Two pair': 4,
  'One pair': 5,
  'High card': 6,
}


def day07part02_reassign_jokers(raw_label2count):
  if 'J' not in raw_label2count:
    return raw_label2count

  negative_counts_ranks_labels = []
  for label, count in raw_label2count.items():
    if label == 'J':
      continue
    negative_counts_ranks_labels.append((-count, day07part02_label2rank[label], label))

  if len(negative_counts_ranks_labels) == 0:
    return {'A': 5}

  sorted_negative_counts_ranks_labels = sorted(negative_counts_ranks_labels)

  _, _, best_label_to_reassign = sorted_negative_counts_ranks_labels[0]
  label2count = {label: -negative_count for negative_count, _, label in sorted_negative_counts_ranks_labels}
  label2count[best_label_to_reassign] += raw_label2count['J']
  return label2count


def day07part02_hand2type(hand):
  raw_label2count = {}
  for label in hand:
    if label in raw_label2count:
      raw_label2count[label] += 1
    else:
      raw_label2count[label] = 1

  label2count = day07part02_reassign_jokers(raw_label2count)

  if len(label2count) == 1 and 5 in label2count.values():
    return 'Five of a kind'
  elif len(label2count) == 2 and 4 in label2count.values():
    return 'Four of a kind'
  elif len(label2count) == 2 and 3 in label2count.values() and 2 in label2count.values():
    return 'Full house'
  elif len(label2count) == 3 and 3 in label2count.values():
    return 'Three of a kind'
  elif len(label2count) == 3 and 2 in label2count.values() and 1 in label2count.values():
    return 'Two pair'
  elif len(label2count) == 4 and 2 in label2count.values():
    return 'One pair'
  elif len(label2count) == 5 and 1 in label2count.values():
    return 'High card'

  return None


def day07part02_handlt(a, b):
  a_type = day07part02_hand2type(a)
  b_type = day07part02_hand2type(b)
  a_typerank = day07part02_type2rank[a_type]
  b_typerank = day07part02_type2rank[b_type]
  if a_typerank < b_typerank:
    return True
  elif a_typerank > b_typerank:
    return False
  else:
    for i in range(len(a)):
      if day07part02_label2rank[a[i]] < day07part02_label2rank[b[i]]:
        return True
      elif day07part02_label2rank[a[i]] > day07part02_label2rank[b[i]]:
        return False
      else:
        continue
  return False


def day07part02_handkey(hand):
  handtype = day07part02_hand2type(hand)
  typerank = day07part02_type2rank[handtype]
  cardranks = tuple(day07part02_label2rank[label] for label in hand)
  return (typerank, cardranks)

def day07part02(puzzle_input, _):
  hands_bids = []
  for line in puzzle_input.splitlines():
    hand, bidstr = line.split()
    bid = int(bidstr)
    hands_bids.append((hand, bid))
  sorted_hands_bids = sorted(hands_bids, key=lambda x: day07part02_handkey(x[0]))
  total_winnings = 0
  for rank, (hand, bid) in zip(range(len(sorted_hands_bids), -1, -1), sorted_hands_bids):
    print(rank, hand, bid)
    total_winnings += rank * bid
  print(total_winnings)


def day08part01(puzzle_input, _):
  lines = puzzle_input.splitlines()
  directions = lines[0].strip()
  nodere = re.compile('^(?P<node>[A-Z]+)\s+=\s+\((?P<left>[A-Z]+),\s+(?P<right>[A-Z]+)\)$')
  node2leftright = {}
  for line in lines[1:]:
    match = nodere.match(line)
    if match is not None:
      node = match.groupdict()['node']
      left = match.groupdict()['left']
      right = match.groupdict()['right']
      node2leftright[node] = (left, right)
  pprint.pprint(node2leftright)

  current_node = 'AAA'
  stepcount = 0
  for direction in itertools.cycle(directions):
    if current_node == 'ZZZ':
      break
    leftright = node2leftright[current_node]
    if direction == 'L':
      current_node = leftright[0]
    elif direction == 'R':
      current_node = leftright[1]
    else:
      print('unknown direction', direction)
      return
    stepcount += 1

  print(stepcount)


def day08part02(puzzle_input, _):
  lines = puzzle_input.splitlines()
  directions = lines[0].strip()
  nodere = re.compile('^(?P<node>[0-9A-Z]+)\s+=\s+\((?P<left>[0-9A-Z]+),\s+(?P<right>[0-9A-Z]+)\)$')
  node2leftright = {}
  for line in lines[1:]:
    match = nodere.match(line)
    if match is not None:
      node = match.groupdict()['node']
      left = match.groupdict()['left']
      right = match.groupdict()['right']
      node2leftright[node] = (left, right)
  pprint.pprint(node2leftright)

  startingnodes = tuple(node for node in node2leftright.keys() if node.endswith('A'))

  pprint.pprint(startingnodes)
  startingnode2z_stepcount_node = {}
  currentnodes = startingnodes
  stepcount = 0
  for direction in itertools.cycle(directions):
    if len(startingnode2z_stepcount_node) == len(startingnodes):
      break

    nextnodes = []
    for i, currentnode in enumerate(currentnodes):
      if currentnode.endswith('Z'):
        startingnode = startingnodes[i]
        if startingnode in startingnode2z_stepcount_node:
          startingnode2z_stepcount_node[startingnode].append((stepcount, currentnode))
        else:
          startingnode2z_stepcount_node[startingnode] = [(stepcount, currentnode)]
      leftright = node2leftright[currentnode]
      if direction == 'L':
        nextnodes.append(leftright[0])
      elif direction == 'R':
        nextnodes.append(leftright[1])
      else:
        print('unknown direction', direction)
        return
    stepcount += 1
    currentnodes = tuple(nextnodes)
    if stepcount % 100000 == 0:
      print(stepcount)
      pprint.pprint(currentnodes)

  pprint.pprint(startingnode2z_stepcount_node)
  first_stepcounts = []
  for stepcounts_nodes in startingnode2z_stepcount_node.values():
    first_stepcount, first_z_node = stepcounts_nodes[0]
    first_stepcounts.append(first_stepcount)
  print(math.lcm(*first_stepcounts))


def day09part01_find_diffs(seq):
  diffs = []
  for a, b in zip(seq, seq[1:]):
    diffs.append(b - a)
  return tuple(diffs)


def day09part01(puzzle_input, _):
  histories=[]
  for line in puzzle_input.splitlines():
    histories.append(tuple(map(int, line.split())))

  pyramids = []
  for history in histories:
    pyramid = [history]
    diffs = day09part01_find_diffs(history)
    pyramid.append(diffs)
    while set(diffs) != {0}:
      diffs = day09part01_find_diffs(diffs)
      pyramid.append(diffs)
    pyramids.append(pyramid)


  completions=[]
  for pyramid in pyramids:
    current_completion = 0
    for i in range(len(pyramid) - 2, -1, -1):
      current_completion += pyramid[i][-1]
    completions.append(current_completion)


  print(sum(completions))


def main():
    day2function = {
        1: (day01, day01),
        2: (day02, day02),
        3: (day03, day03part02),
        4: (day04part01, day04part02),
        5: (day05part01, day05part02),
        6: (day06part01, day06part02),
        7: (day07part01, day07part02),
        8: (day08part01, day08part02),
        9: (day09part01,),
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int)
    parser.add_argument('part', type=int)
    parser.add_argument('filename')
    parser.add_argument('--extra', type=json.loads)
    args = parser.parse_args()
    function = day2function[args.day][args.part - 1]
    with open(args.filename) as f:
        puzzle_input = f.read()
    function(puzzle_input, args.extra)


if __name__ == '__main__':
    main()
