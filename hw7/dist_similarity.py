import sys
import os
import nltk
import re

def remove_puncs(raw_sentences):
    """
    Remove all punctuations in the raw data, including punctuations in the word
    :param raw_sentences: List[List[str]]
    :return: List[List[str]]
    """
    sentences_without_puncs = []
    for i in range(len(raw_sentences)):
        sent = ' '.join(raw_sentences[i])
        sent = re.sub('[^(\w| )]+', '', sent)  # remove all punctuations using Regex
        sentences_without_puncs.append(nltk.word_tokenize(sent))
    return sentences_without_puncs

__name__ = "__main__"
if __name__ == "__main__":
    use_local_file = True
    if use_local_file:
        if 'hw7' in os.listdir():
            os.chdir('hw7')
        window = 2
        weighting = "FREQ"
        # weighting = "PMI"
        judgment_filename = "mc_similarity.txt"
        output_filename = "hw7_sim_" + str(window) + "_" + weighting + "_output.txt"
    else:
        window = sys.argv[1]
        weighting = sys.argv[2]
        if weighting != "FREQ" or weighting != "PMI":
            print("Error: weighting must be FREQ or PMI")
        # weighting = "PMI"
        judgment_filename = sys.argv[3]
        output_filename = sys.argv[4]

    # brown_words = list(nltk.corpus.brown.words())[0:22079]
    brown_sentences = list(nltk.corpus.brown.sents())[0:1000]

    # First, remove all punctuations
    sentences = remove_puncs(brown_sentences)

    #



