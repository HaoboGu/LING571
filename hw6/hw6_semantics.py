import nltk
import sys
import os
import time
from nltk.parse import FeatureChartParser

if __name__ == "__main__":
    s = time.time()
    use_local_file = False
    if use_local_file:
        if 'hw6' in os.listdir():
            os.chdir('hw6')
        input_pcfg_filename = 'grammar.fcfg'
        sentences_filename = 'sentences.txt'
        output_parses_filename = "hw6_output.txt"
    else:
        input_pcfg_filename = sys.argv[1]
        sentences_filename = sys.argv[2]
        output_parses_filename = sys.argv[3]

    gr = nltk.data.load(input_pcfg_filename, format='fcfg')  # read fcfg grammar

    parser = FeatureChartParser(gr)  # Initialize parserxx

    output_file = open(output_parses_filename, 'w')

    # Parse sentences
    with open(sentences_filename, 'r') as sent_file:
        line = sent_file.readline().strip('\n')
        while line:
            output_file.write(line+'\n')
            words = nltk.word_tokenize(line)
            try:
                parsed = parser.parse(words)
                tree = parsed.__iter__()
                out_tree = ''
                for tree in parsed:
                    out_tree = str(tree.label()['SEM'].simplify())
                    # print(tree.label()['SEM'].simplify())
                    output_file.write(out_tree+'\n')
                    # print(tree)
                    break  # only print one possible tree
                if not out_tree:
                    # print('')
                    output_file.write('\n')
            except ValueError:
                # print('')
                output_file.write('\n')
            line = sent_file.readline().strip('\n')

    output_file.close()
