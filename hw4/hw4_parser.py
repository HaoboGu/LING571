import nltk
import sys
import os
import numpy as np
from nltk.tree import ProbabilisticTree
import re
import time


def create_map(productions):
    """
    Create a dictionary mapping symbols on RHS to a set of symbols on LHS based on grammar
    :param productions: production list
    :return: a dictionary {tuple(symbols):set((LHS symbols, prob))}
    """
    dict = {}
    for pr in productions:
        rhs = pr.rhs()  # tuple of symbols on the right hand
        if rhs not in dict:  # if the symbol is visited for the first time
            dict[rhs] = set()
        dict[rhs].add((pr.lhs(), pr.prob()))  # Add non-terminal on the left to the set

    return dict


def initialize_table(n_dimension):
    """
    Initialize a n_dimension*n_dimension table using empty lists and return it
    """
    table = np.zeros((n_dimension, n_dimension), dtype=object)
    for i in range(n_dimension):
        for j in range(n_dimension):
            table[i][j] = []
    return table


def update_cell(table, i, k, j, symbol_map):
    """
    For current cell [i,j], update tree list and probability based on cell [i,k] and [k,j]
    :return: updated table
    """
    for s1 in table[i, k]:
        for s2 in table[k, j]:  # s1 and s2 are trees
            rhs = (s1.label(), s2.label())
            if rhs in symbol_map:  # check if rhs in current grammar's rules
                lhs = symbol_map[rhs]
                # max_prob = -1
                # best_symbol_prob = None
                for l_symbol_prob in lhs:
                    # add current tree to cell [i,j]
                    table[i, j].append(
                        ProbabilisticTree(l_symbol_prob[0], [s1, s2], prob=l_symbol_prob[1] * s1.prob() * s2.prob()))
                #     if s1.prob() * s2.prob() * l_symbol_prob[1] > max_prob:
                #         max_prob = s1.prob() * s2.prob() * l_symbol_prob[1]
                #         best_symbol_prob = l_symbol_prob
                #
                # table[i, j].append(ProbabilisticTree(best_symbol_prob[0], [s1, s2], prob=max_prob))
    return table


def pcky(sentence, pcfg):
    """
    Probabilistic CKY algorithm.
    :param sentence: List[str]
    :param pcfg: nltk.PCFG
    :return: parsed result
    """
    p_rules = pcfg.productions()
    symbol_map = create_map(p_rules)  # map RHS to a set of LHS according to the grammar
    d = len(sentence)  # d is the length of the sentence
    table = initialize_table(d + 1)  # initialize table for pcky
    for j in range(1, len(sentence)+1):
        j_tuple = tuple([sentence[j-1]])
        if j_tuple in symbol_map:
            for symbol_prob in symbol_map[j_tuple]:  # for all terminals
                table[j - 1][j].append(ProbabilisticTree(symbol_prob[0], [sentence[j-1]], prob=symbol_prob[1]))
        for i in range(j - 2, -1, -1):  # from j-2 to 0
            for k in range(i + 1, j):  # from i+1 to j-1
                table = update_cell(table, i, k, j, symbol_map)
    return table


if __name__ == "__main__":
    s = time.time()
    use_local_file = False
    if use_local_file:
        if 'hw4' in os.listdir():
            os.chdir('hw4')
        input_pcfg_filename = 'hw4_trained.pcfg'
        sentences_filename = 'data/sentences.txt'
        output_parses_filename = "parses_base.out"
    else:
        input_pcfg_filename = sys.argv[1]
        sentences_filename = sys.argv[2]
        output_parses_filename = sys.argv[3]

    prob_cfg = nltk.data.load(input_pcfg_filename, format='pcfg')  # read pcfg grammar
    start_symbol = prob_cfg.start()  # get start symbol
    sents_file = open(sentences_filename)  # sentence file
    line = sents_file.readline()
    output_file = open(output_parses_filename, 'w')  # output file

    while line:
        word_seq = nltk.word_tokenize(line)  # word sequence
        words_table = pcky(word_seq, prob_cfg)  # run pcky algorithm
        trees = words_table[0][words_table.shape[1] - 1]  # get parse results
        # Write parses
        if len(trees) == 0:  # no parse tree
            # print('no parse tree')
            output_file.write('\n')
        else:
            # Get best parse first
            max_p = 0
            best_parse = None
            for item in trees:
                if item.prob() > max_p:
                    max_p = item.prob()
                    best_parse = item
            # Convert parse result to one-line format and write to the file
            ostr = re.sub('\s+', ' ', best_parse.pformat()) + '\n'
            output_file.write(ostr)
        line = sents_file.readline()
    sents_file.close()
    output_file.close()
    e = time.time()
    print('Baseline parser costs', e - s, 's')




