import nltk
import sys
import os
import time
from nltk.parse import FeatureEarleyChartParser


if __name__ == "__main__":
    s = time.time()
    use_local_file = False
    if use_local_file:
        if 'hw5' in os.listdir():
            os.chdir('hw5')
        input_pcfg_filename = 'grammar.fcfg'
        sentences_filename = 'sentences.txt'
        output_parses_filename = "hw5_output.txt"
    else:
        input_pcfg_filename = sys.argv[1]
        sentences_filename = sys.argv[2]
        output_parses_filename = sys.argv[3]

    gr = nltk.data.load(input_pcfg_filename, format='fcfg')  # read fcfg grammar

    parser = FeatureEarleyChartParser(gr)  # Initialize parser

    output_file = open(output_parses_filename, 'w')

    # Parse sentences
    with open(sentences_filename, 'r') as sent_file:
        line = sent_file.readline().strip('\n')
        while line:
            words = nltk.word_tokenize(line)
            try:
                parsed = parser.parse(words)
                tree = parsed.__iter__()
                out_tree = ''
                for tree in parsed:
                    out_tree = tree.pformat(margin=sys.maxsize)
                    output_file.write(out_tree+'\n')
                    # print(out_tree)
                    break  # only print one possible tree
                if not out_tree:
                    output_file.write('\n')
            except ValueError:
                # print('\n')
                output_file.write('\n')
            line = sent_file.readline().strip('\n')

    output_file.close()
