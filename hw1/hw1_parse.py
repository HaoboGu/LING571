import nltk
import sys

if __name__ == "__main__":
    use_local_file = False
    if use_local_file:
        grammar_file = "toy.cfg"
        test_sentence_file = "toy_sentences.txt"
        output_file = "toy_output"
    elif sys.argv.__len__() == 4:
        grammar_file = sys.argv[1]
        test_sentence_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print("number of args is incorrect!")
        exit(0)

    grammar = nltk.data.load(grammar_file)
    parser = nltk.parse.EarleyChartParser(grammar)
    sentences = nltk.data.load(test_sentence_file).strip('\n').split('\n')
    o_file = open(output_file, 'w')
    sum_parses = 0
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        parses = parser.parse(tokens)
        n_parses = list(parses).__len__()
        sum_parses += n_parses
        o_file.write(sentence+'\n')
        # print(sentence)
        for item in parser.parse(tokens):
            o_file.write(str(item)+'\n')
        o_file.write("Number of parses: %d\n\n" % n_parses)

    o_file.write("Average parses per sentence: %.3f\n" % (sum_parses/len(sentences)))

