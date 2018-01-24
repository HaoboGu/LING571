import nltk
import sys
import time
from nltk import word_tokenize
import numpy as np
from nltk.tree import Tree


def create_map(productions):
    """
    Create a dictionary mapping symbols on RHS to a set of symbols on LHS based on grammar
    :param productions: production list
    :return: a dictionary {tuple(symbols):set(LHS symbols)}
    """
    dict = {}
    for pr in productions:
        rhs = pr.rhs()  # tuple of symbols on the right hand
        if rhs not in dict:  # if the symbol is visited for the first time
            dict[rhs] = set()
        dict[rhs].add(pr.lhs())  # Add non-terminal on the left to the set

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
    For current cell [i,j], update tree list based on cell [i,k] and [k,j]
    :return: updated table
    """
    for s1 in table[i, k]:
        for s2 in table[k, j]:  # s1 and s2 are trees
            rhs = (s1.label(), s2.label())
            if rhs in symbol_map:  # check if rhs in current grammar's rules
                lhs = symbol_map[rhs]
                for l_symbol in lhs:
                    table[i, j].append(Tree(l_symbol, [s1, s2]))  # add current tree to cell [i,j]
    return table


def cky(words, grammar):
    """
        CKY algorithm, return a table of parsed result
        :param words: list of words
        :param grammar: nltk grammar
        :return: (n+1)*(n+1) table
    """
    rules = grammar.productions()
    symbol_map = create_map(rules)  # map RHS to a set of LHS according to the grammar
    d = len(words)
    # Create a d+1*d+1 table
    # Each cell [i,j] in the table represents set of non-terminals with derivation spanning i and j
    table = initialize_table(d + 1)
    for j in range(1, len(words)+1):
        j_tuple = tuple([words[j-1]])
        if j_tuple in symbol_map:
            for symbol in symbol_map[j_tuple]:  # for all terminals
                table[j - 1][j].append(Tree(symbol, [words[j-1]]))
        for i in range(j - 2, -1, -1):  # from j-2 to 0
            for k in range(i + 1, j):  # from i+1 to j-1
                table = update_cell(table, i, k, j, symbol_map)
    return table


if __name__ == "__main__":
    s = time.time()
    use_local_file = False
    if use_local_file:
        grammar_filename = 'grammar_cnf.cfg'
        test_sentence_filename = 'sentences.txt'
        output_filename = "output_parses.txt"
    else:
        grammar_filename = sys.argv[1]
        test_sentence_filename = sys.argv[2]
        output_filename = sys.argv[3]

    gr = nltk.data.load(grammar_filename)  # load data
    start_symbol = gr.start()  # get start symbol
    sen_file = open(test_sentence_filename)  # sentence file
    line = sen_file.readline()
    o_file = open(output_filename, 'w')  # output file
    s_parses = 0  # sum of parses for all sentences
    n_lines = 0  # number of line
    while line:
        n_lines += 1
        n_parses = 0  # number of parses for current sentence
        word_seq = word_tokenize(line)  # word sequence
        words_table = cky(word_seq, gr)  # cky algorithm
        o_file.write(line)  # print
        trees = words_table[0][words_table.shape[1]-1]
        for item in trees:
            if item.label() == start_symbol:  # count parses starting with start symbol
                o_file.write(item.__str__())
                o_file.write('\n')
                n_parses += 1
        s_parses += n_parses
        o_string = 'Number of parses: ' + str(n_parses) + '\n\n'
        o_file.write(o_string)
        line = sen_file.readline()
    o_file.close()
    sen_file.close()





