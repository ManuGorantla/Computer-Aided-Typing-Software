"Utility functions for file and string manipulation"

import string
from math import sqrt



def lines_from_file(path):
    """Return a list of strings, one for each line in a file."""
    with open(path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def remove_punctuation(s):
    """Return a string with the same contents as s, but with punctuation removed.
    """
    punctuation_remover = str.maketrans('', '', string.punctuation)
    return s.strip().translate(punctuation_remover)

def lower(s):
    """Return a lowercased version of s.

    """
    return s.lower()

def split(s):
    """Return a list of words contained in s, which are sequences of characters
    separated by whitespace (spaces, tabs, etc.).

    """
    return s.split()



KEY_LAYOUT = [["1","2","3","4","5","6","7","8","9","0","-","="],
              ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p","[","]"],
              ["a", "s", "d", "f", "g", "h", "j", "k", "l",";","'"],
              ["z", "x", "c", "v", "b", "n", "m",",",".","/"],
              [" "]]

def distance(p1, p2):
    """Return the Euclidean distance between two points

   
    """
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_key_distances():
    """Return a new dictionary mapping key pairs to distances.

    """
    key_distance = {}

    def compute_pairwise_distances(i, j, d):
        for x in range(len(KEY_LAYOUT)):
            for y in range(len(KEY_LAYOUT[x])):
                l1 = KEY_LAYOUT[i][j]
                l2 = KEY_LAYOUT[x][y]
                d[l1, l2] = distance((i, j), (x, y))

    for i in range(len(KEY_LAYOUT)):
        for j in range(len(KEY_LAYOUT[i])):
            compute_pairwise_distances(i, j, key_distance)

    max_value = max(key_distance.values())
    return {key : value * 8 / max_value for key, value in key_distance.items()}

def count(f):
    """Keeps track of the number of times a function f is called using the
    variable call_count

    """
    def counted(*args):
        counted.call_count += 1
        return f(*args)
    counted.call_count = 0
    return counted

def deep_convert_to_tuple(sequence):
    """Deeply converts tuples to lists.
   
    """
    if isinstance(sequence, list) or isinstance(sequence, tuple):
        return tuple(deep_convert_to_tuple(item) for item in sequence)
    else:
        return sequence
