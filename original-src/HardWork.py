import re

def load_words(filename):
    '''Returns a list containing every word in `filename`.'''
    word_list = []
    with open(filename, 'r') as f:
        for line in f:
            word_list.extend(line.split(' '))
    return word_list

def clean_words(words):
    '''Returns a list containing only words and all lowercased.'''

    clean_list = []
    for word in words:
        match = re.search('[a-z]+', word, re.IGNORECASE)
        if match:
            clean_list.append(match.group(0).lower())

    return clean_list

def count_words(words):
    '''Returns a dictionary mapping each word to the number of times
    it appears.'''
    word_count = {}
    for word in words:
        c = word_count.get(word, 0)
        word_count[word] = c + 1

    return word_count

def get_most_common(word_count, n=10):
    '''Returns the `n` most common words based on the count.'''
    return [i[0] for i in sorted(word_count.items(), key=lambda i: i[1], reverse=True)][:n]
