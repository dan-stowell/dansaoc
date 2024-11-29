import fileinput
import functools
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


def day01(filename):
  calibrationvaluesum = 0
  calibrationvalues = []
  for line in fileinput.input(files=(filename, )):
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

import fileinput
import functools
import operator
import pprint
import re


def load_cubesets(filename):
  gameidre = re.compile("^Game\s+(?P<gameid>\d+):\s+(?P<cubesets>.+)$")
  cubere = re.compile('\s*(?P<cubecount>\d+)\s+(?P<cubecolor>red|blue|green)')
  gameid2cubesets = {}
  for line in fileinput.input(files=(filename, )):
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


def day02(filename, bag_contents):
  gameid2cubesets = load_cubesets(filename)
  powersum = 0
  for gameid, cubesets in gameid2cubesets.items():
    fewest_cubes = find_fewest_cubes(cubesets)
    pprint.pprint(fewest_cubes)
    cubeset_power = functools.reduce(operator.mul, fewest_cubes.values())
    powersum += cubeset_power
  print(powersum)
  # possible_gameids = find_possible_gameids(gameid2cubesets, bag_contents)

if __name__ == '__main__':
    day2function = {
        1: day01,
        2: lambda f: day02(f, {'red': 12, 'green': 13, 'blue': 14})
    }
    day = int(sys.argv[1].strip())
    filename = sys.argv[2]
    function = day2function[day]
    function(filename)
