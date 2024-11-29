import fileinput
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

if __name__ == '__main__':
    day01(sys.argv[1])
