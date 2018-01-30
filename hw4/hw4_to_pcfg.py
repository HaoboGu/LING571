import nltk
import sys
from nltk import induce_pcfg
from nltk.grammar import Nonterminal
import os


if __name__ == "__main__":
    use_local_file = True
    if use_local_file:
        if 'hw4' in os.listdir():
            os.chdir('hw4')
        treebank_filename = 'data/parses.train'
        output_pcfg_filename = "hw4_trained.pcfg"
    else:
        treebank_filename = sys.argv[1]
        output_pcfg_filename = sys.argv[2]

    # open tree bank file
    tb = open(treebank_filename)
    line = tb.readline()

    # set start symbol
    tree = nltk.tree.Tree.fromstring(line)
    start_symbol = Nonterminal(tree.label())

    # read trees and convert them to productions
    productions = []
    while line:
        tree = nltk.tree.Tree.fromstring(line)
        productions += tree.productions()
        line = tb.readline()
    tb.close()

    # convert list of productions to pcfg
    pcfg = induce_pcfg(start_symbol, productions)

    # write pcfg to file
    output_pcfg = open(output_pcfg_filename, 'w')

    # write production with start symbol first
    for prob_production in pcfg.productions():
        if prob_production.lhs() == start_symbol:

            output_pcfg.write(prob_production.__str__())
            output_pcfg.write('\n')
            pcfg.productions().remove(prob_production)
            break

    # write other productions
    for prob_production in pcfg.productions():
        output_pcfg.write(prob_production.__str__())
        output_pcfg.write('\n')
    output_pcfg.close()









