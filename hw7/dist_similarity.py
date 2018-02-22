import sys
import os
import nltk
import re
import numpy as np
from operator import itemgetter
from scipy.spatial.distance import cosine
from scipy import stats
from math import log2


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


def word_sim(output_filename, pairs, sentences, word_set, weight="FREQ"):
    cos_sims = []
    golden = []
    out_f = open(output_filename, 'w')

    if weight == 'FREQ':
        for word1, word2, sim in pairs:
            feature1 = initialize_feature_dict(word_set)
            feature2 = initialize_feature_dict(word_set)
            for sent in sentences:
                sent = np.array(sent).astype(str)
                n_words = len(sent)
                for word_index in np.where(sent == word1)[0]:

                    for offset in range(1, window + 1):  # offset: 1 ~ window
                        if word_index - offset >= 0:
                            feature1[sent[word_index - offset]] += 1
                        if word_index + offset < n_words:
                            feature1[sent[word_index + offset]] += 1

                for word_index in np.where(sent == word2)[0]:
                    for offset in range(1, window + 1):  # offset: 1 ~ window
                        if word_index - offset >= 0:
                            feature2[sent[word_index - offset]] += 1
                        if word_index + offset < n_words:
                            feature2[sent[word_index + offset]] += 1

            m1 = sorted(feature1.items(), key=itemgetter(0), reverse=False)
            m2 = sorted(feature2.items(), key=itemgetter(0), reverse=False)
            v1 = list(map(list, zip(*m1)))
            v2 = list(map(list, zip(*m2)))
            cos_sim = 1 - cosine(list(v1[1]), list(v2[1]))  # 1 - cosine distance

            m1 = sorted(feature1.items(), key=itemgetter(1), reverse=True)
            m2 = sorted(feature2.items(), key=itemgetter(1), reverse=True)
            out_str1 = word1
            out_str2 = word2
            for i in range(0, 10):
                out_str1 = out_str1 + ' ' + m1[i][0] + ':' + str(m1[i][1])
                out_str2 = out_str2 + ' ' + m2[i][0] + ':' + str(m2[i][1])
            out_str1 = out_str1 + '\n'
            out_str2 = out_str2 + '\n'
            out_f.write(out_str1)
            out_f.write(out_str2)
            cos_sims.append(cos_sim.__float__())
            golden.append(float(sim))
            out_str3 = word1 + ',' + word2 + ':' + str(cos_sim) + '\n'
            out_f.write(out_str3)
        res = stats.spearmanr(cos_sims, golden)
        out_str4 = 'Correlation:'+str(res[0])
        out_f.write(out_str4)
    else:
        # PMI
        count = initialize_feature_dict(word_set)
        for sent in sentences:
            for word in sent:
                count[word] += 1
        multiplier = sum(count.values())

        for word1, word2, sim in pairs:
            # To calculate PMI, find all co-occurrences first
            feature1 = initialize_feature_dict(word_set)
            feature2 = initialize_feature_dict(word_set)
            word_in_window1 = set()
            word_in_window2 = set()
            for sent in sentences:
                sent = np.array(sent).astype(str)
                n_words = len(sent)
                for word_index in np.where(sent == word1)[0]:
                    for offset in range(1, window + 1):  # offset: 1 ~ window
                        if word_index - offset >= 0:
                            feature1[sent[word_index - offset]] += 1
                            word_in_window1.add(sent[word_index - offset])
                        if word_index + offset < n_words:
                            feature1[sent[word_index + offset]] += 1
                            word_in_window1.add(sent[word_index + offset])
                for word_index in np.where(sent == word2)[0]:
                    for offset in range(1, window + 1):  # offset: 1 ~ window
                        if word_index - offset >= 0:
                            feature2[sent[word_index - offset]] += 1
                            word_in_window2.add(sent[word_index - offset])
                        if word_index + offset < n_words:
                            feature2[sent[word_index + offset]] += 1
                            word_in_window2.add(sent[word_index + offset])
            for word in word_in_window1:
                # PMI = co-occurrence(wd1, wd2) * # of words / (count(wd1) * count(wd2))
                pmi1 = feature1[word] * multiplier / (count[word1] * count[word])
                feature1[word] = max(log2(pmi1), 0)
            for word in word_in_window2:
                pmi2 = feature2[word] * multiplier / (count[word2] * count[word])
                feature2[word] = max(log2(pmi2), 0)
            m1 = sorted(feature1.items(), key=itemgetter(0), reverse=False)
            m2 = sorted(feature2.items(), key=itemgetter(0), reverse=False)
            v1 = list(map(list, zip(*m1)))
            v2 = list(map(list, zip(*m2)))
            cos_sim = 1 - cosine(list(v1[1]), list(v2[1]))  # 1 - cosine distance

            m1 = sorted(feature1.items(), key=itemgetter(1), reverse=True)
            m2 = sorted(feature2.items(), key=itemgetter(1), reverse=True)
            out_str1 = word1
            out_str2 = word2
            for i in range(0, 10):
                out_str1 = out_str1 + ' ' + m1[i][0] + ':' + str(m1[i][1])
                out_str2 = out_str2 + ' ' + m2[i][0] + ':' + str(m2[i][1])
            out_str1 = out_str1 + '\n'
            out_str2 = out_str2 + '\n'
            out_f.write(out_str1)
            out_f.write(out_str2)
            cos_sims.append(cos_sim.__float__())
            golden.append(float(sim))
            out_str3 = word1 + ',' + word2 + ':' + str(cos_sim) + '\n'
            out_f.write(out_str3)
        res = stats.spearmanr(cos_sims, golden, 0)
        out_str4 = 'Correlation:'+str(res[0])
        out_f.write(out_str4)
    out_f.close()


if __name__ == "__main__":
    use_local_file = False
    if use_local_file:
        if 'hw7' in os.listdir():
            os.chdir('hw7')
        window = 2
        weighting = "FREQ"
        # weighting = "PMI"
        judgment_filename = "mc_similarity.txt"
        output_filename = "hw7_sim_" + str(window) + "_" + weighting + "_output.txt"
    else:
        window = sys.argv[1]
        weighting = sys.argv[2]
        if weighting != "FREQ" or weighting != "PMI":
            print("Error: weighting must be FREQ or PMI")
        # weighting = "PMI"
        judgment_filename = sys.argv[3]
        output_filename = sys.argv[4]

    # Read word pairs
    print('Reading word pairs...')
    word_pairs = read_word_pairs(judgment_filename)

    print('Reading corpus...')
    brown_sentences = list(nltk.corpus.brown.sents())

    # First, remove all punctuations
    print('Removing punctuations...')
    brown_sentences, words = remove_puncs(brown_sentences)

    # Calculate similarity
    word_sim(output_filename, word_pairs, brown_sentences, words, weighting)

