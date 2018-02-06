import nltk
import sys
import os
import numpy as np
import time
from nltk.parse import FeatureEarleyChartParser


if __name__ == "__main__":
    s = time.time()
    use_local_file = True
    if use_local_file:
        if 'hw4' in os.listdir():
            os.chdir('hw4')
        input_pcfg_filename = 'example_grammar.fcfg'
        sentences_filename = 'example_sentences.txt'
        output_parses_filename = "hw5_output.txt"
    else:
        input_pcfg_filename = sys.argv[1]
        sentences_filename = sys.argv[2]
        output_parses_filename = sys.argv[3]

    gr = nltk.data.load(input_pcfg_filename, format='fcfg')  # read fcfg grammar
    parser = FeatureEarleyChartParser(gr)
    with open(sentences_filename, 'r') as sent_file:
        line = sent_file.readline().strip('\n')
        while line:
            words = nltk.word_tokenize(line)
            try:
                parsed = parser.parse(words)
            except ValueError:
                print('A')
            line = sent_file.readline().strip('\n')

