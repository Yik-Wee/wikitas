"""
Functions to get similarity of words
and list of words & related wordsfrom string
"""
from typing import List, Optional
from nltk.corpus import wordnet
from .wikiapi import get_categories


def similarity(words_1: List[str], words_2: List[str]) -> float:
    """
    Finds the average Wu-Palmer similarity between 2 lists of words

    Parameters:
    ----------
    `words_1`: List[str]
        List of words to match against `words_2`
    `words_2`: List[str]
        List of words to match against `words_1`

    Returns:
    -------
    Average similarity of all words from `words_1` and `words_2`
    """
    total_sim = 0
    total_comparisons = 0

    # Compare each word in `words_1` with each word in `word_2`
    # Skip word if it doesn't exist in wordnet db
    for w_1 in words_1:
        syn_1 = wordnet.synsets(w_1)
        if not syn_1:  # Word `w_1` not in wordnet db
            continue

        for w_2 in words_2:
            syn_2 = wordnet.synsets(w_2)
            if not syn_2:  # Word `w_2` not in wordnet db
                continue

            sim = syn_2[0].wup_similarity(syn_1[0])
            total_sim += sim
            total_comparisons += 1  # Increment total no. of comparisons made

    # No words were compared (no words existed in wordnet db)
    if total_comparisons == 0:
        return 0

    return total_sim / total_comparisons  # return average similarity


def get_words(title: str) -> List[str]:
    """
    Get the list of words from a string (e.g. sentence, phrase, etc.)

    Parameters:
    ----------
    `title`: str
        The string to split into words (sentence, phrase, etc.)

    Returns:
    -------
    List of words from string
    """
    buffer = []
    word_buffer = ""
    for char in title:
        if char.isalpha():
            word_buffer += char
        elif word_buffer:
            buffer.append(word_buffer)
            word_buffer = ""

    if word_buffer:
        buffer.append(word_buffer)
    return buffer


def get_words_with_categories(
    title: str,
    similarity_threshold: Optional[float] = 0.4
) -> List[str]:
    """
    Get list of words from string (e.g. sentence, phrase, etc.) including words
    from `title`'s wikipedia categories

    Parameters:
    ----------
    `title`: str
        The title of the wikipedia page (or sentence, phrase, etc.) to split
        into words (including words from it's wikipedia cateories)
    `similarity_threshold`: Optional[float]
        0 <= similarity_threshold <= 1
        Words from the wikipedia categories of `title` with a similarity
        above this threshold will be added to the list
    """
    initial_words = get_words(title)

    # Get set of words in title existing in wordnet db
    words = {word for word in initial_words if wordnet.synsets(word)}
    categories = get_categories(title)

    if not words:  # Initial words were invalid
        for cat in categories:
            cat_words = get_words(cat.replace("Category:", ""))
            for word in cat_words:
                # Words beginning with lowercase are usually unimportant
                # e.g. in, with, based, etc.
                if word[0].isupper() and word.lower() != "articles" and wordnet.synsets(word):
                    words.add(word)

        return list(words)  # Top 5 relevant category words

    for cat in categories:
        cat_words = get_words(cat.replace("Category:", ""))
        for word in cat_words:
            sim = similarity([word], initial_words)
            if sim >= similarity_threshold:
                words.add(word)

    return list(words)
