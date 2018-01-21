import nltk
import sys
from nltk.grammar import is_nonterminal
from nltk.grammar import is_terminal
from nltk.grammar import Nonterminal
from nltk.grammar import Production
import time
from nltk import word_tokenize
import numpy as np

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
    Initialize a n_dimension*n_dimension table with empty sets and return it
    """
    table = np.zeros((n_dimension, n_dimension), dtype=object)
    for i in range(n_dimension):
        for j in range(n_dimension):
            table[i][j] = set()
    return table


def find_lhs(table, i, k, j, productions):
    """
    Look through the grammar and find lhs X where X satisfies {X->BC in grammar && B in table[i,k] && C in table[k,j]}
    :return:
    """
    return 0


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
    table = initialize_table(d+1)

    for j in range(1, len(words)+1):
        j_tuple = tuple([j])
        if j_tuple in symbol_map:
            table[j-1][j] = symbol_map[j_tuple]
        else:
            print("This word cannot be reached by the grammar")
        for i in range(j-2, -1, -1):  # from j-2 to 0
            for k in range(i+1, j):  # from i+1 to j-1
                X = find_lhs()
                table[i, j] = table[i, j].union(X)
                # where X satisfies {X->BC in grammar && B in table[i,k] && C in table[k,j]}


if __name__ == "__main__":
    s = time.time()
    use_local_file = True
    if use_local_file:
        # grammar_filename = "other_grammars/commandtalk_original.cfg"
        import os
        if 'hw3' in os.listdir():
            os.chdir('hw3')
        grammar_filename = 'grammar_cnf.cfg'
        test_sentence_filename = 'sentences.txt'
        output_filename = "output_parses.txt"

    else:
        grammar_filename = sys.argv[1]
        test_sentence_filename = sys.argv[2]
        output_filename = sys.argv[3]

    gr = nltk.data.load(grammar_filename)  # load data
    sen_file = open(test_sentence_filename)
    line = sen_file.readline()
    while line:
        word_seq = word_tokenize(line)
        cky(word_seq, gr)
        line = sen_file.readline()

    print(a)
    sen_file.close()




