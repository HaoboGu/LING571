import sys
import os
import nltk
import re
import numpy as np
from scipy.stats import spearmanr
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
def remove_puncs(raw_sentences):
    """
    Remove all punctuations in the raw data, including punctuations in the word
    :param raw_sentences: List[List[str]]
    :return: List[List[str]]
    """
    sentences_without_puncs = []
    all_words = set()
    puncs = set()
    for raw_sent in raw_sentences:
        sent_without_punc = []
        for raw_w in raw_sent:
            if not re.search('^\W+$', raw_w):
                sent_without_punc.append(raw_w.lower())
                all_words.add(raw_w.lower())
            else:
                puncs.add(raw_w)
        sentences_without_puncs.append(sent_without_punc)

    return sentences_without_puncs, all_words


def initialize_feature_dict(all_words):
    """
    Initialize feature dictionary, based on words in word set
    :param all_words:
    :return: dictionary of features
    """
    temp = {}
    for w in all_words:
        temp[w] = 0
    return temp


def read_word_pairs(filename):
    """
    Read word pairs from given file. Each line is of the form: wd1,wd2,similarity_score
    :param filename:
    :return: [wd1, wd2, similarity]
    """
    word_pairs = []
    with open(filename, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            word_pairs.append(line.split(','))
            line = f.readline().strip('\n')
    return np.array(word_pairs, dtype=str)


def read_wsd_test_file(filename):
    """
    Read word sense disambiguation test data.
    :param filename: str
    :return: list[(probe word, noun group)]
    """
    wsd_test = []
    with open(filename, 'r') as wsd_test_file:
        line = wsd_test_file.readline().strip('\n')

        while line:
            line = re.sub('\s+', ' ', line)
            probe_word, noun_group = line.split(' ')[0], line.split(' ')[1]
            noun_group = noun_group.split(',')
            wsd_test.append((probe_word, noun_group))
            line = wsd_test_file.readline().strip('\n')

    return wsd_test

if __name__ == "__main__":
    use_local_file = True
    if use_local_file:
        if 'hw8' in os.listdir():
            os.chdir('hw8')
        information_file_type = "nltk"
        wsd_test_filename = "wsd_contexts.txt"
        judgment_filename = "mc_similarity.txt"
        output_filename = "hw8_output.txt"
    else:
        information_file_type = sys.argv[1]
        wsd_test_filename = sys.argv[2]
        judgment_filename = sys.argv[3]
        output_filename = sys.argv[4]
    # # Read word pairs
    # print('Reading word pairs...')
    # pairs = read_word_pairs(judgment_filename)
    #
    # # brown_words = list(nltk.corpus.brown.words())[0:22079]
    # print('Reading corpus...')
    # sentences = list(nltk.corpus.brown.sents())
    # # sentences = list(nltk.corpus.brown.words())
    #
    # wnic = wordnet_ic.ic('ic-brown-resnik-add1.dat')

    test_data = read_wsd_test_file(wsd_test_filename)
