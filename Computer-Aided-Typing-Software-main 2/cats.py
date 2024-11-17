"""Typing test implementation"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random





def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which the SELECT returns True.
    If there are fewer than K such paragraphs, return an empty string.
    """
    paragraphList = []

    for x in range(len(paragraphs)):
        if select(paragraphs[x]):
            paragraphList.append(paragraphs[x])
    
    if k > len(paragraphList) - 1:
        return ''
    else:
        return paragraphList[k]


def about(subject):
    """Return a function that takes in a paragraph and returns whether
    that paragraph contains one of the words in SUBJECT.

    """
    assert all([lower(x) == x for x in subject]), "subjects should be lowercase."



    def inPara(paragraph):
        newParagraph = remove_punctuation(paragraph)
        lowerPara = lower(newParagraph)
        finalPara = split(lowerPara)
        for x in range(len(finalPara)):
            for y in range(len(subject)):
                if finalPara[x] == subject[y]:
                    return True

        return False

    return inPara


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    compared to the corresponding words in SOURCE.
    """
    typed_words = split(typed)
    source_words = split(source)
    if len(typed_words) == 0:
        typed_words.append("")
    if len(source_words) == 0:
        source_words.append("")
    
    correct = 0

    for x in range(min(len(source_words), len(typed_words))):
        if typed_words[x] == source_words[x]:
            correct += 1
        
    return (correct/(len(typed_words)))*100.0


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.
    """
    assert elapsed > 0, "Elapsed time must be positive"
    return (len(typed))/5/(elapsed/60)





def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD based on DIFF_FUNCTION. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, return TYPED_WORD instead.
    """
    dif = lambda word: diff_function(typed_word, word, limit)
    minDiff = min(word_list, key = dif)

    if diff_function(typed_word, minDiff, limit) > limit or (typed_word in word_list):
        return typed_word
    
    return minDiff


def furry_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.
    """
    if limit == -1:
        return 33333333333
    if (len(typed)) == 0 or len(source) == 0:
        return abs((len(typed)) - len(source))    
    if typed[0] != source[0]:
        return 1 + furry_fixes(typed[1:], source[1:], limit - 1)
    else:
        return furry_fixes(typed[1:], source[1:], limit)
   


def minimum_mewtations(typed, source, limit):
    """A diff function for autocorrect that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    """
    if limit == -1:
        return 3333333333
    if (len(typed)) == 0 or len(source) == 0:
        return abs((len(typed)) - len(source))
    
    val = 3333333333
    
    if typed[0] == source[0]:
        val = minimum_mewtations(typed[1:], source[1:], limit)
    
    add = 1 + minimum_mewtations(typed, source[1:], limit - 1)
    rem = 1 + minimum_mewtations(typed[1:], source, limit - 1)
    sub = 1 + minimum_mewtations(typed[1:], source[1:], limit - 1)

    return min(add, rem, sub, val)
        


minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, "Remove this line to use your final_diff function."


FINAL_DIFF_LIMIT = 6 



def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.
    """
    correct = 0

    for x in range(len(typed)):
        if typed[x] == source[x]:
            correct += 1
        else:
            break

    val = (correct/len(source))
    
    upload({"id": user_id, "progress": val})
    
    return val


def time_per_word(words, timestamps_per_player):
    """Return a dictionary {'words': words, 'times': times} where times
    is a list of lists that stores the durations it took each player to type
    each word in words.
    """
    tpp = timestamps_per_player 
    times = []

    for x in timestamps_per_player:
        vals = []

        for y in range(len(x) - 1):
            vals.append(x[y + 1] - x[y])
        
        times.append(vals)
    return {'words': words, 'times': times}


def fastest_words(words_and_times):
    """Return a list of lists indicating which words each player typed fastests.
    """
    check_words_and_times(words_and_times)  
    words, times = words_and_times['words'], words_and_times['times']
    player_indices = range(len(times)) 
    word_indices = range(len(words)) 
    vals = [[] for x in player_indices]

    for y in word_indices:
        topA = -1
        topB = 33333333333

        for z in player_indices:
            i = get_time(times, z, y)

            if (i < topB):
                topA = z
                topB = i  

        vals[topA].append(words[y])

    return vals


def check_words_and_times(words_and_times):
    """Check that words_and_times is a {'words': words, 'times': times} dictionary
    in which each element of times is a list of numbers the same length as words.
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """Return the time it took player_num to type the word at word_index,
    given a list of lists of times returned by time_per_word."""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = False  



def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
