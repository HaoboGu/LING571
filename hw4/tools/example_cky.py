#!/usr/bin/env python3
"""
Basic Python CKY parser implementation.

Note that the root symbol is defined at
the top of the file.
"""
import sys, string, nltk
import collections
import argparse

# -------------------------------------------
# Root Symbol Definition
# -------------------------------------------
ROOT_SYMBOL = 'TOP'


def pprint(tree):
    """
    Prints a cleanly indented version of the parse tree.
    :param tree:
    :return:
    """
    out_str = ''
    indent_depth = 0
    indent_span = '  '
    open_brackets = tree.split('(')
    open_count = 0
    for open_bracket in open_brackets:
        if open_count > 0:
            ct = 0
            while ct < indent_depth:
                out_str += indent_span
                ct += 1
            out_str += '('
        if open_bracket.find(')') >= 0:
            closes = open_bracket.split(')')
            close_count = 0
            while close_count < len(closes)-1:
                out_str += closes[close_count] + ')'
                indent_depth -= 1
                close_count += 1
            out_str += '\n'
        else:
            out_str += open_bracket+'\n'
        if open_count > 0:
            indent_depth += 1

        open_count += 1

    print(out_str+'\n')


class Rule(object):
    """
    Representation of a rule A -> B ... C
    """
    def __init__(self, head, symbols):
        self.head = head
        self.symbols = symbols
        self._key = head, symbols

    def __eq__(self, other):
        return self._key == other._key

    def __hash__(self):
        return hash(self._key)


def get_grammar(grammar_data):
    """
    Build a grammar from strings like "X -> Y Z | b"
    :type grammar_data: str
    :rtype: set[Rule]
    """
    grammar = set()
    for line in grammar_data.splitlines():
        head, symbols_str = line.split(' -> ')
        for symbols_str in symbols_str.split(' | '):
            symbols = tuple(symbols_str.split())
            grammar.add(Rule(head, symbols))
    return grammar


def cky_table(grammar: set, words):
    """
    Given a grammar and the input words, build both the
    nonterminal table and backpointer table.
    :type grammar: set[rule]
    """
    nonterminal_table = collections.defaultdict(set)
    backpointer_table = collections.defaultdict(lambda: {})
    for j, word in enumerate(words):
        j += 1
        # find all rules for the current word
        for rule in grammar:
            if rule.symbols == (word,):
                nonterminal_table[j - 1, j].add(rule.head)
                backpointer_table[j - 1, j][rule.head] = []
                back = None, None, None
                backpointer_table[j - 1, j][rule.head].append(back)

        # for each span of words ending at the current word,
        # find all splits that could have formed that span
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                # if the two constituents identified by this
                # split can be combined, add the combination
                # to the table
                for rule in grammar:
                    if len(rule.symbols) == 2:
                        l_sym, r_sym = rule.symbols
                        if l_sym in nonterminal_table[i, k]:
                            if r_sym in nonterminal_table[k, j]:
                                nonterminal_table[i, j].add(rule.head)
                                back = k, l_sym, r_sym
                                if rule.head not in backpointer_table[i, j]:
                                    backpointer_table[i, j][rule.head] = []
                                if back not in backpointer_table[i, j][rule.head]:
                                    backpointer_table[i, j][rule.head].append(back)


        
    # return tree
    return get_tree(0, len(words), ROOT_SYMBOL, backpointer_table, words)

def get_tree(row, col, symbol, backpointer_table, words) -> list:
    """
    Helper function for converting backpointers to a tree
    :param row:
    :param col:
    :param symbol:
    :return:
    """
    mid, head1, head2 = backpointer_table[row, col][symbol][0]
    if mid is head1 is head2 is None:
        return ['(%s %s)' % (symbol, words[row])]
    trees = []
    for mid, head1, head2 in backpointer_table[row, col][symbol]:
        trees_left = get_tree(row, mid, head1, backpointer_table, words)
        trees_right = get_tree(mid, col, head2, backpointer_table, words)
        for tree_l in trees_left:
            for tree_r in trees_right:
                trees.append('(%s %s %s)' % (symbol, tree_l, tree_r))

    return(trees)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('grammarfile', help='Path to the CFG file to load.')
    p.add_argument('sentfile', help='Path to the sentences to parse.')

    args = p.parse_args()

    grammar_f = open(args.grammarfile,'r')
    grammar_text = ''.join(grammar_f.readlines())

    grammar_cnf = get_grammar(grammar_text.replace("'",''))

    with open(args.sentfile, 'r') as sent_f:

        for sent in sent_f.readlines():
            sent = sent[:-1]
            words = nltk.word_tokenize(sent)
            if len(words) > 0:
                trees = cky_table(grammar_cnf, words)

                # Print the sentence and number of parses.
                print(sent + ' ['+str(len(trees))+' parse(s)]\n')

                # Prettyprint the resulting parses.
                for tree in trees:
                    pprint(tree)
            else:
                print(sent)

main()
