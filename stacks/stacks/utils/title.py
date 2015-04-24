# utils.title
# Helpers for modifying book title strings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 20:50:28 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: title.py [] benjamin@bengfort.com $

"""
Helpers for modifying book title strings
"""

##########################################################################
## Helper functions
##########################################################################


def capitalize(word):
    """
    Checks if a hyphen is in the word, and if so, capitalizes every
    word in the hyphen. Otherwise, returns the standard capitalize.
    """
    if '-' in word:
        words = word.split('-')
        words = [w.capitalize() for w in words]
        return '-'.join(words)
    return word.capitalize()


def title_case(string):
    """
    Capitalize the first and last word of the string, and every other
    word in the string, EXCEPT those that are listed in the articles.
    """
    articles = [
        "the", "a", "an", "of", "at", "on", "to",
        "over", "and", "but", "or", "nor"
    ]

    words = string.split(' ')
    for i, word in enumerate(words):
        # First word and last word should be capitalized.
        if i == 0 or i == len(words) - 1:
            word = word.capitalize()
        else:
            # Check for acronyms.
            if word.isupper():
                continue
            else:
                word = word.lower()

            if word not in articles:
                word = capitalize(word)
        words[i] = word
    return ' '.join(words)


def make_title(t):
    articles = ["The", "A", "An", "Of", "At", "On"]

    # Make words uppercase and remove extra whitespace
    t = t.strip()
    t = title_case(t)

    # Replace any html entities
    t = t.replace('&Amp;', '&')
    t = t.replace('&amp;', '&')

    # Check if comma appended article:
    tgrp = t.split(',')
    if tgrp[-1].strip() in articles:
        tgrp.insert(0, tgrp.pop())
        t = "%s %s" % (tgrp[0].strip(), ','.join(tgrp[1:]))

    return t
