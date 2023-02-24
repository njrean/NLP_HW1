from random import shuffle
from collections import Counter
import os

# --- data reader ---


def get_sentences(data_type):
    file_path = os.path.dirname(os.path.realpath(__file__))
    data_path = {
        'train': file_path + '/orchid_train.txt',
        'test': file_path + '/orchid_test.txt'
    }

    if data_type not in data_path:
        raise Exception('Please specify "train" or "test" to retrieve data.')

    file_path = data_path[data_type]
    sentences = list()
    current_sentences = list()
    with open(file_path) as data_file:
        for raw_line in data_file:
            line = raw_line.strip()
            if len(line) == 0:
                sentences.append(current_sentences)
                current_sentences = list()
            else:
                word, pos = line.split('\t')
                current_sentences.append((word, pos))

    if len(current_sentences) > 0:
        sentences.append(current_sentences)

    return sentences


def get_word_freq():
    sentences = get_sentences('train')
    tokens = [word for sent in sentences for (word, pos) in sent]
    word_freq = Counter(tokens)
    return word_freq


# --- preprocess ---
def raw_to_sentences():
    orchid_file_path = 'orchid97.txt'
    sentences = list()
    current_sentence = list()
    sentence_begin = False
    in_sentence = False
    special_sent = False

    with open(orchid_file_path) as orchid_file:
        for raw_line in orchid_file:
            line = raw_line.strip()

            if line[0] == '#' and line[1:].isdigit():
                sentence_begin = True

            elif sentence_begin:
                if line[0] == '%':
                    special_sent = True

                if line[-2:] == '//':
                    if not special_sent:
                        in_sentence = True
                    sentence_begin = False
                    special_sent = False

            elif in_sentence:
                if line == '//':
                    sentences.append(current_sentence)
                    current_sentence = list()
                    in_sentence = False
                else:
                    word, pos = line.split('/')
                    current_sentence.append((word, pos))

    train_boundary = int(len(sentences)*0.8)
    train_sentences = sentences[0:train_boundary]
    test_sentences = sentences[train_boundary:]

    write_orchid_file(train_sentences, 'orchid_train.txt')
    write_orchid_file(test_sentences, 'orchid_test.txt')


def write_orchid_file(sentences, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for sent in sentences:
            for (word, pos) in sent:
                output_file.write(word + '\t' + pos + '\n')
            output_file.write('\n')


if __name__ == '__main__':
    raw_to_sentences()