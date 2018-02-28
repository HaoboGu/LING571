import sys
import os
import numpy as np
from scipy.stats import spearmanr
from nltk.corpus import *
from nltk.corpus.reader.wordnet import information_content
from collections import Counter
from operator import itemgetter


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


def resnik(word1, word2, ic_data):
    """
    Calculate resnik similarity between word1 and word2 using information content data.
    Resnik similarity = max of [ic(s) for s in subsumers(word1, word2)]
    :param word1:
    :param word2:
    :param ic_data:
    :return:
    """
    resnik_sim = 0
    best_sense = ''
    for syn_sense_probe in wordnet.synsets(word1):
        for syn_sense_noun in wordnet.synsets(word2):
            syn_word1 = wordnet.synset(syn_sense_probe.name())  # get synnet for word1
            syn_word2 = wordnet.synset(syn_sense_noun.name())  # get synnet for word2
            subsumers = syn_word1.common_hypernyms(syn_word2)  # get all subsumers
            ic = 0
            if len(subsumers) > 0:
                # If there exists subsumers for probe and noun
                for s in subsumers:
                    ic = information_content(s, ic_data) if information_content(s, ic_data) > ic else ic
            if ic > resnik_sim:
                # If current information content is better
                resnik_sim = ic
                best_sense = syn_word1
    return resnik_sim, best_sense


def resnik_wsd(data, ic_data, output_file, judgment_file):
    """
    Main part of this hw
    :param data: test data
    :param ic_data: information content data
    :param output_file: output filename
    :param judgment_file: human judgment filename
    :return:
    """
    with open(output_file, 'w') as of:
        # For probe word and noun group pairs in wsd context file
        for probe, noun_group in data:
            out_s = ''
            sense_list = []
            for noun in noun_group:
                resnik_sim, best_sense = resnik(probe, noun, ic_data)
                out_s = out_s + '(' + probe + ', ' + noun + ', ' + str(resnik_sim) + ')' + ' '
                if not isinstance(best_sense, str):  # if no common subsumers for probe and noun
                    sense_list.append(best_sense)
            # print(Counter(sense_list))
            sorted_sense = sorted(Counter(sense_list).items(), key=itemgetter(1), reverse=True)
            # Write to file
            of.write((out_s.strip(' ')+'\n'))
            of.write((sorted_sense[0][0].name()+'\n'))

        # For word pairs in human judgment file
        pairs = read_word_pairs(judgment_file)
        resnik_sim_list, gold = [], []
        for word1, word2, sim in pairs:
            resnik_sim, best_sense = resnik(word1, word2, ic_data)
            resnik_sim_list.append(resnik_sim)
            gold.append(float(sim))
            out_s = word1 + ',' + word2 + ':' + str(resnik_sim) + '\n'
            of.write(out_s)
        correlation = spearmanr(gold, resnik_sim_list)[0]
        out_s = 'Correlation:' + str(correlation) + '\n'
        of.write(out_s)


if __name__ == "__main__":
    use_local_file = False
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

    if information_file_type == 'nltk':
        wnic = wordnet_ic.ic('ic-brown-resnik-add1.dat')
    else:
        print('Do not have other information content file, use nltk instead')
        wnic = wordnet_ic.ic('ic-brown-resnik-add1.dat')

    test_data = read_wsd_test_file(wsd_test_filename)

    resnik_wsd(test_data, wnic, output_filename, judgment_filename)