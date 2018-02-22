import sys
import os
import nltk
import re
import numpy as np
from scipy.spatial.distance import cosine
from scipy import stats
from gensim import models


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


if __name__ == "__main__":
    os.environ['PYTHONHASHSEED'] = '1'
    use_local_file = False
    if use_local_file:
        if 'hw7' in os.listdir():
            os.chdir('hw7')
        window = 2
        judgment_filename = "mc_similarity.txt"
        output_filename = "hw7_sim_" + str(window) + "_" + "CBOW" + "_output.txt"
    else:
        window = int(sys.argv[1])
        judgment_filename = sys.argv[2]
        output_filename = sys.argv[3]

    # Read word pairs
    print('Reading word pairs...')
    pairs = read_word_pairs(judgment_filename)

    # brown_words = list(nltk.corpus.brown.words())[0:22079]
    print('Reading corpus...')
    sentences = list(nltk.corpus.brown.sents())
    # sentences = list(nltk.corpus.brown.words())

    # First, remove all punctuations
    print('Removing punctuations...')
    sentences, word_set = remove_puncs(sentences)
    # words = remove_puncs(brown_words)

    model = models.Word2Vec(sentences, min_count=0, workers=4, window=window, size=100, seed=1)

    print('start calculating')
    cos_sims = []
    golden = []
    out_f = open(output_filename, 'w')
    for word1, word2, sim in pairs:
        v1 = model.wv[word1]
        v2 = model.wv[word2]
        wv_sim = 1 - cosine(v1, v2)
        cos_sims.append(float(wv_sim))
        golden.append(float(sim))
        out_str1 = word1 + ',' + word2 + ':' + str(wv_sim) + '\n'
        out_f.write(out_str1)
    res = stats.spearmanr(cos_sims, golden)
    out_str2 = 'Correlation:' + str(res[0]) + '\n'
    out_f.write(out_str2)
    print(res)
    out_f.close()
