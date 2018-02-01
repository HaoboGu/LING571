import nltk
import sys
from nltk import induce_pcfg
from nltk.grammar import Nonterminal
from nltk.grammar import Production
import os


if __name__ == "__main__":
    use_local_file = False
    if use_local_file:
        if 'hw4' in os.listdir():
            os.chdir('hw4')
        treebank_filename = 'data/parses.train'
        output_pcfg_filename = "hw4_improved.pcfg"
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

    # Add productions dealing with *unknown* words
    lhs_set = []  # Set of non-terminals that derive terminals
    for p in productions:
        if p.is_lexical():
            lhs_set.append(p.lhs())
    for lhs in lhs_set:
        productions.append(Production(lhs, ['*unknown*']))

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
