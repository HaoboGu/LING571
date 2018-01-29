import nltk
import sys
import time
from nltk import word_tokenize
import numpy as np
from nltk.tree import Tree
from nltk.grammar import PCFG
from nltk import induce_pcfg
from nltk.grammar import Nonterminal
import os

if __name__ == "__main__":
    s = time.time()
    use_local_file = True
    if use_local_file:
        if 'hw4' in os.listdir():
            os.chdir('hw4')
        treebank_filename = 'data/parses.train'
        output_pcfg_filename = "hw4_trained.pcfg"
    else:
        treebank_filename = sys.argv[1]
        output_pcfg_filename = sys.argv[2]

    tb = open(treebank_filename)
    line = tb.readline()
    if line:
        tree = nltk.tree.Tree.fromstring(line)
        start_symbol = Nonterminal(tree.label())
        # print(start_symbol)
    productions = []
    while line:
        tree = nltk.tree.Tree.fromstring(line)
        productions += tree.productions()
        line = tb.readline()
    tb.close()
    if productions:
        pcfg = induce_pcfg(start_symbol, productions)

    output_pcfg = open(output_pcfg_filename, 'w')
    for prob_productions in pcfg.productions():
        output_pcfg.write(prob_productions.__str__())
        output_pcfg.write('\n')
    output_pcfg.close()









