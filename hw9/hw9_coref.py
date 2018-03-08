import sys
import os
import nltk


if __name__ == "__main__":
    use_local_file = False
    if use_local_file:
        if 'hw9' in os.listdir('.'):
            os.chdir('hw9')
        grammar_filename = 'grammar.cfg'
        test_sentence_filename = 'coref_sentences.txt'
        output_filename = 'hw9_output.txt'
    else:
        grammar_filename = sys.argv[1]
        test_sentence_filename = sys.argv[2]
        output_filename = sys.argv[3]
    # Load grammar
    grammar = nltk.data.load(grammar_filename)
    # Set parser
    parser = nltk.parse.EarleyChartParser(grammar)
    # Load sentences
    sentences = nltk.data.load(test_sentence_filename).strip('\n').split('\n')

    # Get set of pronouns
    productions = grammar.productions()
    pronouns = []
    for item in productions:
        if item.lhs().symbol() in ['PRP', 'PossPro']:
            pronouns.append(item.rhs()[0])
    i = 0
    output_file = open(output_filename, 'w')
    while i < len(sentences)-1:
        sent1 = sentences[i]
        sent2 = sentences[i + 1]
        # Tokenize
        tokens1 = nltk.word_tokenize(sent1)
        tokens2 = nltk.word_tokenize(sent2)
        # Parse two sentences
        parses1 = parser.parse(tokens1)
        parses2 = parser.parse(tokens2)
        # Assume that there is at least one parse tree here
        tree1 = list(parses1)[0]
        tree2 = list(parses2)[0]
        #
        # tree1.pretty_print()
        # tree2.pretty_print()
        # print('********')
        leaves = tree2.leaves()
        pronoun_in_sent = [leave for leave in leaves if leave in pronouns]
        for word in pronoun_in_sent:
            out_str = word
            out_str = out_str + ' ' + tree1.pformat(margin=500) + ' ' + tree2.pformat(margin=500) + '\n'
            # print(out_str)
            output_file.write(out_str)
        output_file.write('\n')
        i += 3

    output_file.close()

