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
        sentence = ' '.join(raw_sentences[i])
        sentence = re.sub('[^\w ]+', '', sentence.lower())  # remove all punctuations using Regex
        sentences_without_puncs.append(nltk.word_tokenize(sentence))
    return sentences_without_puncs


def initialize_feature_dict(all_words):
    """
    Initialize feature dictionary, based on words in word set
    :param all_words:
    :return: dictionary of features
    """
    temp = {}
    for w in all_words:
        temp[w] = 0

    features = {}
    for w in all_words:
        features[w] = temp.copy()
    return features


# def add_to_dict(dictionary, key, value):
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
    print('Reading corpus...')
    brown_sentences = list(nltk.corpus.brown.sents())[0:1000]

    # First, remove all punctuations
    print('Removing punctuations...')
    sentences = remove_puncs(brown_sentences)

    # Create the set of word
    word_set = set()
    for sent in sentences:
        word_set = word_set.union(set(sent))

    # Initialize the feature dictionary
    print('Initializing feature dict...')
    feat_dict = initialize_feature_dict(word_set)

    if weighting == 'FREQ':
        # Use frequency as the value of features
        for sent in sentences:
            length = len(sent)
            for i in range(length):
                cur_word = sent[i]
                for index in range(1, window+1):  # consider words in the window
                    if i+index < length:
                        feat_word = sent[i+index]
                        # current word is sent[i], add 1 on feature sent[i+index]
                        feat_dict[cur_word][feat_word] += 1
                    if i-index >= 0:
                        feat_word = sent[i-index]
                        # current word is sent[i], add 1 on feature sent[i-index]
                        feat_dict[cur_word][feat_word] += 1


    else:
        print(1)



