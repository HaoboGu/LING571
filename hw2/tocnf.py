import nltk
import sys
from nltk.grammar import is_nonterminal
from nltk.grammar import is_terminal
from nltk.grammar import Nonterminal
from nltk.grammar import Production
import time


def get_symbol(element):
    if is_nonterminal(element):
        return element.symbol()
    else:
        return element

def create_rule_series(productions):
    # eliminate long productions
    if len(productions.rhs()) <= 2:
        return productions
    else:
        new_symbol = get_symbol(productions.rhs()[1])  # rhs[0] + new_symbol
        for i in range(2, len(productions.rhs())):
            new_symbol = new_symbol + '_' + get_symbol(productions.rhs()[i])
        new_productions = [Production(productions.lhs(), (productions.rhs()[0], Nonterminal(new_symbol)))]
        new_productions.extend(create_rule_series_helper(productions.rhs()[1:]))
        return new_productions


def create_rule_series_helper(nonterminal_list):
    if len(nonterminal_list) < 2:
        return []
    else:
        new_symbol = get_symbol(nonterminal_list[1])
        for i in range(2, len(nonterminal_list)):  # combine last n-1 symbols as one
            new_symbol = new_symbol + '_' + get_symbol(nonterminal_list[i])
        lh_symbol = get_symbol(nonterminal_list[0]) + '_' + new_symbol  # symbol on the left hand
        productions = [Production(Nonterminal(lh_symbol), (nonterminal_list[0], Nonterminal(new_symbol)))]
        productions.extend(create_rule_series_helper(nonterminal_list[1:]))
        return productions


if __name__ == "__main__":
    s = time.time()
    use_local_file = True
    if use_local_file:
        # grammar_filename = "other_grammars/commandtalk_original.cfg"
        grammar_filename = 'toy1.cfg'
        output_filename = "output.txt"
    elif len(sys.argv) == 3:
        grammar_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        print("Number of args is not correct.")
        exit(0)

    gr = nltk.data.load(grammar_filename)  # load data

    print(len(gr.productions()))
    # Binarize non-binary rules
    for production in gr.productions():
        if len(production.rhs()) > 2:
            gr.productions().remove(production)  # remove non-binary productions
            gr.productions().extend(create_rule_series(production))  # add binarized productions
    print('after binarize:', len(gr.productions()))

    # Hybrid production
    for production in gr.productions():
        is_hybrid = 0
        if len(production.rhs()) > 1:  # more than one symbols are on the right hand side
            rh_list = []  # new list for right hand symbols
            new_productions = []  # list of new productions
            is_hybrid = 0  # flag that indicates if current production is hybrid
            for r_symbol in production.rhs():
                if is_terminal(r_symbol):  # for terminal symbol
                    dummy_symbol = Nonterminal(r_symbol)  # create dummy nonterminal
                    new_productions.append(Production(dummy_symbol, [r_symbol]))  # new unit production
                    rh_list.append(dummy_symbol)
                    is_hybrid = 1  # hybrid production confirmed
                else:  # for nonterminal symbol
                    rh_list.append(r_symbol)
            if is_hybrid:  # need to remove original production and add some productions
                new_productions.append(Production(production.lhs(), rh_list))  # new production with dummy symbol
                gr.productions().remove(production)  # remove hybrid productions
                gr.productions().extend(new_productions)  # add converted productions
    print('after converting hybrid:', len(gr.productions()))

    # Unit production conversion
    keep_looping = 1
    # maintain a set which is same as the production list to speed up the program
    production_set = set(gr.productions())
    nonterminal_set = {}
    while keep_looping:
        size = len(production_set)
        keep_looping = 0
        # TODO: check potential problems on nonterminal set
        for production in gr.productions():
            if len(production.rhs()) == 1 and is_nonterminal(production.rhs()[0]):  # A->B, B is non-terminal
                if production.rhs()[0] not in nonterminal_set:
                    nonterminal_set[production.rhs()[0]] = production.lhs()  # add B to a set
                    keep_looping = 1
            elif production.lhs() in nonterminal_set:  # B->... productions
                if len(production.rhs()) == 1 and is_terminal(production.rhs()[0]):  # B->b, b is terminal
                    # B->b, b is terminal
                    new_production = Production(nonterminal_set[production.lhs()], [production.rhs()[0]])
                    # if new_production not in gr.productions():
                    if new_production not in production_set:
                        production_set.add(new_production)  # add to the grammar
                        gr.productions().append(new_production)
                        keep_looping = 1
        print('after 1 loop of processing unit:', len(gr.productions()))
    for p in gr.productions():
        print(p)

    e = time.time()
    print(e-s)



