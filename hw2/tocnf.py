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


def process_hybrid_productions(productions):
    new_productions_list = []  # list of new productions
    to_remove_list = []
    # Hybrid production
    for p in productions:
        is_hybrid = 0  # flag that indicates if current production is hybrid
        # print(production, len(production.rhs()))
        if len(p.rhs()) > 1:  # more than one symbols are on the right hand side
            rh_list = []  # new list for right hand symbols
            for r_symbol in p.rhs():
                if is_terminal(r_symbol):  # for terminal symbol
                    dummy_symbol = Nonterminal(r_symbol)  # create dummy nonterminal
                    new_productions_list.append(Production(dummy_symbol, [r_symbol]))  # new unit production
                    rh_list.append(dummy_symbol)
                    is_hybrid = 1  # hybrid production confirmed
                else:  # for nonterminal symbol
                    rh_list.append(r_symbol)
            if is_hybrid:  # need to remove original production and add some productions
                # in the loop, we won't change the list. Store them first.
                new_productions_list.append(Production(p.lhs(), rh_list))  # new production with dummy symbol
                to_remove_list.append(p)
    return to_remove_list, new_productions_list


def process_unit_productions(productions, nonterminal_set):
    # maintain a set which is same as the production list to speed up the program
    production_set = set(gr.productions())
    need_another_loop = 0
    to_remove = []
    for p in productions:
        if len(p.rhs()) == 1 and is_nonterminal(p.rhs()[0]):  # A->B, B is non-terminal
            to_remove.append(p)
            if p.rhs()[0] not in nonterminal_set:
                nonterminal_set[p.rhs()[0]] = p.lhs()  # add B to a set
                need_another_loop = 1
        elif p.lhs() in nonterminal_set:  # B->... productions
            if len(p.rhs()) == 1 and is_terminal(p.rhs()[0]):  # B->b, b is terminal
                new_production = Production(nonterminal_set[p.lhs()], [p.rhs()[0]])
                # if new_production not in gr.productions():
                if new_production not in production_set:
                    production_set.add(new_production)  # add to the grammar
                    # gr.productions().append(new_production)
                    to_add.append(new_production)
                    need_another_loop = 1
    return to_add, nonterminal_set, need_another_loop, to_remove


def write_grammar(grammar, filename):
    f = open(filename, 'w')
    start_state = grammar.start().__str__()
    start_state = "%start " + start_state + '\n\n'
    f.write(start_state)
    for p in grammar.productions():
        f.write(p.__str__())
        f.write('\n')
    f.close()

# g = nltk.data.load('hw2_grammar_cnf.cfg')
# print(g.is_chomsky_normal_form())


if __name__ == "__main__":
    s = time.time()
    use_local_file = True
    if use_local_file:
        # grammar_filename = "other_grammars/commandtalk_original.cfg"
        grammar_filename = 'atis.cfg'
        output_filename = "hw2_grammar_cnf.cfg"
    elif len(sys.argv) == 3:
        grammar_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        print("Number of args is not correct.")
        exit(0)

    gr = nltk.data.load(grammar_filename)  # load data

    print(len(gr.productions()))
    to_remove, to_add = process_hybrid_productions(gr.productions())
    # remove hybrid rules and add rules with dummy symbol
    for production in to_remove:
        gr.productions().remove(production)
    gr.productions().extend(to_add)
    print('after converting hybrid:', len(gr.productions()))

    # Binarize non-binary rules
    to_remove = []
    to_add = []
    for production in gr.productions():
        if len(production.rhs()) > 2:
            to_remove.append(production)
            to_add.extend(create_rule_series(production))
    for production in to_remove:
        gr.productions().remove(production)
    gr.productions().extend(to_add)  # add binarized productions
    print('after binarize:', len(gr.productions()))

    # Unit production conversion
    keep_looping = 1

    nonterminal_set = {}
    while keep_looping:
        to_add = []
        to_add, nonterminal_set, keep_looping, to_remove = process_unit_productions(gr.productions(), nonterminal_set)
        gr.productions().extend(to_add)
        print('after 1 loop of processing unit:', len(gr.productions()))

    for p in to_remove:
        gr.productions().remove(p)
    write_grammar(gr, output_filename)
    e = time.time()
    print(e-s)



