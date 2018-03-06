import sys
import os
import nltk


if __name__ == "__main__":
    use_local_file = True
    if use_local_file:
        if 'hw9' in os.listdir():
            os.chdir('hw9')
        grammar_filename = 'grammar.cfg'
        test_sentence_filename = 'coref_sentences.txt'
        output_filename = 'hw9_output.txt'
    else:
        grammar_filename = sys.argv[1]
        test_sentence_filename = sys.argv[2]
        output_filename = sys.argv[3]

    grammar = nltk.data.load(grammar_filename)
    parser = nltk.parse.EarleyChartParser(grammar)
    sentences = nltk.data.load(test_sentence_filename).strip('\n').split('\n')


    i = 0
    while i < len(sentences)-2:
        sent1 = sentences[i]
        sent2 = sentences[i+1]
        tokens1 = nltk.word_tokenize(sent1)
        tokens2 = nltk.word_tokenize(sent2)
        parses1 = parser.parse(tokens1)
        parses2 = parser.parse(tokens2)
        for item in parses2:
            print(item[0])
        i += 3




