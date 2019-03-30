import re

def charrange(a, b):
    return [chr(x) for x in range(ord(a), ord(b) + 1)]
    

def padder(text, length, padder='a'):
    return text + (padder * (length - len(text)))


def parse_wrong_position(msg):
    return int(re.match('Wrong password at position (.*)', msg)[1])

def print1(msg):
    print(f'\r{msg}', end='')


def print2(msg):
    print(f'\n\r{msg}\n', end='')
